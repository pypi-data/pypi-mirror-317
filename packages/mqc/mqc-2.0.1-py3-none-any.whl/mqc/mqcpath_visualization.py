import sys
import os
import cobra
from cobra import Model, Reaction, Metabolite
import json
import re
import d3flux
import pandas as pd
# from bigg_function import *


def get_model_met_from_reaction_string(model,reaction_str,fwd_arrow,rev_arrow,reversible_arrow,term_split):
    # set the arrows
    forward_arrow_finder = (
            _forward_arrow_finder
            if fwd_arrow is None
            else re.compile(re.escape(fwd_arrow))
        )
    reverse_arrow_finder = (
            _reverse_arrow_finder
            if rev_arrow is None
            else re.compile(re.escape(rev_arrow))
        )
    reversible_arrow_finder = (
            _reversible_arrow_finder
            if reversible_arrow is None
            else re.compile(re.escape(reversible_arrow))
        )
    compartment_finder = re.compile("^\s*(\[[A-Za-z]\])\s*:*")
    found_compartments = compartment_finder.findall(reaction_str)
    if len(found_compartments) == 1:
        compartment = found_compartments[0]
        reaction_str = compartment_finder.sub("", reaction_str)
    else:
        compartment = ""
    # reversible case
    arrow_match = reversible_arrow_finder.search(reaction_str)
    if arrow_match is not None:
        pass
    else:  # irreversible
        # try forward
        arrow_match = forward_arrow_finder.search(reaction_str)
        if arrow_match is not None:
            pass
        else:
            # must be reverse
            arrow_match = reverse_arrow_finder.search(reaction_str)
            if arrow_match is None:
                raise ValueError("no suitable arrow found in '%s'" % reaction_str)
            else:
                pass
    reactant_str = reaction_str[: arrow_match.start()].strip()
    product_str = reaction_str[arrow_match.end() :].strip()
    for substr, factor in ((reactant_str, -1), (product_str, 1)): # (('asn-L_c + h2o_c', -1), ('NH4+ + asp-L_c', 1)) -1和1代表方程左边还是右边
        if len(substr) == 0:
            continue
        # substr： ’NH4+ + asp-L_c‘， term_split==’+‘，此时以+号分割就会把NH4+分割成NH4和空字符串，导致后面的met_id为空，从而导致错误
        # asn-L_c + h2o_c --> NH4+ + asp-L_c，方程里就是给的错误ID:NH4+,所以改掉cobra的内置函数————reaction.build_reaction_from_string(new_equ)，将其中分割的+号前加一个空格，即" +",nh4+就是一个整体了
        for term in substr.split(term_split):
            term = term.strip()
            if term.lower() == "nothing":
                continue
            if " " in term:
                num_str, met_id = term.split()
                num = float(num_str.lstrip("(").rstrip(")")) * factor
            else:
                met_id = term
                num = factor
            met_id += compartment  
            try:
                met = model.metabolites.get_by_id(met_id)
            except KeyError:
                met = Metabolite(met_id)
                model.add_metabolites(met)
                
                #reaction.add_metabolites({met: num})
    #model.add_reaction(reaction)
    return model  

def build_model_from_FBA_result_plus(model_pfba_solution,rxn_switch,coordinates, model, rxnId):
    """由FBA结果构建模型
    Arguments
    ----------
    * model_pfba_solution: 模型计算结果.
    :return: cobra model.
    """
    #print(substrate_id,product_id)
    # inimodel = cobra.io.load_json_model('data/ASGEM_20221124_python37.json')
    inimodel = model
    metlink_model = Model('metlink_model')
    

    for index, row in model_pfba_solution.iterrows():
        # new_equ=row['equ'].replace('__D_e','_e').replace('__L_e','_e')
        new_equ=row['equ']
        metlink_model=get_model_met_from_reaction_string(metlink_model,new_equ,fwd_arrow='-->', rev_arrow='<--', reversible_arrow='<=>', term_split=' +')
        reaction = Reaction(index) 
        reaction_infor=inimodel.reactions.get_by_id(index)
        # reaction_ano='Reaction id: <br/>'+str(index)+'<hr/>'+'Reaction name: <br/>'+str(index)+'<hr/>'+\
        #         'Reaction subsystem: <br/>'+'none'+'<hr/>'+'Reaction equation: <br/>'+\
        #         str(new_equ)+'<hr/>'+'Reaction gene_reaction_rule: <br/>'+'none'+'<hr/>'
        rxn_name = reaction_infor.build_reaction_string(use_metabolite_names=True)
        reaction_ano='Reaction id: <br/>'+str(index)+'<hr/>'+'Reaction name: <br/>'+str(index)+'<hr/>'+\
                'Reaction equation: <br/>'+str(new_equ)+'<hr/>'+'Reaction equation name: <br/>'+\
                    str(rxn_name)+'<hr/>'


        reaction.notes['map_info'] = {}
        reaction.notes['map_info']['annotation']=reaction_ano
        if rxn_switch == 'T':
            #reaction.notes['map_info']['display_name'] = reaction.id + " "+ str("%.2f" %(abs(row['fluxes'])))
            reaction.notes['map_info']['display_name'] = str("%.2f" %(abs(row['fluxes'])))
        elif rxn_switch == 'F':
            #reaction.notes['map_info']['display_name'] = reaction.name + " "+str("%.2f"%(abs(row['fluxes'])))
            reaction.notes['map_info']['display_name'] = str("%.2f"%(abs(row['fluxes'])))
        #d.notes.map_info.group   
        #[undefined, 'ko', 1, 2, 3, 4, 5, 6, 7, 8]
        if coordinates:#坐标轴赋值
            if 'reactions' in coordinates.keys():
                if index in coordinates['reactions']:
                    reaction.notes['map_info']['x'] = float(coordinates['reactions'][index]['x'])
                    reaction.notes['map_info']['y'] = float(coordinates['reactions'][index]['y'])
        
        if index == rxnId:
            reaction.notes['map_info']['group']=1 # 目标反应显示红色
        # if index in model_change_json['exchange_infor'].keys():
        #     reaction.notes['map_info']['group']=4
        # if index in model_change_json['add_reaction_infor'].keys():
        #     reaction.notes['map_info']['group']=5       
        # elif index in model_change_json['del_reaction_infor'].keys():
        #     reaction.notes['map_info']['group']=1    
        # elif index in model_change_json['del_gene_infor'].keys():
        #     reaction.notes['map_info']['group']=1 
        # else:
        #     reaction.notes['map_info']['group']=3
        metlink_model.add_reactions([reaction])
        reaction.build_reaction_from_string(new_equ)  
    #print(len(metlink_model.reactions.get_by_id('DM_pyr_c').products))  
    display_name_format = (lambda met: re.sub('__[D,L]', '', met.id[:-2].upper()))

    for eachmet in metlink_model.metabolites:
        mets = inimodel.metabolites.get_by_id(eachmet.id)
        eachmet.compartment = mets.compartment
        # print(eachmet.compartment,'..................................')
        if re.search('_c',eachmet.id):
            eachmet.compartment='c'
        elif re.search('_p',eachmet.id):
            eachmet.compartment='p'
        elif re.search('_e',eachmet.id):
            eachmet.compartment='e'  
            
        try:
            inimodel.metabolites.get_by_id(eachmet.id)
        except:
            eachmet_id= "_e".join(eachmet.id.split('_e')[:-1])+'__D_e' 
            try:
                inimodel.metabolites.get_by_id(eachmet_id)
            except:
                eachmet_id= "_e".join(eachmet.id.split('_e')[:-1])+'__L_e' 
                try:
                    inimodel.metabolites.get_by_id(eachmet_id)
                except:
                    pass
                else:
                    metabolite_infor=inimodel.metabolites.get_by_id(eachmet_id)
            else:
                metabolite_infor=inimodel.metabolites.get_by_id(eachmet_id)
        else:
            metabolite_infor=inimodel.metabolites.get_by_id(eachmet.id)
        eachmet.name='Metabolite id: <br/>'+str(eachmet.id)+'<hr/>'+'Metabolite name: <br/>'+str(metabolite_infor.name)+'<hr/>'+\
                        'Metabolite formula: <br/>'+str(metabolite_infor.formula)+'<hr/>'
        eachmet.notes['map_info'] = {}
        #eachmet.notes['map_info']['annotation']=metabolite_ano
        rxns = model.reactions.get_by_id(rxnId)
        # if eachmet.id in ['nadh_c','nad_c','atp_c','atp_p', 'atp_e','C00002', 'C00002[c]','C00002[p]','C00002[e]','ATP', 'MNXM3', 'cpd00002', 'cpd00002_c0','cpd00002_p0','cpd00002_e0', 'HMDB00538', 'ZKHQWZAMYRWXGA-KQYNXXCUSA-J','adp_c','adp_p','adp_e','C00008','C00008[c]', 'ADP', 'MNXM7','cpd00008','cpd00008_c0','cpd00008_p0','cpd00008_e0', 'HMDB01341', 'XTWYTFMLZFPYCI-KQYNXXCUSA-K','nadph_c','NADPH','C00005','C00005[c]','MNXM6','HMDB00221', 'HMDB00799', 'HMDB06341','cpd00005','ACFIXJIJDZMPPO-NNYOXOHSSA-J','nadph','META:NADPH','cpd00005_c0','nadp_c','NADP','MNXM5','C00006','C00006[c]','HMDB00217','cpd00006','XJLXINKUBYWONI-NNYOXOHSSA-K','META:NADP','nadp','cpd00006_c0']:    # [ATP,'cpd00002',ADP,'cpd00008',鲜肉(鲑鱼)色]
        #     eachmet.notes['map_info']['color'] = "#FA8072"
        if eachmet.id in [m.id for m in rxns.metabolites]:
            eachmet.notes['map_info']['color'] = "f08080"
        # elif met.id[:-3] in ['cpd00003', 'cpd00004', 'cpd00005', 'cpd00006']:# [nad、nadh、nadp、nadph]绿宝石
        #     met.notes['map_info']['color'] = "#008000"
        else:   #  其他为适中的碧绿色
            eachmet.notes['map_info']['color'] = "#00FA9A" 
        if coordinates:#坐标轴赋值
            cormet=display_name_format(eachmet)
            if 'metabolites' in coordinates.keys():
                #print(cormet,cormet.lower())
                if cormet.lower() in coordinates['metabolites'].keys():
                    eachmet.notes['map_info']['x'] = float(coordinates['metabolites'][cormet.lower()]['x'])
                    eachmet.notes['map_info']['y'] = float(coordinates['metabolites'][cormet.lower()]['y'])
        # if eachmet.id.endswith('_c') or eachmet.id.endswith('_C') or eachmet.id.endswith('_p') or eachmet.id.endswith('_P') or eachmet.id.endswith('_e') or eachmet.id.endswith('_E'):
        #     pass
        # else:
        #     eachmet.id=eachmet.id+'_c'
    return metlink_model

def get_model_information(model):
    All_met = []
    All_rxn = []
    for met in model.metabolites:
        All_met.append(met.id)
        # print(met.id,met.name,'............................')
    for rxn in model.reactions:
        All_rxn.append(rxn.id)  # 所有 rxn
    uni_All_met=list(set(All_met))
    uni_All_rxn=list(set(All_rxn))
    return uni_All_met, uni_All_rxn

def pathway_tsv_visualization(pathway_tsv_file,cofactor_switch,flow,outputdir, rxnId, model):
    exclude_rxn = ['EX_co2_e','H2Otex','O2tpp','CO2tpp','O2tex','NH4tex','CO2tex','NH4tpp','H2Otpp','EX_o2_e','EX_h2o_e','EX_nh4_e','EX_o2_e','ADD_h_c','ADD_h_p','ADD_respiratory1']
    total_common_factor_list =  ['hco3_c','ni2_c','cdp_c', 'ag_c', 'dctp_c', 'dutp_c', 'ctp_c', 'gdp_c', 'gtp_c', 'ump_c', 'ca2_c', \
                            'h2o_c', 'datp_c', 'co2_c', 'no2_c', 'no_c', 'k_c', 'zn2_c', 'no3_c', 'o2_c', 'cl_c', 'udp_c', 'damp_c',\
                            'ditp_c', 'dump_c', 'q8h2_c', 'pppi_c', 'idp_c', 'dimp_c', 'pi_c', 'dttp_c', 'so4_c', 'adp_c', 'xtp_c',\
                            'dgtp_c', 'dadp_c', 'coa_c', 'ppi_c', 'h2_c', 'cmp_c', 'fe2_c', 'o2s_c', 'h_c', 'gmp_c', 'itp_c', 'q8_c', \
                            'cobalt2_c', 'n2o_c', 'xmp_c', 'xdp_c', 'nadph_c', 'cu_c', 'cu2_c', 'atp_c', 'dgmp_c', 'imp_c', 'h2s_c', 'utp_c',\
                            'dtmp_c', 'fadh2_c', 'so3_c', 'fad_c', 'cd2_c', 'dgdp_c', 'nad_c', 'nadh_c', 'hg2_c', 'dcmp_c', 'dudp_c', 'dtdp_c',\
                            'didp_c', 'mn2_c', 'dcdp_c', 'nh4_c', 'amp_c', 'fe3_c', 'nadp_c', 'so2_c', 'h2o2_c', 'mg2_c',\
                                'hco3_p','ni2_p','cdp_p', 'ag_p', 'dctp_p', 'dutp_p', 'ctp_p', 'gdp_p', 'gtp_p', 'ump_p', 'ca2_p', \
                            'h2o_p', 'datp_p', 'co2_p', 'no2_p', 'no_p', 'k_p', 'zn2_p', 'no3_p', 'o2_p', 'cl_p', 'udp_p', 'damp_p',\
                            'ditp_p', 'dump_p', 'q8h2_p', 'pppi_p', 'idp_p', 'dimp_p', 'pi_p', 'dttp_p', 'so4_p', 'adp_p', 'xtp_p',\
                            'dgtp_p', 'dadp_p', 'coa_p', 'ppi_p', 'h2_p', 'cmp_p', 'fe2_p', 'o2s_p', 'h_p', 'gmp_p', 'itp_p', 'q8_p', \
                            'cobalt2_p', 'n2o_p', 'xmp_p', 'xdp_p', 'nadph_p', 'cu_p', 'cu2_p', 'atp_p', 'dgmp_p', 'imp_p', 'h2s_p', 'utp_p',\
                            'dtmp_p', 'fadh2_p', 'so3_p', 'fad_p', 'cd2_p', 'dgdp_p', 'nad_p', 'nadh_p', 'hg2_p', 'dcmp_p', 'dudp_p', 'dtdp_p',\
                            'didp_p', 'mn2_p', 'dcdp_p', 'nh4_p', 'amp_p', 'fe3_p', 'nadp_p', 'so2_p', 'h2o2_p', 'mg2_p',\
                                'hco3_e','ni2_e','cdp_e', 'ag_e', 'dctp_e', 'dutp_e', 'ctp_e', 'gdp_e', 'gtp_e', 'ump_e', 'ca2_e', \
                            'h2o_e', 'datp_e', 'co2_e', 'no2_e', 'no_e', 'k_e', 'zn2_e', 'no3_e', 'o2_e', 'cl_e', 'udp_e', 'damp_e',\
                            'ditp_e', 'dump_e', 'q8h2_e', 'pppi_e', 'idp_e', 'dimp_e', 'pi_e', 'dttp_e', 'so4_e', 'adp_e', 'xtp_e',\
                            'dgtp_e', 'dadp_e', 'coa_e', 'ppi_e', 'h2_e', 'cmp_e', 'fe2_e', 'o2s_e', 'h_e', 'gmp_e', 'itp_e', 'q8_e', \
                            'cobalt2_e', 'n2o_e', 'xmp_e', 'xdp_e', 'nadph_e', 'cu_e', 'cu2_e', 'atp_e', 'dgmp_e', 'imp_e', 'h2s_e', 'utp_e',\
                            'dtmp_e', 'fadh2_e', 'so3_e', 'fad_e', 'cd2_e', 'dgdp_e', 'nad_e', 'nadh_e', 'hg2_e', 'dcmp_e', 'dudp_e', 'dtdp_e',\
                            'didp_e', 'mn2_e', 'dcdp_e', 'nh4_e', 'amp_e', 'fe3_e', 'nadp_e', 'so2_e', 'h2o2_e', 'mg2_e', 'flxso_c','flxr_c','WATER_c',\
                            'PROTON_c','NADH_c','NAD_c','NADPH_c','NADP_c','ATP_c','ADP_c','Pi_c','pqq_c','pqqh2_c']
    #由通量数据构建model 便于后续获得metlink
    rxn_switch = 'F'
    cofactor_switch = "T"
    id_or_name = True
    # flow = True 
    coordinates= False

    if flow == "True":
        flow = True
    else:
        flow = False


    # outfolder = pathway_outputpath # 读取途径生成文件
    # for file_name in os.listdir(outfolder): #得到文件夹下所有文件名
        # if 'summary' not in file_name and 'tsv' in file_name: 
    pathway_df = pd.read_table(pathway_tsv_file,header=None)
    pathway_df.columns = ['id','fluxes','equ','equName','bounds','check']
    pathway_df.set_index('id',inplace=True)
    
    metlink_model = build_model_from_FBA_result_plus(pathway_df,rxn_switch,coordinates, model, rxnId)
    
    # 可视化
    All_met, All_rxn= get_model_information(metlink_model)
    #print(All_rxn)
    common_factor_list=list(set(total_common_factor_list).intersection(set(All_met)))
    if cofactor_switch == "T":
        d3flux.update_cofactors(metlink_model, common_factor_list)

    html = d3flux.flux_map(metlink_model, overwrite_reversibility=True,
                        excluded_metabolites = common_factor_list,excluded_reactions =exclude_rxn,
                        figsize=(1000, 1000), display_name_format=id_or_name,
                        hide_unused="true", hide_unused_cofactors="true",
                        flux_dict=pathway_df['fluxes'],
                        flowLayout = flow)  # 是否要隐藏flux为0的

    # show_factor_file = './show_factor.html'  # 前端d3flux可视化文件
    html_file = os.path.join(outputdir,f"{rxnId}.html")
    with open(html_file, "w")as wf:
        wf.write(html.data)



