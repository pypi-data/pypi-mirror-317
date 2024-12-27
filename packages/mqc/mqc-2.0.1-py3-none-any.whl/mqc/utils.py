# -*- coding: utf-8 -*-

from cobra import Model, Reaction, Metabolite
import pandas as pd
import math 
import re, os
import json
import cobra 
import d3flux
from cobra.util.solver import linear_reaction_coefficients
from cobra.flux_analysis import pfba
from cobra.io.dict import model_to_dict
import time 
# from mqc.config import cfg
from mqc.defaults import *
from mqc.mqcpath_visualization import *
from mqc.control.rules_control2 import Rules2



def add_rxn(model, rxn_name, rxn_expression):
    """
    Add the reaction to the model.

    Parameters
    ----------
    rxn_name : str
        Reactive name —— "ADD_ATPM"
    rxn_expression : str
        Reactive expression —— "atp_c + h2o_c  --> adp_c + h_c + pi_c"
    model : cobra.Model
 
    Return
    ------
    cobra.Model
        The model after adding the reaction

    """
    reaction = Reaction(rxn_name)
    model.add_reactions([reaction])
    try:
        reaction.build_reaction_from_string(rxn_expression)
        print('add_rxn...............',rxn_name)
    except:
        print('交换反应添加失败',rxn_name)
        pass
    return model 

def select_more_met(model, met_list):
    """"""
    more_met = {}
    if len(met_list) == 1:
        return met_list[0]
    else:
        for met in met_list:
            more_met[met] = len(model.metabolites.get_by_id(met).reactions)
        for mets,nums in more_met.items():
            if nums == max(more_met.values()):
                return mets

def add_atpm_rxn(model, xTP, xDP):
    """
    Add atpm reaction to model.

    Parameters
    ----------
    model : cobra.Model

    Return
    ------
    cobra.Model
        Model after adding atpm 

    """
    atp_list, adp_list, h2o_list, h_list, pi_list = [], [], [], [], []
    for met in model.metabolites:
        if met.name in eval(f'{xTP}_NAME') and met.compartment in C_COMPARTMENT: atp_list.append(met.id)
        if met.name in H_NAME and met.compartment in C_COMPARTMENT: h_list.append(met.id)
        if met.name in eval(f'{xDP}_NAME') and met.compartment in C_COMPARTMENT: adp_list.append(met.id)
        if met.name in H2O_NAME and met.compartment in C_COMPARTMENT: h2o_list.append(met.id)
        if met.name in PI_NAME and met.compartment in C_COMPARTMENT: pi_list.append(met.id)
    atp_c = select_more_met(model, atp_list)
    h_c = select_more_met(model, h_list)
    adp_c = select_more_met(model, adp_list)
    h2o_c = select_more_met(model, h2o_list)
    pi_c = select_more_met(model, pi_list)
    if not atp_c or not h_c or not adp_c or not h2o_c or not pi_c:
        return ''
    rxn_name = f"ADD_{xTP}M"
    rxn_exp = "{} + {} --> {} + {} + {}".format(atp_c, h2o_c, adp_c, h_c, pi_c)
    print(rxn_name,rxn_exp)
    add_rxn(model, rxn_name, rxn_exp)
    return rxn_name 


def add_nadh_rxn(model):
    """
    Add nadh reaction to model.

    Parameters
    ----------
    model : cobra.Model

    Return
    ------
    cobra.Model
        Model after adding nadh 

    """
    nadh_list, h_list, nad_list = [], [], []
    for met in model.metabolites:
        if met.name in NADH_NAME and met.compartment in C_COMPARTMENT: nadh_list.append(met.id)
        if met.name in H_NAME and met.compartment in C_COMPARTMENT: h_list.append(met.id)
        if met.name in NAD_NAME and met.compartment in C_COMPARTMENT: nad_list.append(met.id) 
    nadh_c = select_more_met(model, nadh_list)
    h_c = select_more_met(model, h_list)
    nad_c = select_more_met(model, nad_list)
    if not nadh_c or not h_c or not nad_c:
        return ''
    rxn_name = "ADD_NADH"
    rxn_exp = "{} + {} --> {}".format(nadh_c, h_c, nad_c)
    print(rxn_name,rxn_exp)
    add_rxn(model, rxn_name, rxn_exp)
    return rxn_name 

def get_other_nadh_rxn(model, rea, pro1, pro2, name):
    """"""
    nadh_list, h_list, nad_list = [], [], []
    for met in model.metabolites:
        if met.name in rea and met.compartment in C_COMPARTMENT: nadh_list.append(met.id)
        if met.name in pro1 and met.compartment in C_COMPARTMENT: h_list.append(met.id)
        if met.name in pro2 and met.compartment in C_COMPARTMENT: nad_list.append(met.id) 
    nadh_c = select_more_met(model, nadh_list)
    h_c = select_more_met(model, h_list)
    nad_c = select_more_met(model, nad_list)
    if not nadh_c or not h_c or not nad_c:
        return ''
    rxn_name = f"ADD_{name}"
    rxn_exp = "{} --> {} + {}".format(nadh_c, h_c, nad_c)
    print(rxn_name,rxn_exp)
    add_rxn(model, rxn_name, rxn_exp)
    return rxn_name 

def first_get_biomass_rxn(model, initial_rxn_id):
    """"""
    if initial_rxn_id:
        initial_rxn = model.reactions.get_by_id(initial_rxn_id)
        mets = list(initial_rxn.metabolites.keys())[0]
        if len(initial_rxn.metabolites) == 1 and 'biomass' in mets.id.lower() or mets.id.lower() in 'biomass' or mets.name in BIOMASS or 'biomass' in mets.name.lower():
            ids = mets.id
            for rxn in model.reactions:
                if any(ids in k.id for k in rxn.products if len(rxn.products) > 1):
                    return rxn.id
    for rxn in model.reactions:
        if len(rxn.metabolites) == 1:
            mets = list(rxn.metabolites.keys())[0]
            if 'biomass' in mets.id.lower() or mets.id.lower() in 'biomass' or mets.name in BIOMASS or 'biomass' in mets.name.lower():
                ids = mets.id
                for rxn in model.reactions:
                    if any(ids in k.id for k in rxn.products if len(rxn.products) > 1):
                        return rxn.id
    return ""

def get_biomass_rxn(model):
    """"""
    biomassId, num = [], 0
    for rxn in model.reactions:
        all_met_id = [met.id for met in rxn.metabolites]
        all_met_name = [met.name.lower() for met in rxn.metabolites]
        if len(set(PROTEIN) & set(all_met_id)) != 0 and len(set(DNA_RNA) & set(all_met_id)) >= 2:
            biomassId.append(rxn.id)
        if len(set(PROTEIN_COMPOSITION + DNA_COMPOSITION + RNA_COMPOSITION) & set(all_met_id)) >= 16 and len(set(DNA_COMPOSITION + RNA_COMPOSITION) & set(all_met_id)) >= 4:
            biomassId.append(rxn.id)
        if any(['protein' in k for k in all_met_name]) : num += 1
        if any(['dna' in k for k in all_met_name]) : num += 1
        if any(['rna' in k for k in all_met_name]) : num += 1
        if any(['lipid' in k for k in all_met_name]) : num += 1
        if num == 4:
            biomassId.append(rxn.id)
        num = 0
    biomassId = list(set(biomassId))
    return biomassId

def check_biomass_rxn(model, biomass_rxn_id):
    """"""
    not_contained, special_macro,temp = [], ['dna', 'rna', 'protein', 'lipid', 'peptido', 'cellwall'],[]
    protein_composition = {'Protein_ala': ALA,'Protein_arg':ARG,'Protein_asn': ASN,'Protein_asp': ASP,'Protein_cys': CYS,'Protein_gln': GLN,'Protein_glu': GLU,
                'Protein_gly': GLY,'Protein_his': HIS,'Protein_ile': ILE,'Protein_leu': LEU,'Protein_lys': LYS,'Protein_met': MET,'Protein_phe': PHE,
                'Protein_pro': PRO,'Protein_ser': SER,'Protein_thr': THR,'Protein_trp': TRP,'Protein_tyr': TYR,'Protein_val': VAL
        }
    dna_rna_composition = {
        'DNA_datp':DATP ,'DNA_dctp': DCTP,'DNA_dgtp': DGTP,'DNA_dttp': DTTP,'RNA_ctp': CTP,'RNA_gtp': GTP,'RNA_utp':UTP,'RNA_atp': ATP
        }
    rxns = model.reactions.get_by_id(biomass_rxn_id)
    all_met_id = [met.id for met in rxns.metabolites]
    left_met_name = [met.name for met in rxns.reactants]
    if any(macro in metName.lower() for macro in special_macro for metName in left_met_name): # 有大分子时看缺什么大分子，没有才看缺什么小分子
        for macro in special_macro:
            for metName in left_met_name:
                if macro in metName.lower():
                    temp.append(macro)
                    break 
        not_contained = [k for k in special_macro if k not in temp]
    else:
        for name, compose in {**protein_composition, **dna_rna_composition}.items():
            if len(set(compose) & set(all_met_id)) == 0:
                not_contained.append(name)
    return not_contained

def find_biomass_rxn(model):
    """"""
    try:
        initial_rxn_id = list(linear_reaction_coefficients(model).keys())[0].id
    except:
        initial_rxn_id = ''
    biomassIds = get_biomass_rxn(model)
    if biomassIds or initial_rxn_id:
        return 1
    else:
        return 0

       

def get_atpm_rxn(model_info, model, xTP, xDP):
    """
    get atpm reactions
    """
    if (xTP == 'ATP' and len(set(model_info["all_rxn_id"]) & set(ATPM)) == 0) or (xTP != 'ATP'):
        atpm_id = add_atpm_rxn(model, xTP, xDP)
    else:
        atpm_id = [i for i in ATPM if i in model_info["all_rxn_id"]][0]
    return atpm_id


def set_initial_obj(model):
    """
    Find the biomass equation and set it as the target.

    Parameters
    ----------
    model : cobra.Model

    Return
    ------
    str
        biomass equation ID

    """
    for rxn in model.reactions:
        all_mets = [m.id for m in rxn.metabolites]
        if len(all_mets) != 1 and ('bio' in rxn.id or 'biomass' in rxn.id or 'BIO' in rxn.id or 'BIOMASS' in rxn.id):
            return rxn.id
        else :
            return ''



def set_initial_obj2(model, rxnId):
    """
    Find the biomass equation and set it as the target.

    Parameters
    ----------
    rxnId : str
        Initial goals for model setup

    Notes
    -----
    The initial goal is biomass_c ⇌, Re-find the new biomass equation from the model

    """
    rxn = model.reactions.get_by_id(rxnId)
    all_mets = [m.id for m in rxn.metabolites]
    if len(all_mets) == 1 and ('bio' in rxn.id or 'biomass' in rxn.id or 'BIO' in rxn.id or 'BIOMASS' in rxn.id):
        for rxns in model.reactions:
            products_mets = [m.id for m in rxns.products]
            if all_mets[0] in products_mets:
                return rxns.id
            else:
                return ''
    else:
        return rxnId

def add_demand(modelInfo, model, metId):
    """
    Add demand reaction.

    Parameters
    ----------
    modelInfo : dict
        Information about the model
    metId : str
        The metabolite ID that needs to be added to the demand reaction

    Notes
    -----
    If there is an exchange reaction containing the metabolite ID in the model, set it directly as the target, otherwise add the demand reaction

    """
    mets = model.metabolites.get_by_id(metId) 
    flag, objectiveId = 0, ''
    for rxn in modelInfo["reactions"]:
        rxns = model.reactions.get_by_id(rxn['id'])
        all_mets = [met.id for met in rxns.metabolites]
        if metId in all_mets and len(all_mets) == 1 and ((rxn['reactants_mets'] and rxn["bounds"][1] > 0) or (rxn['products_mets'] and rxn['bounds'][0] < 0)):
            objectiveId = rxn["id"]
            flag += 1
    if flag == 0:
        if f"DM_{metId}" in modelInfo["all_rxn_id"]: # if 'DM_' + metId in modelInfo["all_rxn_id"]:TypeError: can only concatenate str (not "Metabolite") to str
            objectiveId = f"DM_{metId}"
        else:
            try:
                demand_rxn = model.add_boundary(mets, type = 'demand') # 添加demand反应
                objectiveId = demand_rxn.id
            except:
                objectiveId = f"DM_{metId}"
    return objectiveId

def add_accoa(model, metId):
    """"""
    coa_c = ''
    for met in model.metabolites:
        if met.name in COA and met.compartment in C_COMPARTMENT:
            coa_c = met.id
            break
    if not coa_c:
        return ''
    rxn_name = "ADD_ACOA"
    rxn_exp = "{} --> {}".format(metId, coa_c)
    add_rxn(model, rxn_name, rxn_exp)
    return rxn_name

def set_model_objective(modelInfo, model, rxnId):
    """
    Set the incoming response ID as the target and update modelInfo.
    """
    # now_obj_rxn_info = []
    model.objective = rxnId
    now_obj_rxn_flux = model.slim_optimize()
    now_obj_rxn_exp = model.reactions.get_by_id(rxnId).build_reaction_string(use_metabolite_names=True)
    now_obj_rxn_exp_id = model.reactions.get_by_id(rxnId).build_reaction_string()
    NowObjRxnInfo = {"rxn_id" : rxnId,
                    "rxn_flux" : now_obj_rxn_flux,
                    "rxn_exp" : now_obj_rxn_exp,
                    "rxn_exp_id" : now_obj_rxn_exp_id}
    # now_obj_rxn_info.append(NowObjRxnInfo)
    modelInfo["now_obj_rxn"] = NowObjRxnInfo


def is_bio_exp_correct(modelInfo):
    """
    Judging whether the biomass response of the model is correctly represented.
    """
    # id_index = modelInfo["initial_rxn"].index("initial_rxn_id")
    if not modelInfo["initial_rxn"]["biomass_rxn_id"]:
        return 0
    return 1


def relative_molecular_mass(model, metid):
    """
    Judging whether the biomass response of the model is correctly represented.
    """
    met = model.metabolites.get_by_id(metid)
    mass = 0
    if pd.isna(met.formula) or 'R' in met.formula or 'X' in met.formula or met.formula == 'nan' or not met.formula:
        return 0
    for e,en in met.elements.items():
        if e == 'C': mass += 12*en       
        if e == 'H': mass += 1*en         
        if e == 'O': mass += 16*en        
        if e == 'N': mass += 14*en        
        if e == 'P': mass += 31*en        
        if e == 'S': mass += 32*en       
        if e == 'Ca': mass += 40*en         
        if e == 'Mn': mass += 55*en         
        if e == 'Fe': mass += 56*en     
        if e == 'Zn': mass += 65*en
        if e == 'Na': mass += 23*en
        if e == 'Mg': mass += 24*en
        if e == 'Al': mass += 27*en 
        if e == 'Si': mass += 28*en 
        if e == 'Cl': mass += 35.5*en 
        if e == 'K': mass += 39*en 
        if e == 'Cu': mass += 64*en 
        if e == 'Ag': mass += 108*en 
        if e == 'I': mass += 127*en 
        if e == 'Au': mass += 197*en 
        if e == 'Ba': mass += 137*en 
    return mass


def reduced_degree(model, metId):
    """Calculating the degree of reduction of a metabolite's single carbon"""
    met = model.metabolites.get_by_id(metId)
    degree = 0
    for e,en in met.elements.items():
        if e == 'C':
            degree = degree  + 4*en
        if e == 'H':
            degree = degree  + 1*en
        if e == 'O':
            degree = degree  + (-2)*en
        if e == 'N':
            degree = degree  + (-3)*en
        if e == 'P':
            degree = degree  + (5)*en
        if e == 'S':
            degree = degree  + (6)*en
    if pd.isna(met.charge) or met.charge == 'nan' or not met.charge:
        met.charge = 0
    degree = degree - met.charge
    return degree

def max_reduced_degree_rate(model, metId, model_info):
    """Calculate the theoretical yield of the maximum reduction degree of the product"""
    c_met_degree, max_rate, s_met_degree, N_met_degree, met_degree = 0, 0, 0, 0, 0
    temp = []
    if model.slim_optimize() > 0:
        pfba_solution = pfba(model)
        need_fluxes = pfba_solution.fluxes[abs(pfba_solution.fluxes)>1e-6] 
    else:
        need_fluxes = {}
    # need_fluxes=model.optimize().fluxes[abs(model.optimize().fluxes)>1e-6]
    degree = reduced_degree(model, metId)
    met_accoa = model.metabolites.get_by_id(metId)
    if met_accoa.name in ACCOA and met_accoa.compartment in C_COMPARTMENT:
        for met in model.metabolites:
            if met.name in COA and met.compartment in C_COMPARTMENT:
                coa_c = met.id
                break
        coa_degree = reduced_degree(model, coa_c)
        degree -= coa_degree
    if round(degree,5) > 0:
        for r,v in need_fluxes.items() :
            rxn = model.reactions.get_by_id(r)  
            all_mets = [m.id for m in rxn.metabolites]
            mets = model.metabolites.get_by_id(all_mets[0])
            # if len(all_mets) == 1 and metId not in all_mets and 'S' in mets.elements.keys():
            #     if (rxn.reactants and v < 0) or (rxn.products and v > 0):
            #         s_met_degree += (abs(round(v,5)) * reduced_degree(model, all_mets[0]))
            # if len(all_mets) == 1 and metId not in all_mets and 'N' in mets.elements.keys():
            #     if (rxn.reactants and v < 0) or (rxn.products and v > 0):
            #         N_met_degree += (abs(round(v,5)) * reduced_degree(model, all_mets[0]))
            # if len(all_mets) == 1 and metId not in all_mets and 'C' in mets.elements.keys():
            #     if (rxn.reactants and v < 0) or (rxn.products and v > 0):
            #         c_met_degree += (abs(round(v,5)) * reduced_degree(model, all_mets[0]))
            if len(all_mets) == 1 and metId not in all_mets:
                if mets.id not in O2 and mets.name not in O2_NAME:
                    for k in ['S','C','H','O','P']:
                        if k in mets.elements.keys():
                            met_degree += (-(round(v,5)) * reduced_degree(model, all_mets[0]))
                            # print(rxn,rxn.check_mass_balance(),(round(v,5)),reduced_degree(model, all_mets[0]),met_degree,mets.elements.keys(),sep='  ')
                            break
        max_rate = (met_degree)/abs(degree)
        # max_rate = (s_met_degree + N_met_degree + c_met_degree)/abs(degree)
        # print(max_rate,met_degree,degree)
    elif round(degree,5) < 0:
        max_rate = 0
        temp = [f"The reduction degree of {metId} is {round(degree,5)}, There may be issues with the charge or formula of this substance: {metId}"]
    else:
        max_rate = 0
    return max_rate, temp

def get_biomass_adp_coefficient(model, model_info):
    """"""
    initial_rxn_id = model_info["initial_rxn"]["biomass_rxn_id"]
    if initial_rxn_id:
        rxns = model.reactions.get_by_id(initial_rxn_id)
        for met in rxns.metabolites:
            if met.name in ADP_NAME:
                adp_met = met.id
        atp_coefficient = rxns.metabolites[model.metabolites.get_by_id(adp_met)]
        model_info["initial_rxn"]["adp_coefficient"] = atp_coefficient

def find_autotrophic_and_carbon_source(model_info, model):
    """"""
    for rxn in model_info["reactions"]:
        rxns = model.reactions.get_by_id(rxn['id'])
        if rxn["id"] in model_info["exchange_rxns"]:
            if (rxn['reactants_mets'] and rxn["bounds"][0] <= 0) or (rxn['products_mets'] and rxn['bounds'][1] >= 0):
                r_met_name = rxn["all_mets"][0] 
                r_met = list(rxns.metabolites.keys())[0]
                if any(r_met.id.startswith(source_name) for source_name in AUTOTROPHIC_SOURCE) or str(r_met.formula) == 'Z' or r_met_name in PHOTON_NAME:
                    all_rea = [k.id for k in model.metabolites.get_by_id(r_met.id).reactions] # 只参与了交换反应和转运反应就不算是自养
                    if len(set(all_rea) & (set(model_info["all_rxn_id"])-set(model_info["exchange_rxns"])-set(model_info["transport_rxns"]))) != 0:
                        rxn["autotrophic"] = "true"
                if re.search("C[A-Z]",str(r_met.formula)) or re.search("C[\d]",str(r_met.formula)) or r_met_name in C_LIST: # C后边是大写字母或者数字，或者包含X or str(r_met.formula).find('R') != -1 or str(r_met.formula).find('X') != -1 or str(r_met.formula) == 'null'
                    if r_met_name not in CO2_NAME and r_met_name not in (HCO3_NAME + H2CO3_NAME) and str(r_met.formula) != 'X': # formula不为X
                        rxn["carbon_source"] = "true"
                        # print(rxn["id"],r_met.formula,r_met.name,'xxxxxxx')
                 
            
def set_no2_no3_bounds(model_info, model):
    """"""
    counter = 0
    for rxn in model_info["reactions"]:
        if rxn["id"] in model_info["exchange_rxns"]:
            r_met_name = rxn["all_mets"][0] 
            if r_met_name in NO3_NAME or r_met_name in NO2_NAME:
                counter += 1
    if counter == 2:
        for rxn in model_info["reactions"]:
            rxns = model.reactions.get_by_id(rxn['id'])
            if rxn["id"] in model_info["exchange_rxns"]:
                r_met_name = rxn["all_mets"][0] 
                if r_met_name in NO2_NAME:
                    rxns.bounds = (0,1000)
                    



def is_autotrophic(model_info):
    """"""
    for rxn in model_info["reactions"]:
        if 'autotrophic' in rxn.keys(): 
            return True
    return False



def find_other_carbon_source(model_info, model):
    """"""
    carbon_rxnId, carbon_met = '', ['sucrose','maltose','starch','xylose','glycrole','glycerol'] # 蔗糖、麦芽糖、淀粉、木糖、甘油
    for carbon_met_name in carbon_met:
        for rxn in model_info["reactions"]:
            if rxn['id'] in model_info['exchange_rxns'] and carbon_met_name == rxn['all_mets'][0].lower():
                carbon_rxnId = rxn['id']
                break
        if carbon_rxnId:
            break
    if carbon_rxnId:
        return carbon_rxnId
    for num in [6,5,3,2]:
        for rxns in model.reactions:
            if rxns.id in model_info['exchange_rxns']:
                met = [met for met in rxns.metabolites][0]
                if len(set(met.elements.keys()) & set((['C','H','O']))) == 3 and met.elements['C'] == num:
                    carbon_rxnId = rxns.id
                    break 
        if carbon_rxnId:
            break
    return carbon_rxnId

def normalize_all_rxn_bounds(model_info, model):
    """change the reaction boundary outside the model exchange reaction to (-1000, 1000) within this range"""
    for rxn in model_info["reactions"]:
        rxns = model.reactions.get_by_id(rxn['id'])
        if rxn["bounds"][0] < 0 and rxn["bounds"][1] > 0:
            rxns.bounds = (-1000,1000)
            rxn["bounds"] = [-1000,1000]
        if rxn["bounds"][0] >= 0 and rxn["bounds"][1] > 0:
            rxns.bounds = (0,1000)
            rxn["bounds"] = [0,1000]
        if rxn["bounds"][0] < 0 and rxn["bounds"][1] <= 0:
            rxns.bounds = (-1000,0)
            rxn["bounds"] = [-1000,0]
            
    
                     

def close_autotrophic_or_c_source(model_info, model, flag):
    """Set no autotrophic or C source supply"""
    for rxn in model_info["reactions"]:
        for rxnId in model_info["min_set"]:
            if rxn['id'] == rxnId:
                rxns = model.reactions.get_by_id(rxnId)
                if rxns.reactants:
                    rxns.bounds = (0,1000)
                    rxn["bounds"] = [0,1000]
                if rxns.products:
                    rxns.bounds = (-1000,0)
                    rxn["bounds"] = [-1000,0] 
    for rxn in model_info["reactions"]:
        if "autotrophic" in rxn.keys():
            rxns = model.reactions.get_by_id(rxn['id'])
            if rxns.reactants:
                rxns.bounds = (0,1000)
                rxn["bounds"] = [0,1000]
            if rxns.products:
                rxns.bounds = (-1000,0)
                rxn["bounds"] = [-1000,0] 
        # if rxns.reactants and rxn["bounds"][0] < 0:
        #     model.reactions.get_by_id(rxn['id']).bounds = (0,1000)
        #     rxn["bounds"] = [0,1000]
        # if rxn['products_mets'] and rxn['bounds'][1] > 0:
        #     model.reactions.get_by_id(rxn['id']).bounds = (-1000,0)
        #     rxn["bounds"] = [-1000,0]           



def del_bio_boundary(model_info, model, model_control_info):
    """"""
    initial_rxn_id = model_info["initial_rxn"]["biomass_rxn_id"]
    if initial_rxn_id:
        initial_bio_rxn = model.reactions.get_by_id(initial_rxn_id)
        if initial_bio_rxn.lower_bound != 0:
            model_control_info['boundary_information']["score"] = 0
        if initial_bio_rxn.bounds != (0,1000):  
            model_info['biomass_boundary'] = f"The initial biomass [{initial_rxn_id}] boundary is {initial_bio_rxn.bounds}, changed to (0, 1000)"
            # initial_bio_rxn.bounds = (0,1000)
            model_info['need_set_bio'][initial_rxn_id] = (0,1000)
            model_info['modify_rxn'].append(initial_rxn_id)
        else:
            model_info['biomass_boundary'] = f"The initial biomass [{initial_rxn_id}] boundary is (0, 1000),is ok"

def set_single_carbon(model_info, model):
    """"""
    glucose_rxnId = model_info['glucose_rxnId']
    if glucose_rxnId:
        model_info['need_set_carbon_source'][glucose_rxnId] = (-10,1000)
        # model_info['carbon_source_supply'].extend([f"glucose present,Use glucose({glucose_rxnId}) as the carbon source"])
        min_set = glucose_rxnId
    else:
        carbon_rxnId = find_other_carbon_source(model_info, model)
        model_info['need_set_carbon_source'][carbon_rxnId] = (-10,1000)
        # model_info['carbon_source_supply'].extend([f"There is no glucose,Use {carbon_rxnId} as the carbon source"])
        min_set = carbon_rxnId
    model_info['min_carbon_source_set'] = list(model_info['need_set_carbon_source'].keys())
    model_info["min_set"] = [min_set]
    print('单碳碳源:', model_info["min_set"])

def get_lower_bound(model, check_model, ids):
    """"""
    rxns = model.reactions.get_by_id(ids)
    bounds = check_model.reactions.get_by_id(ids).bounds
    print(ids,bounds,'................sssssss')
    if rxns.lower_bound == 0 or rxns.lower_bound < -100:
        return (-10,1000)
    else:
        return bounds

def del_model_boundary(model_info, model, check_model, model_control_info):
    """"""
    carbon_source_rxn, carbon_source_rxn2, num, min_set, flag = [], [], 0, [], 0
    model_info['carbon_source_supply'], model_info['biomass_boundary'], model_info['pre_modify_bounds'], model_info['need_set_carbon_source'], model_info['need_set_bio'], model_info['modify_rxn'], min_set_all, supply_carbon_source = [], [], [], {}, {}, [], [], []
    del_bio_boundary(model_info, model, model_control_info)
    # normalize_all_rxn_bounds(model_info, model)
    find_autotrophic_and_carbon_source(model_info, model) # 获取自养、异养碳源
    get_carbon_mets(model_info, model) # 获取碳源交换反应的代谢物
    is_auto_build(model_info, model) # 判断是否是自动构建的模型
    for rxn in model_info["reactions"]:
        if 'carbon_source' in rxn.keys():
            if (rxn['reactants_mets'] and rxn["bounds"][0] < 0) or (rxn['products_mets'] and rxn['bounds'][1] > 0):
                supply_carbon_source.append(rxn['id'])
    model_info['carbon_source_supply'] = [f"The initial carbon source set in this model was  : {supply_carbon_source}\n"]
    if model_info["automatic_build"]: # 当模型为自动构建的模型时，就不用找最小碳源集，直接将葡萄糖等单碳作为碳源即可，在后续进行gap，添加必要的途径
        print('automatic_build:',model.slim_optimize(),'........................................111.......................')
        set_single_carbon(model_info, model) # 设置单碳作为最小碳源
    else:
        for rxn in model_info["reactions"]:
            if 'carbon_source' in rxn.keys():
                carbon_source_rxn.append(rxn['id'])
                rxns = model.reactions.get_by_id(rxn['id'])   
                r_met = list(rxns.metabolites.keys())[0]
                if rxns.bounds != (-1000,1000) and str(r_met.formula) != 'null':
                    num += 1
        glucose_rxnId = model_info['glucose_rxnId']
        if num == 0: # 当所有碳源都是（-1000，1000）时，选择单碳作为碳源即可
            model_info['carbon_source_supply'].extend(["Wrong initial model bounds, all carbon source bounds are (-1000, 1000)"])
            model_control_info['boundary_information']["score"] = 0
            set_single_carbon(model_info, model) # 设置单碳作为最小碳源
        elif len(supply_carbon_source)==1 and model.slim_optimize()>1e-6:
            model_info['need_set_carbon_source'][supply_carbon_source[0]] = check_model.reactions.get_by_id(supply_carbon_source[0]).bounds
            model_info["min_set"] = [supply_carbon_source[0]]
            print('存在单一供给碳源且能生长:', model_info["min_set"],model.slim_optimize())
        else:  
            min_set_dict = get_min_carbon_source_set(model_info, model, check_model, carbon_source_rxn, flag)
            if min_set_dict:
                for k,v in min_set_dict.items():
                    min_set_key = k
                    min_set_all = v
                model_info['min_carbon_source_set'] = min_set_all
                print('min_set_all', min_set_dict)
                if min_set_all:
                    if 'min_set' == min_set_key: # 这是第一步逐一打开获取到的列表，在列表中任取一个作为最小碳源都可以满足生长，先找葡萄糖、蔗糖等，没有就任选一个作为碳源
                        if glucose_rxnId in min_set_all:
                            model_info['need_set_carbon_source'][glucose_rxnId] = get_lower_bound(model, check_model, glucose_rxnId)
                            min_set = glucose_rxnId
                        else:
                            carbon_rxnId = find_other_carbon_source(model_info, model)
                            min_set = carbon_rxnId if carbon_rxnId in min_set_all else min_set_all[0]  
                            model_info['need_set_carbon_source'][min_set] = get_lower_bound(model, check_model, carbon_rxnId)
                        # model_info['need_set_carbon_source'][min_set_all] = get_lower_bound(model, check_model, min_set_all)
                        # min_set = min_set_all
                    elif 'min_set1' == min_set_key: # 第二步的列表，其中包含多个子列表，每个子列表都是一对碳源，任选一对碳源打开都可以满足生长
                        min_set = min_set_all[0]
                        for rxnId in min_set:
                            model_info['need_set_carbon_source'][rxnId] = get_lower_bound(model, check_model, rxnId)
                    else: # 第三步得到的列表，其中所有物质都需要打开作为最小碳源集
                        min_set = min_set_all
                        print(min_set_all,'..................')
                        for rxnId in min_set_all:
                            model_info['need_set_carbon_source'][rxnId] = get_lower_bound(model, check_model, rxnId)
                if type(min_set) == str:
                    model_info["min_set"] = [min_set]
                else:
                    model_info["min_set"] = min_set
            else:
                model_info["min_set"] = []
    # for rxn in model_info["reactions"]:    
    #     rxns = model.reactions.get_by_id(rxn['id'])
    #     if "carbon_source" in rxn.keys() and rxn['id'] not in model_info["min_set"]:
    #         if rxns.reactants:
    #             rxn['bounds'] = (0,1000) # 在 model_info中同步此时的边界
    #         if rxns.products:
    #             rxn['bounds'] = (-1000,0)
    #         if rxns.lower_bound < -100:      
    #             carbon_source_rxn2.append(rxn['id'])
    #             model_control_info['boundary_information']["score"] = 0
    #         close_carbon_source_rxn(model, rxn['id']) # 除了最小碳源集以外的其他碳源直接关闭，以后关闭或者打开只处理最小碳源集
    # other_carbon_source = [rxn['id'] for rxn in model_info["reactions"] if 'carbon_source' in rxn.keys() and rxn['id'] not in model_info['min_set']]
    if len(supply_carbon_source) == 1:
        model_info['carbon_source_supply'].extend([f"The ({model_info['min_set']}) was used as minimum carbon source set"])
    else:
        model_info['carbon_source_supply'].extend([f"The ({model_info['min_set']}) was used as minimum carbon source set and turn off other carbon sources"])
    # if carbon_source_rxn2:
    #     model_info['carbon_source_supply'].extend([f"\n({carbon_source_rxn2}) carbon sources boundary is less than -100"])          
    # else:
    #     model_info['carbon_source_supply'].extend([f"\nThe initial model boundary is correct, carbon sources boundary is not less than -100"])
    

def close_carbon_source_rxn(model, rxnId):
    """"""
    rxns = model.reactions.get_by_id(rxnId)
    if rxns.reactants:
        rxns.bounds = (0,1000)
    if rxns.products:
        rxns.bounds = (-1000,0)

def open_carbon_source_rxn(model, rxnId):
    """"""
    rxns = model.reactions.get_by_id(rxnId)
    if rxns.reactants:
        rxns.bounds = (-10,1000)
    if rxns.products:
        rxns.bounds = (-1000,10)

def get_min_carbon_source_set(model_info, model, check_model, carbon_source_rxn, flag):
    """"""
    flag += 1
    if flag > 5:
        return {}
    min_set, temp, min_set1, min_set2, min_set3, min_set_dict, num = [], [], [], [], [], {}, 1e-4
    glucose_rxnId = model_info['glucose_rxnId']
    with model:
        # 第一步，全部关闭后逐一打开
        for rxnId in carbon_source_rxn:
            close_carbon_source_rxn(model, rxnId)
  
        for rxnId in carbon_source_rxn:
            open_carbon_source_rxn(model, rxnId)
            if model.slim_optimize() > num: 
                num = model.slim_optimize()
                min_set.append(rxnId)
            close_carbon_source_rxn(model, rxnId)
        print('min_set:',min_set,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) 
        num = 1e-4
        if min_set:
            min_set_dict['min_set'] = min_set
            return min_set_dict
        else:
            # 第二步，全部关闭的情况下，两两打开
            temp_flag = 0
            for id1 in carbon_source_rxn:
                open_carbon_source_rxn(model, id1)
                for id2 in carbon_source_rxn:
                    open_carbon_source_rxn(model, id2)
                    if (id1 == glucose_rxnId or id2 == glucose_rxnId) and model.slim_optimize() > 1e-4:
                        min_set1 = []
                        min_set1.append([id1,id2])
                        temp_flag = 1
                        break 
                    if model.slim_optimize() > num: 
                        num = model.slim_optimize()  
                        temp.append(id1)
                        temp.append(id2)
                        if temp:
                            min_set1 = []
                            min_set1.append(temp)
                            temp = []
                    close_carbon_source_rxn(model, id2)
                close_carbon_source_rxn(model, id1)
                if temp_flag == 1:
                    break 
            temp = []
            print('min_set1:',min_set1,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            if min_set1:
                min_set_dict['min_set1'] = min_set1
                return min_set_dict
            else:
                # 第三步，全部打开的情况下，逐一关闭
                for rxnId in carbon_source_rxn:
                    open_carbon_source_rxn(model, rxnId)
                temp_biomass_rxn_flux = model.slim_optimize()
                    # model.reactions.get_by_id(rxnId).bounds = check_model.reactions.get_by_id(rxnId).bounds
                for rxnId in carbon_source_rxn:
                    close_carbon_source_rxn(model, rxnId)
                    if model.slim_optimize() < 0.1 * temp_biomass_rxn_flux:  
                        print(model.slim_optimize(),temp_biomass_rxn_flux,rxnId,'.......')
                        min_set2.append(rxnId)
                        open_carbon_source_rxn(model, rxnId)
                    # model.reactions.get_by_id(rxnId).bounds = check_model.reactions.get_by_id(rxnId).bounds
                print('min_set2:',min_set2,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                # 验证第三步得到的碳源集：先全部关闭，然后打开第三步的碳源集，能生长就作为最小碳源集；否则打开它们然后从碳源集里移除，把除了它们以外的碳源底物集合作为集合，
                # 再跑一遍最小碳源集的程序，在这个基础上第二次找出最小碳源集，与第一次的加和；得到新的碳源集，再测试一下生长，如果不能长，同样把第一轮和第二轮的碳源都打开，直到能生长为止
                for rxnId in carbon_source_rxn:
                    close_carbon_source_rxn(model, rxnId)

                if min_set2:
                    min_set3.extend(min_set2)
                    for rxnId in min_set2:
                        open_carbon_source_rxn(model, rxnId)
                    print(model.slim_optimize(),'.....................',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    if model.slim_optimize() > 1e-4: 
                        min_set_dict['min_set3'] = min_set3
                        return min_set_dict
                    else:
                        for rxnId in min_set2:
                            open_carbon_source_rxn(model, rxnId)
                            carbon_source_rxn.remove(rxnId)
                        print('carbon_source_rxn:',carbon_source_rxn,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        temp = get_min_carbon_source_set(model_info, model, check_model, carbon_source_rxn, flag)
                        print('temp:',temp,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        print('min_set3:',min_set3,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        if temp:
                            if type(temp) == dict:
                                for k,v in temp.items():
                                    if type(v[0]) == list:
                                        min_set3.extend(v[0])
                                    else:
                                        min_set3.extend(v)
                                min_set_dict['min_set3'] = min_set3
                            else:
                                min_set3.extend(temp)
                                min_set_dict['min_set3'] = min_set3
                            return min_set_dict
    

            # min_set = min_set1 if (len(min_set2) >= 2 or len(min_set2) == 0) and min_set1 else min_set2
            # return min_set
    # return min_set
    
def get_not_carbon_source_limiting_metabolites(model_info, model, check_model):
    """"""
    limit_rxn,limit_rxn2, model_info["limiting_metabolites"] = {},{}, {}
    if model.slim_optimize() > 0:
        pfba_solution = pfba(model)
        pfba_rxns = pfba_solution.fluxes[abs(pfba_solution.fluxes)>1e-6] 
    else:
        pfba_rxns = {}
    with model:
        for ids,v in pfba_rxns.items():
            rxns = model.reactions.get_by_id(ids)
            if len(rxns.metabolites) == 1:
                for rxn in model_info["reactions"]:
                    if ids == rxn['id']:
                        # rxns = model.reactions.get_by_id(rxn['id'])
                        # print(ids,v,rxns.bounds,'pfba_rxns')
                        if 'carbon_source' not in rxn.keys() and v == rxns.lower_bound and v > -1000:  
                            limit_rxn2[ids] = v
                            rxns.lower_bound = -1000
                            if model.slim_optimize() > 0:
                                model_info["limiting_metabolites"] = limit_rxn2
                                pfba_solution = pfba(model)
                                need_fluxes = pfba_solution.fluxes[abs(pfba_solution.fluxes)>1e-6] 
                                limit_rxn[rxn['id']] = round(need_fluxes[rxn['id']],3)
                            rxns.lower_bound = check_model.reactions.get_by_id(ids).lower_bound
    if limit_rxn:
        temp = f"The supply of non-carbon-source substances {limit_rxn.keys()} was limited. The lower bound of {limit_rxn.keys()} in the initial model was {limit_rxn2}, when the lower bound was set to -1000, the calculated uptake rate was {limit_rxn}"
    else:
        temp = "No non-carbon source limiting metabolites detected"
    return temp




def set_bio_boundary(model_info, model):
    """"""
    if model_info['need_set_bio']:
        for rxnId, rxn_bounds in model_info['need_set_bio'].items():
            for rxn in model_info["reactions"]:
                if rxnId == rxn['id']:
                    rxns = model.reactions.get_by_id(rxnId)
                    rxns.bounds = rxn_bounds
                        

def get_c_source_supply(model_info, model):
    """"""
    model_info['need_set_carbon_mets'] = []
    for rxnId in model_info['need_set_carbon_source'].keys():
        model_info['modify_rxn'].append(rxnId)
        for rxn in model_info["reactions"]:
            if rxnId == rxn['id']:
                rxns = model.reactions.get_by_id(rxnId)
                r_met = list(rxns.metabolites.keys())[0]
                model_info['need_set_carbon_mets'].append(r_met.id)

def close_all_carbon(model_info, model, model_control_info):
    """"""
    carbon_source_rxn = []
    for rxn in model_info["reactions"]:    
        rxns = model.reactions.get_by_id(rxn['id'])
        if "carbon_source" in rxn.keys() and rxn['id'] not in model_info["min_set"]:
            if rxns.reactants:
                rxn['bounds'] = (0,1000) # 在 model_info中同步此时的边界
            if rxns.products:
                rxn['bounds'] = (-1000,0)
            if rxns.lower_bound < -100:      
                carbon_source_rxn.append(rxn['id'])
                model_control_info['boundary_information']["score"] = 0
            close_carbon_source_rxn(model, rxn['id']) # 除了最小碳源集以外的其他碳源直接关闭，以后关闭或者打开只处理最小碳源集
    if carbon_source_rxn:
        model_info['carbon_source_supply'].extend([f"\n({carbon_source_rxn}) carbon sources boundary is less than -100"])          
    else:
        model_info['carbon_source_supply'].extend([f"\nThe initial model boundary is correct, carbon sources boundary is not less than -100"])

def get_proportion_c(model_info, model):
    """"""
    total_proportion = 0
    if model.slim_optimize() > 0:
        pfba_solution = pfba(model)
        need_fluxes = pfba_solution.fluxes[abs(pfba_solution.fluxes)>1e-6] 
    else:
        need_fluxes = {}
    for r,v in need_fluxes.items():
        for rxnId in model_info["min_set"]:
            if r == rxnId:
                print(r,v,rxnId,'....get_proportion_c.....')
                total_proportion += abs(v)
    return total_proportion, need_fluxes

def get_flux(need_fluxes, rxnId):
    """"""
    for r,v in need_fluxes.items():
        if r == rxnId:
            return abs(v)
        
def get_carbon_proportion(model_info, model, check_model, model_control_info):
    """"""
    model_info["carbon_source_boundary_dict"] = {}
    if model_info["automatic_build"] or len(model_info["min_set"]) == 1:
        close_all_carbon(model_info, model, model_control_info)
    else:
        for rxnId in model_info["min_set"]:
            for rxn in model_info["reactions"]:
                if rxnId == rxn['id']:
                    rxns = model.reactions.get_by_id(rxnId)
                    met = [met for met in rxns.metabolites][0] 
                    bounds = check_model.reactions.get_by_id(rxnId).bounds
                    if rxns.reactants:
                        if -100 <= rxns.lower_bound < 0 and -100 <= bounds[0] < 0:
                            rxns.bounds = bounds
                        else:
                            rxns.bounds = (-10,1000)
                    if rxns.products:
                        if 0 < rxns.upper_bound <= 100 and 0 < bounds[1] <= 100:
                            rxns.bounds = bounds
                        else:
                            rxns.bounds = (-1000,10)
        close_all_carbon(model_info, model, model_control_info) # 先按照最小碳源设置供给量，然后关闭其他所有碳源，再来寻找比例
        total_proportion, need_fluxes = get_proportion_c(model_info, model) # pfba计算，获取结果中所有最小碳源集通量的和
        for rxnId in model_info["min_set"]:
            for rxn in model_info["reactions"]:
                if rxnId == rxn['id']:
                    rxns = model.reactions.get_by_id(rxnId)
                    met = [met for met in rxns.metabolites][0] 
                    rxn_flux = get_flux(need_fluxes, rxnId) # 获取当前碳源在结果中的通量
                    met_proportion = eval(format(rxn_flux / total_proportion, '.3e')) # 根据通量比值，获取当前碳源在所有碳源里的比例
                    met_c = eval(format((60 * met_proportion), '.3e')) # 一共供给60个碳，乘以相应的比例，可以得到当前碳源应该分到的碳的个数
                    print(rxnId,met,met.formula,met.elements)
                    c_supply = eval(format(met_c / met.elements['C'], '.3e')) # 当前碳源应该分到的碳的个数除以C的个数得到供给量
                    if rxns.reactants:
                        bounds = (-c_supply,1000)
                    if rxns.products:
                        bounds = (-1000,c_supply)
                    model_info["carbon_source_boundary_dict"][rxnId] = bounds
                    

def set_c_source_supply(model_info, model, flag, check_model):
    """"""
    model_info["carbon_source_boundary"] = []
    if model_info["automatic_build"] or len(model_info["min_set"]) == 1:
        for rxnId in model_info["min_set"]:
            for rxn in model_info["reactions"]:
                if rxnId == rxn['id']:
                    rxns = model.reactions.get_by_id(rxnId)
                    met = [met for met in rxns.metabolites][0]
                    c_supply = round(60 / met.elements['C'])
                    if rxns.reactants:
                        rxns.bounds = (-c_supply,1000)
                    if rxns.products:
                        rxns.bounds = (-1000,c_supply)
                    if flag == 'yields' or flag == 'bio':
                        rxn['bounds'] = rxns.bounds
                    model_info["carbon_source_boundary"].append(f"{rxnId} : {rxns.bounds}")
    else:
        for rxnId, bounds in model_info["carbon_source_boundary_dict"].items():
            for rxn in model_info["reactions"]:
                if rxnId == rxn['id']:
                    model.reactions.get_by_id(rxnId).bounds = bounds
                    if flag == 'yields' or flag == 'bio':
                        rxn['bounds'] = bounds
                    model_info["carbon_source_boundary"].append(f"{rxnId} : {bounds}")
    # print(model_info["carbon_source_boundary"])

def get_carbon_mets(model_info, model):
    """"""
    model_info['need_set_carbon_mets'] = []
    for rxn in model_info["reactions"]:
        if 'carbon_source' in rxn.keys():
            rxns = model.reactions.get_by_id(rxn['id'])   
            r_met = list(rxns.metabolites.keys())[0]
            model_info['need_set_carbon_mets'].append(r_met.id)

def is_auto_build(model_info, model):
    """"""
    num, total = 0, 0
    for rxns in model.reactions:
        for rxn in model_info["reactions"]:
            if rxns.id == rxn['id'] and 'carbon_source' in rxn.keys():
                print('所有碳源',rxns,rxns.bounds)
                total += 1
                if rxns.bounds == (-1000,1000) or rxns.bounds == (-10000,10000):
                    num += 1
    print(num,total,',,,,,,,,,,,,')
    try:
        if (num/total) >= 0.7:
            model_info["automatic_build"] = 1
        else:
            model_info["automatic_build"] = 0
    except ZeroDivisionError:
        model_info["automatic_build"] = 0
  
def is_exist_respiratory_chain(model_info, rea, rea2, pro):
    """
    "4.0 H+ + Menaquinol 7 C46H66O2 + 0.5 O2 O2 --> H2O H2O + 4.0 H+ + Menaquinone 7 C46H64O2"
    """
    for rxn in model_info['reactions']:
        if len(set(rea) & set(rxn['reactants_mets'])) != 0 and len(set(rea2) & set(rxn['reactants_mets'])) != 0 and len(set(pro) & set(rxn['products_mets'])) != 0:
            return 1
        if len(set(rea) & set(rxn['products_mets'])) != 0 and len(set(rea2) & set(rxn['reactants_mets'])) != 0 and len(set(pro) & set(rxn['reactants_mets'])) != 0:
            return 1


def add_respiratory_chain(model_info, model, check_model):
    """"""
    if is_exist_respiratory_chain(model_info, O2_NAME , Q8H2_SAME, Q8_SAME) or is_exist_respiratory_chain(model_info, NADH_NAME , Q8_SAME, Q8H2_SAME):
        if not model_info["chain_rxn"]:
            mets = [met.id for met in model.metabolites]
            if model_info["model_identifier"] == "modelseed":
                if 'rxn08173' not in model.reactions and 'rxn10042' not in model.reactions:
                    if len(set(['cpd00008_c0','cpd00009_c0','cpd00067_c0','cpd00001_c0','cpd00002_c0','cpd00067_e0']) & set(mets)) == 6:
                        reaction = Reaction('add_ATPS4_e') #添加rxn08173
                        model.add_reactions([reaction])
                        check_model.add_reactions([reaction])        
                        reaction.build_reaction_from_string('cpd00008_c0 + cpd00009_c0 + 4.0 cpd00067_e0 --> cpd00001_c0 + cpd00002_c0 + 3.0 cpd00067_c0')
                        model_info['modify_rxn'].append('add_ATPS4_e')
                        model_info["h_close"].append('cpd00067_e0')
                        model_info["special_boundary_reaction"].extend([f"The model lacks 'add_ATPS4_e' respiratory chain reaction, add it to the model"])
                    if len(set(['cpd00008_c0','cpd00009_c0','cpd00067_c0','cpd00001_c0','cpd00002_c0','cpd00067_p0']) & set(mets)) == 6:
                        reaction = Reaction('add_ATPS4rpp_p') #添加NOG
                        model.add_reactions([reaction])
                        check_model.add_reactions([reaction])        
                        reaction.build_reaction_from_string('cpd00008_c0 + cpd00009_c0 + 4.0 cpd00067_p0 --> cpd00001_c0 + cpd00002_c0 + 3.0 cpd00067_c0')
                        model_info['modify_rxn'].append('add_ATPS4rpp_p')
                        model_info["h_close"].append('cpd00067_p0')
                        model_info["special_boundary_reaction"].extend([f"The model lacks 'add_ATPS4rpp_p' respiratory chain reaction, add it to the model"])
            elif model_info["model_identifier"] == "virtual":
                if len(set(['adp[c]','h[e]','pi[c]','atp[c]','h2o[c]','h[c]']) & set(mets)) == 6:
                    reaction = Reaction('add_ATPS4_e') #添加add_ATPS4
                    model.add_reactions([reaction])
                    check_model.add_reactions([reaction])        
                    reaction.build_reaction_from_string('adp[c] + 4.0 h[e] + pi[c] --> atp[c] + h2o[c] + 3.0 h[c]')
                    model_info['modify_rxn'].append('add_ATPS4_e')
                    model_info["h_close"].append('h[e]')
                    model_info["special_boundary_reaction"].extend([f"The model lacks 'add_ATPS4_e' respiratory chain reaction, add it to the model"])
                if len(set(['adp[c]','h[p]','pi[c]','atp[c]','h2o[c]','h[c]']) & set(mets)) == 6:
                    reaction = Reaction('add_ATPS4rpp_p') #添加NOG
                    model.add_reactions([reaction])
                    check_model.add_reactions([reaction])        
                    reaction.build_reaction_from_string('adp[c] + 4.0 h[p] + pi[c] --> atp[c] + h2o[c] + 3.0 h[c]')
                    model_info['modify_rxn'].append('add_ATPS4rpp_p')
                    model_info["h_close"].append('h[p]')
                    model_info["special_boundary_reaction"].extend([f"The model lacks 'add_ATPS4rpp_p' respiratory chain reaction, add it to the model"])
            else:
                if 'ATPS4' not in model.reactions:
                    if len(set(['adp_c','h_e','pi_c','atp_c','h2o_c','h_c']) & set(mets)) == 6:
                        reaction = Reaction('add_ATPS4_e') #添加ATPS4
                        model.add_reactions([reaction])
                        check_model.add_reactions([reaction])        
                        reaction.build_reaction_from_string('adp_c + 4.0 h_e + pi_c --> atp_c + h2o_c + 3.0 h_c')
                        model_info['modify_rxn'].append('add_ATPS4_e')
                        model_info["h_close"].append('h_e')
                        model_info["special_boundary_reaction"].extend([f"The model lacks 'add_ATPS4_e' respiratory chain reaction, add it to the model"])
                if 'ATPS4rpp' not in model.reactions:
                    if len(set(['adp_c','h_p','pi_c','atp_c','h2o_c','h_c']) & set(mets)) == 6:
                        reaction = Reaction('add_ATPS4rpp_p') #添加NOG
                        model.add_reactions([reaction])
                        check_model.add_reactions([reaction])        
                        reaction.build_reaction_from_string('adp_c + 4.0 h_p + pi_c <=> atp_c + h2o_c + 3.0 h_c')
                        model_info['modify_rxn'].append('add_ATPS4rpp_p')
                        model_info["h_close"].append('h_p')
                        model_info["special_boundary_reaction"].extend([f"The model lacks 'add_ATPS4rpp_p' respiratory chain reaction, add it to the model"])
                    
def use_ATPS4rpp_or_ATPS4(model):
    """如果同时添加了h_e和h_p的呼吸链反应,需要删掉其中一个,计算biomass途径,删掉不在途径里的那一个反应"""
    if 'add_ATPS4_e' in model.reactions and 'add_ATPS4rpp_p' in model.reactions:
        if model.slim_optimize() > 0:
            pfba_solution = pfba(model)
            need_fluxes = pfba_solution.fluxes[abs(pfba_solution.fluxes)>1e-6] 
        else:
            need_fluxes = {}
        if 'add_ATPS4_e' in list(need_fluxes.keys()) and 'add_ATPS4rpp_p' not in list(need_fluxes.keys()):
            model.reactions.remove('add_ATPS4rpp_p')
        if 'add_ATPS4rpp_p' in list(need_fluxes.keys()) and 'add_ATPS4_e' not in list(need_fluxes.keys()):
            model.reactions.remove('add_ATPS4_e')
        


def find_hc_he(model, model_info, rea, rea2, pro):
    """
    "4.0 H+ + Menaquinol 7 C46H66O2 + 0.5 O2 O2 --> H2O H2O + 4.0 H+ + Menaquinone 7 C46H64O2"
    """
    respiratory_chain, h_c, h_e = [], '', ''
    for rxn in model_info['reactions']:
        if len(set(rea) & set(rxn['reactants_mets'])) != 0 and len(set(rea2) & set(rxn['reactants_mets'])) != 0 and len(set(pro) & set(rxn['products_mets'])) != 0:
            rxns = model.reactions.get_by_id(rxn['id'])
            print(rxns)
            h_met = [met.id for met in rxns.metabolites if met.name in H_NAME]
            if len(h_met) == 2:
                h_c = h_met[0]
                h_e = h_met[1]
            if len(h_met) == 1:
                if h_met[0] in H_E:
                    h_e = h_met[0]
                else:
                    h_c = h_met[0]
        if len(set(rea) & set(rxn['products_mets'])) != 0 and len(set(rea2) & set(rxn['reactants_mets'])) != 0 and len(set(pro) & set(rxn['reactants_mets'])) != 0:
            rxns = model.reactions.get_by_id(rxn['id'])
            print(rxns)
            h_met = [met.id for met in rxns.metabolites if met.name in H_NAME]
            if len(h_met) == 2:
                h_c = h_met[1]
                h_e = h_met[0]
            if len(h_met) == 1:
                if h_met[0] in H_E:
                    h_e = h_met[0]
                else:
                    h_c = h_met[0]
    return h_c, h_e


def deprecated_add_respiratory_chain(model_info, model, check_model):
    """
    先找o2和mql7_c/q8h2_c组合生成mqn7_c/q8_c的反应，没有h_e就补上4个，然后找nadh_c和mqn7_c/q8_c生成mql7_c/q8h2_c的反应，没有就在右边补上3个
    carveme:
    CYTB_B3	0.51557	4.0 h_c + mql7_c + 0.5 o2_c --> h2o_c + 4.0 h_e + mqn7_c
    NADH4	0.51557	h_c + mqn7_c + nadh_c --> mql7_c + nad_c   （没有作用）
    virtual：
    CCOuq	28.71359	4.0 h_c + 0.5 o2_c + q8h2_c --> h2o_c + 4.0 h_e + q8_c
    NADH5	28.70798	h_c + nadh_c + q8_c --> nad_c + q8h2_c  （没有作用）
    NADH10	20.39211	h_c + mqn8_c + nadh_c --> mql8_c + nad_c
    最后找ATPS4	34.79409	adp_c + 4.0 h_e + pi_c --> atp_c + h2o_c + 3.0 h_c，没有就补上
    ADP + Phosphate + 4.0 H+ --> H2O + ATP + 3.0 H+     adp_c + 4.0 h_e + pi_c --> atp_c + h2o_c + 3.0 h_c
    """
    respiratory_chain, h_c, h_e = [], '', ''
    rea = O2_NAME + Q8H2_SAME
    h_c, h_e = find_hc_he(model, model_info, O2_NAME , Q8H2_SAME, Q8_SAME)
    print('hc:',h_c,'he:', h_e,'...........')
    if not h_c:
        h_c, b = find_hc_he(model, model_info, NADH_NAME , Q8_SAME, Q8H2_SAME)
    if not h_e:
        a, h_e = find_hc_he(model, model_info, NADH_NAME , Q8_SAME, Q8H2_SAME)
    print('hc:',h_c,'he:',h_e,',,,,,,,,,,')
    for rxn in model_info['reactions']:
        if len(set(O2_NAME) & set(rxn['reactants_mets'])) != 0 and len(set(Q8H2_SAME) & set(rxn['reactants_mets'])) != 0 and len(set(Q8_SAME) & set(rxn['products_mets'])) != 0:
            respiratory_chain.append(rxn['id'])
        if len(set(O2_NAME) & set(rxn['products_mets'])) != 0 and len(set(Q8H2_SAME) & set(rxn['products_mets'])) != 0 and len(set(Q8_SAME) & set(rxn['reactants_mets'])) != 0:
            respiratory_chain.append(rxn['id'])
    for rxn in model.reactions:
        if rxn.id in respiratory_chain:
            if set(O2_NAME) & set([rea.name for rea in rxn.reactants]) != 0:
                h_met = [met.id for met in rxn.products if met.name in H_NAME]
                if len(h_met) == 0:
                    if not h_e and model_info["h_close"]:
                        h_e = model_info["h_close"][0]
                    try:
                        h_met = model.metabolites.get_by_id(h_e)
                        rxn.add_metabolites({h_met:4.0})
                        model_info['modify_rxn'].append(rxn.id)
                        print(rxn.id,rxn)
                    except:
                        break
            else:
                h_met = [met.id for met in rxn.reactants if met.name in H_NAME]
                if len(h_met) == 0:
                    if not h_e and model_info["h_close"]:
                        h_e = model_info["h_close"][0]
                    try:
                        h_met = model.metabolites.get_by_id(h_e)
                        rxn.add_metabolites({h_met:-4.0})
                        model_info['modify_rxn'].append(rxn.id)
                        print(rxn.id,rxn)
                    except:
                        break
    respiratory_chain = []
    for rxn in model_info['reactions']:
        if len(set(NADH_NAME) & set(rxn['reactants_mets'])) != 0 and len(set(Q8_SAME) & set(rxn['reactants_mets'])) != 0 and len(set(Q8H2_SAME) & set(rxn['products_mets'])) != 0:
            respiratory_chain.append(rxn['id'])
        if len(set(NADH_NAME) & set(rxn['products_mets'])) != 0 and len(set(Q8_SAME) & set(rxn['reactants_mets'])) != 0 and len(set(Q8H2_SAME) & set(rxn['reactants_mets'])) != 0:
            respiratory_chain.append(rxn['id'])
    for rxn in model.reactions:
        if rxn.id in respiratory_chain:
            if set(NADH_NAME) & set([rea.name for rea in rxn.reactants]) != 0: # nadh在左边
                h_met = [met.id for met in rxn.products if met.name in H_NAME] # 处理h_e
                if len(h_met) == 0:
                    if not h_e and model_info["h_close"]:
                        h_e = model_info["h_close"][0]
                    try:
                        h_met = model.metabolites.get_by_id(h_e)
                        rxn.add_metabolites({h_met:3.0})
                        model_info['modify_rxn'].append(rxn.id)
                        print(rxn.id,rxn)
                    except:
                        break
                h_met = [met.id for met in rxn.reactants if met.name in H_NAME] # 处理h_c
                if len(h_met) == 0:
                    if not h_c:
                        h_c = model_info["h_c"][0]
                        try:
                            h_met = model.metabolites.get_by_id(h_c)
                            rxn.add_metabolites({h_c : -4.0})
                            model_info['modify_rxn'].append(rxn.id)
                            print(rxn.id,rxn)
                        except:
                            break
                else:
                    h_met = model.metabolites.get_by_id(h_c)
                    rxn.add_metabolites({h_c : -3.0})
                    model_info['modify_rxn'].append(rxn.id)
                    print(rxn.id,rxn)
            else: # nadh在右边
                h_met = [met.id for met in rxn.reactants if met.name in H_NAME] # 处理h_e
                if len(h_met) == 0:
                    if not h_e and model_info["h_close"]:
                        h_e = model_info["h_close"][0]
                    try:
                        h_met = model.metabolites.get_by_id(h_e)
                        rxn.add_metabolites({h_met:-3.0})
                        model_info['modify_rxn'].append(rxn.id)
                        print(rxn.id,rxn)
                    except:
                        break
                h_met = [met.id for met in rxn.reactants if met.name in H_NAME] # 处理h_c
                if len(h_met) == 0:
                    if not h_c:
                        h_c = model_info["h_c"][0]
                        try:
                            h_met = model.metabolites.get_by_id(h_c)
                            rxn.add_metabolites({h_c : 4.0})
                            model_info['modify_rxn'].append(rxn.id)
                            print(rxn.id,rxn)
                        except:
                            break
                else:
                    h_met = model.metabolites.get_by_id(h_c)
                    rxn.add_metabolites({h_c : 3.0})
                    model_info['modify_rxn'].append(rxn.id)
                    print(rxn.id,rxn)
    if not model_info["chain_rxn"]:
        if model_info["model_identifier"] == "modelseed":
            if 'rxn08173' not in model.reactions:
                reaction = Reaction('rxn08173') #添加rxn08173
                model.add_reactions([reaction])
                check_model.add_reactions([reaction])        
                reaction.build_reaction_from_string('cpd00008 + cpd00009 + 4.0 cpd00067 => cpd00001 + cpd00002 + 3.0 cpd00067')
                model_info['modify_rxn'].append('rxn08173')
        elif model_info["model_identifier"] == "virtual":
                reaction = Reaction('add_ATPS4') #添加add_ATPS4
                model.add_reactions([reaction])
                check_model.add_reactions([reaction])        
                reaction.build_reaction_from_string('adp[c] + 4.0 h[e] + pi[c] --> atp[c] + h2o[c] + 3.0 h[c]')
                model_info['modify_rxn'].append('rxn08173')
        else:
            if 'ATPS4' not in model.reactions:
                reaction = Reaction('ATPS4') #添加ATPS4
                model.add_reactions([reaction])
                check_model.add_reactions([reaction])        
                reaction.build_reaction_from_string('adp_c + 4.0 h_e + pi_c --> atp_c + h2o_c + 3.0 h_c')
                model_info['modify_rxn'].append('ATPS4')



def old_set_c_source_supply(model_info, model, flag):
    """"""
    model_info['need_set_carbon_mets'] = []
    # model_info['need_set_carbon_source']里保存的边界已弃用，使用新的方法去设置边界，但碳源的key值还有用
    for rxnId, rxn_bounds in model_info['need_set_carbon_source'].items():
        # print(rxnId,rxn_bounds,'xxxx')
        for rxn in model_info["reactions"]:
            if rxnId == rxn['id']:
                rxns = model.reactions.get_by_id(rxnId)
                r_met = list(rxns.metabolites.keys())[0]
                model_info['need_set_carbon_mets'].append(r_met.id)
                rxns.bounds = rxn_bounds
                rxn['bounds'] = rxn_bounds
                # if flag == 'yields' or flag == 'bio':
                #     rxn['bounds'] = rxn_bounds


def set_auto_source_supply(model_info, model, check_model, flag):                    
    for rxn in model_info["reactions"]:
        if 'autotrophic' in rxn.keys():
            rxns = model.reactions.get_by_id(rxn['id'])
            rxns.bounds = check_model.reactions.get_by_id(rxn['id']).bounds
            if flag == 'yields' or flag == 'bio':
                rxn['bounds'] = rxns.bounds


def del_h2s_fe2(model_info, model, check_model):
    """"""
    flag = 0
    initial_rxn_id = model_info["initial_rxn"]["biomass_rxn_id"]
    if initial_rxn_id:
        for met in model.reactions.get_by_id(initial_rxn_id).reactants:
            if met.name in FE2:
                flag = 1
                break 
    for rxn in model.reactions:
        if len(rxn.metabolites) == 1:
            mets = list(rxn.metabolites.keys())[0]
            if mets.name in H2S_NAME or (mets.name in FE2 and flag == 0):
                local_bounds = check_model.reactions.get_by_id(rxn.id).bounds
                if rxn.bounds != (0,1000):
                    rxn.bounds = (0,1000)
                    print(rxn,mets.id,mets.name,model.slim_optimize(),sep='   ')
                    if model.slim_optimize() > 1e-4:
                        model_info['modify_rxn'].append(rxn.id)
                        model_info["special_boundary_reaction"].extend([f"The initial {rxn.id} boundary is {local_bounds}, changed to {rxn.bounds}"])
                    else:
                        if 'automatic_build' in model_info.keys():
                            rxn.bounds = (-10,1000)
                        else:
                            rxn.bounds = local_bounds

def add_respiratory_chain_rxn(model_info, model, check_model):
    """"""
    count = 0
    for met in model.metabolites:
        if (len(met.id.split("_")[-1]) == 1) and (not met.id.startswith('cpd')):
            count += 1
    if count/len(model.metabolites) > 0.8:
        print(count,len(model.metabolites),'add_respiratory_chain_rxn')
        # if not model_info["chain_rxn"]:
        mets = [met.id for met in model.metabolites]
        if 'ATPS4rpp' not in model.reactions:
            if len(set(['adp_c','h_p','pi_c','atp_c','h2o_c','h_c']) & set(mets)) == 6:
                reaction = Reaction('ATPS4rpp') #添加NOG
                model.add_reactions([reaction])
                check_model.add_reactions([reaction])        
                reaction.build_reaction_from_string('adp_c + 4.0 h_p + pi_c <=> atp_c + h2o_c + 3.0 h_c')
                model_info['modify_rxn'].append('ATPS4rpp')
                model_info["special_boundary_reaction"].extend([f"The model lacks 'ATPS4rpp' respiratory chain reaction, add it to the model"])
        # if 'CYTBO3_4pp' not in model.reactions:
            if len(set(['o2_c','h_p','q8h2_c','q8_c','h2o_c','h_c']) & set(mets)) == 6:
                reaction = Reaction('CYTBO3_4pp') #添加NOG
                model.add_reactions([reaction])
                check_model.add_reactions([reaction])
                reaction.build_reaction_from_string('4.0 h_c + 0.5 o2_c + q8h2_c --> h2o_c + 4.0 h_p + q8_c')
                model_info['modify_rxn'].append('CYTBO3_4pp')
                model_info["special_boundary_reaction"].extend([f"The model lacks 'CYTBO3_4pp' respiratory chain reaction, add it to the model"])
        if 'NADH16pp' not in model.reactions:
            if len(set(['nadh_c','h_p','q8_c','q8h2_c','nad_c','h_c']) & set(mets)) == 6:
                reaction = Reaction('NADH16pp') #添加NOG
                model.add_reactions([reaction])
                check_model.add_reactions([reaction])
                reaction.build_reaction_from_string('4.0 h_c + nadh_c + q8_c --> 3.0 h_p + nad_c + q8h2_c')
                model_info['modify_rxn'].append('NADH16pp')
                model_info["special_boundary_reaction"].extend([f"The model lacks 'NADH16pp' respiratory chain reaction, add it to the model"])
      


def del_h2(model_info, model, check_model):
    """"""
    if 'rxn08734_c0' in model.reactions:
        model.reactions.get_by_id('rxn08734_c0').bounds = (0,0)
        reaction = Reaction('cpd11640_c0') #添加NOG
        model.add_reactions([reaction])
        check_model.add_reactions([reaction])
        reaction.build_reaction_from_string('cpd11640_c0 -->')
        model_info['modify_rxn'].append('cpd11640_c0')
        model_info["special_boundary_reaction"].extend([f"The reaction rxn08734_c0 is not correct. No NADH is needed to generate proton driving force,turn it off and add H2 efflux reaction"])

def close_h2_ppt_tsul(model_info, model):
    """"""
    for rxn in model.reactions:
        if len(rxn.metabolites) == 1:
            mets = list(rxn.metabolites.keys())[0]
            if mets.name in H2_NAME or mets.id in H2:
                rxn.bounds = (0,0)
                model_info['modify_rxn'].append(rxn.id)
                model_info["special_boundary_reaction"].extend([f"Close the input of h2:{rxn}"])
            if mets.name in PPT_NAME or mets.id in PPT:
                rxn.bounds = (0,0)
                model_info['modify_rxn'].append(rxn.id)
                model_info["special_boundary_reaction"].extend([f"Close the input of ppt:{rxn}"])
            if mets.name in TSUL_NAME or mets.id in TSUL:
                rxn.bounds = (0,0)
                model_info['modify_rxn'].append(rxn.id)
                model_info["special_boundary_reaction"].extend([f"Close the input of tsul:{rxn}"])

def set_special_boundary_rxn(model_info, model, check_model):
    """"""
    model_info["special_boundary_reaction"], temp = [], []
    # for rxn in model.reactions:
    #     if rxn.lower_bound > 0 or rxn.upper_bound < 0:
    #         print(rxn,rxn.bounds)
    for rxn in model_info["reactions"]:
        if rxn['bounds'][0] > 0 or rxn['bounds'][1] < 0:
            if rxn['id'] not in ATPM:
                rxn["special_boundary"] = "true"
                temp.append(rxn['id'])
                model_info['modify_rxn'].append(rxn['id']) # 会把一些有问题的边界的反应记录进去：比如ATPM;但是不能给改成0，这样就没有维持能了
    for rxns in model.reactions:
        if rxns.id in temp:
            # model_info["special_boundary_reaction"].extend([f"{rxns.id} : {rxns.bounds}"])
            local_bounds = check_model.reactions.get_by_id(rxns.id).bounds
            if rxns.lower_bound > 0:
                rxns.bounds = (0,1000)
            if rxns.upper_bound < 0:
                rxns.bounds = (-1000,0)
            model_info["special_boundary_reaction"].extend([f"The initial {rxns.id} boundary is {local_bounds}, changed to {rxns.bounds}"])
        if rxns.id in model_info['exchange_rxns']:
            mets = list(rxns.metabolites.keys())[0]
            if 'biomass' in mets.id.lower() or mets.id.lower() in 'biomass' or mets.name in BIOMASS or 'biomass' in mets.name.lower():
                if rxns.bounds != (0,1000):
                    local_bounds = check_model.reactions.get_by_id(rxns.id).bounds
                    rxns.bounds = (0,1000)
                    model_info['modify_rxn'].append(rxns.id)
                    # model_info["special_boundary_reaction"].extend([f"{rxns.id} : {rxns.bounds}"])
                    model_info["special_boundary_reaction"].extend([f"The initial {rxns.id} boundary is {local_bounds}, changed to {rxns.bounds}"])
                else:
                    model_info["special_boundary_reaction"].extend([f"The initial {rxns.id} boundary is {rxns.bounds}"])
    close_h2_ppt_tsul(model_info, model)
    del_h2s_fe2(model_info, model, check_model)
    # add_respiratory_chain_rxn(model_info, model, check_model)
    del_h2(model_info, model, check_model)
    
    
   
       
def set_special_boundary_rxn2(model_info, model):
    """"""
    for rxn in model_info["reactions"]:
        if 'special_boundary' in rxn.keys():
            rxns = model.reactions.get_by_id(rxn['id'])
            if rxns.lower_bound > 0:
                rxns.bounds = (0,1000)
            if rxns.upper_bound < 0:
                rxns.bounds = (-1000,0)
          

def rxn_no_annotation(model_info, model):
    for rxn in model_info['reactions']:
        rxns = model.reactions.get_by_id(rxn["id"])
        if rxns.annotation == []:
            rxn["annotation"] = "false"
        elif len(rxns.annotation) == 1 and  'MetaNetX (MNX) Equation' in str(rxns.annotation): 
            rxn["annotation"] = "true"
        else:
            rxn["annotation"] = "true"


def run_rules(rules, model_info, model):
    """在gap添加了新反应后,把规则再跑一次"""
    rules.get_all_rules(model_info, model)
    check_rxn_balance(model_info, model)
    check_C_balance(model_info, model)
    net_penalty_points(model_info)

def check_rxn_balance(model_info, model): 
    """
    Check if the reaction is balanced
    """ 
    for rxn in model_info['reactions']:
        if rxn['id'] not in model_info['exchange_rxns']:
            # check is a dictionary, calculate the mass and charge balance of the reaction, for a balanced reaction, this should be empty
            rxns = model.reactions.get_by_id(rxn['id'])
            check = rxns.check_mass_balance()
            if len(check) != 0:
                # Elemental balance, charge nan  {'charge': nan}
                if 'charge' in check.keys() and len(check) == 1 and math.isnan(check['charge']):
                    rxn["balance"] = "true"
                # {'charge': 1.0, 'H': 1.0}，The number of charge and the number of hydrogen are the same and have the same sign, the reaction is considered to be correct, and no manual inspection is performed
                elif  "'H': " in str(check) and "'charge': " in str(check) and len(check) == 2 and check['charge'] == check['H'] and check['charge'] * check['H'] >=0:
                    rxn["balance"] = "true"
                # h2o，and the same sign, this response is considered correct
                elif "'H': " in str(check) and "'O': " in str(check) and len(check) == 2 and abs(check['O']) == 1 and abs(check['H']) == 2 and check['O'] * check['H'] >=0:
                    rxn["balance"] = "true"
                elif not [k for k,v in rxns.check_mass_balance().items() if round(v,3) != 0]:
                    rxn["balance"] = "true"
                elif [k.id for k,v in rxns.metabolites.items() if not k.formula]:
                    rxn["balance"] = "true"
                else:
                    rxn["balance"] = "false"
            else:
                rxn["balance"] = "true"
        else:
            rxn["balance"] = ""


def check_C_balance(model_info, model): 
    """
    Check if the reaction is carbon balanced
    """ 
    for rxn in model_info['reactions']:
        if rxn['id'] not in model_info['exchange_rxns']:
            rxns = model.reactions.get_by_id(rxn['id'])
            check = rxns.check_mass_balance()
            if len(check) != 0 and ('C' in check.keys() and round(check['C'],3) != 0):
                # The element contains C, that is, carbon is not conserved
                rxn["c_balance"] = "false"
            else:
                rxn["c_balance"] = "true"
            if [k.id for k,v in rxns.metabolites.items() if not k.formula]:
                rxn["c_balance"] = "true"
        else:
            rxn["c_balance"] = ""



def net_penalty_points(model_info):
    """
    give reaction penalty
    """
    # rules.get_all_rules(model_info, model)
    # check_rxn_balance(model_info, model)
    # check_C_balance(model_info, model)
    for rxn in model_info['reactions']:
        grate = 0
        if rxn['id'] not in model_info['exchange_rxns'] and rxn['id'] not in model_info['transport_rxns'] and not rxn['id'].startswith('ADD_'):
            if rxn['balance'] == 'false':  # Response Imbalance Response Penalty
                grate += 3
                rxn["rules"]["charge and mass unbalanced reactions"] = "true"
            if rxn['c_balance'] == 'false':  # carbon imbalance reaction penalty
                grate += 20
                rxn["rules"]["unbalance reaction with carbon"] = "true"
            if rxn["rules"]:  # 3 points for failure to comply with reaction direction rules
                grate += 3
            if rxn["annotation"] == "false":
                grate += 1
                rxn["rules"]["Reactions without annotation information may be incorrect."] = "true"
            rxn["net_penalty_points"] = grate
            if 'right_chain_rxn' in rxn['rules'].keys():
                rxn["net_penalty_points"] = 0
        elif rxn['id'] in model_info['exchange_rxns'] and ('Superoxide anion cannot be taken up by cells directly' in rxn["rules"].keys() or 'energy_reducing_power' in rxn["rules"].keys()):
            rxn["net_penalty_points"] = 3
        else:
            rxn["net_penalty_points"] = 0
        # if rxn['id']=='ALAB':
        #     print(rxn["net_penalty_points"])
        #     exit()
 
def get_c_mol(model):
    """"""
    if model.slim_optimize() > 0:
        pfba_solution = pfba(model)
        need_fluxes = pfba_solution.fluxes[abs(pfba_solution.fluxes)>1e-6] 
    else:
        need_fluxes = {}
    num=0
    for r,v in need_fluxes.items():
        rxns = model.reactions.get_by_id(r)
        check = rxns.check_mass_balance() 
        if len(rxns.metabolites) == 1:
            if 'C' in check and v < 0:
                num += abs(check['C'] * v)
                print('get_c_mol',num,check['C'],v,rxns,check,'........................')
    try:                
        return round(model.slim_optimize()/num,3)
    except:
        return 0

def write_flux_file(model_info, model, objectiveId, yieldId, cfg:object):
    """
    get flux file
    """
    # pfba_solution = pfba(model)  # Reaction with limited flux value v greater than 1e-6
    # need_fluxes = pfba_solution.fluxes[abs(pfba_solution.fluxes)>1e-6]  # abs(pfba_solution.fluxes)>1e-6 gets the true or false result of each reaction, and finally returns true
    if model.slim_optimize() > 0:
        pfba_solution = pfba(model)
        need_fluxes = pfba_solution.fluxes[abs(pfba_solution.fluxes)>1e-6] 
    else:
        need_fluxes = {}
    flux_table = os.path.join(cfg.output_dir,f"{yieldId}.tsv")
    formulas, r_list = '', []
    count=0
    with open(flux_table, 'w') as flux:  
    # with open(f"tmp/y3z/{metId}.txt", 'w') as flux:  
        for r,v in need_fluxes.items():
            count+=1
            # print(count,r,model.reactions.get_by_id(r),v,'.............')
            for rxn in model_info['reactions']:
                if r == rxn['id'] and r != objectiveId:
                    r_list.append(r)
                    rxns = model.reactions.get_by_id(r)
                    check = rxns.check_mass_balance()  
                    if len(rxns.metabolites)==1:
                        all_met = [m for m in rxns.metabolites][0]
                        formulas = all_met.formula
                    # print(r,rxn['net_penalty_points'],'..............................')
                    try:
                        check = rxns.check_mass_balance()        
                        flux.write(f"{r}\t{round(v,5)}\t{rxn['rxn_exp_id']}\t{rxn['rxn_exp_name']}\t{check}\t{rxn['net_penalty_points']}\t{rxns.bounds}\t{formulas}\n")   
                    except ValueError:
                        flux.write(f"{r}\t{round(v,5)}\t{rxn['rxn_exp_id']}\t{rxn['rxn_exp_name']}\t{rxn['net_penalty_points']}\t{rxns.bounds}\t{formulas}\n")   
                    except KeyError:
                        print(rxn, repr(KeyError))
                        # exit()
            if r == objectiveId:
                rxns = model.reactions.get_by_id(r)
                flux.write(f"{r}\t{round(v,5)}\t{rxns.reaction}\t{rxns.build_reaction_string(use_metabolite_names=True)}\t{rxns.check_mass_balance()}\t{rxns.bounds}\n")
            if 'sink_rxn' in model_info.keys() and r in model_info['sink_rxn']:
                rxns = model.reactions.get_by_id(r)
                flux.write(f"{r}\t{round(v,5)}\t{rxns.reaction}\t{rxns.build_reaction_string(use_metabolite_names=True)}\t{rxns.check_mass_balance()}\t{rxns.bounds}\t{formulas}\n")
            if 'gaped_rxn' in model_info.keys() and r in model_info["gaped_rxn"]:
                rxns = model.reactions.get_by_id(r)
                flux.write(f"{r}\t{round(v,5)}\t{rxns.reaction}\t{rxns.build_reaction_string(use_metabolite_names=True)}\t{rxns.check_mass_balance()}\t{rxns.bounds}\t{formulas}\n")
            if 'modify_rxn' in model_info.keys() and r in model_info["modify_rxn"] and r not in r_list:
                rxns = model.reactions.get_by_id(r)
                flux.write(f"{r}\t{round(v,5)}\t{rxns.reaction}\t{rxns.build_reaction_string(use_metabolite_names=True)}\t{rxns.check_mass_balance()}\t{rxns.bounds}\t{formulas}\n")


         

def write_flux_file3(model_info, model, objectiveId,cfg:object):
    """
    get flux file
    """
    if model.slim_optimize() > 0:
        pfba_solution = pfba(model)
        need_fluxes = pfba_solution.fluxes[abs(pfba_solution.fluxes)>1e-6] 
    else:
        need_fluxes = {}
    with open(cfg.flux_path3, 'w') as flux:  
        for r,v in need_fluxes.items():
            for rxn in model_info['reactions']:
                if r == rxn['id'] and r != objectiveId:
                    rxns = model.reactions.get_by_id(r)
                    try:
                        check = rxns.check_mass_balance()        
                        flux.write(f"{r}\t{round(v,5)}\t{rxn['rxn_exp_id']}\t{rxn['rxn_exp_name']}\t{check}\t{rxn['net_penalty_points']}\t{rxns.bounds}\n")   
                    except ValueError:
                        flux.write(f"{r}\t{round(v,5)}\t{rxn['rxn_exp_id']}\t{rxn['rxn_exp_name']}\t{rxn['net_penalty_points']}\t{rxns.bounds}\n")   
                    except KeyError:
                        print(rxn, repr(KeyError))
                        # exit()
            if r == objectiveId:
                rxns = model.reactions.get_by_id(r)
                flux.write(f"{r}\t{round(v,5)}\t{rxns.build_reaction_string(use_metabolite_names=False)}\t{rxns.check_mass_balance()}\t{rxns.bounds}\n")
            if 'sink_rxn' in model_info.keys() and r in model_info['sink_rxn']:
                rxns = model.reactions.get_by_id(r)
                flux.write(f"{r}\t{round(v,5)}\t{rxns.build_reaction_string(use_metabolite_names=False)}\t{rxns.check_mass_balance()}\t{rxns.bounds}\n")

 

def write_flux_file2(model_info, model, objectiveId,yieldId,cfg:object):
    """
    get flux file
    """
    if model.slim_optimize() > 0:
        pfba_solution = pfba(model)
        need_fluxes = pfba_solution.fluxes[abs(pfba_solution.fluxes)>1e-6] 
    else:
        need_fluxes = {}
    flux_table = os.path.join(cfg.output_dir,f"{yieldId}.tsv")
    with open(flux_table, 'w') as flux:  
        for r,v in need_fluxes.items():
            # print(r,model.reactions.get_by_id(r),v,'.............')
            for rxn in model_info['reactions']:
                if r == rxn['id'] and r != objectiveId:
                    rxns = model.reactions.get_by_id(r)
                    # print(rxn['rxn_exp_id'])
                    try:
                        check = rxns.check_mass_balance()      
                        flux.write(f"{r}\t{round(v,5)}\t{rxn['rxn_exp_id']}\t{check}\t{rxns.bounds}\n") 
                    except ValueError:
                        flux.write(f"{r}\t{round(v,5)}\t{rxn['rxn_exp_id']}\t{rxns.bounds}\tno_check_mass_balance\n")  
            if r == objectiveId:
                rxns = model.reactions.get_by_id(r)
                flux.write(f"{r}\t{round(v,5)}\t{rxns.build_reaction_string(use_metabolite_names=True)}\t{check}\t{rxns.bounds}\n")
            if 'sink_rxn' in model_info.keys() and r in model_info['sink_rxn']:
                rxns = model.reactions.get_by_id(r)
                flux.write(f"{r}\t{round(v,5)}\t{rxns.build_reaction_string(use_metabolite_names=True)}\t{rxns.check_mass_balance()}\t{rxns.bounds}\n")
      


def get_visualiza_html(model, rxnId, need_fluxes, cfg:object):
    """"""
    # simple_model = Model('simple_model')
    # all_met = []
    flux_table = os.path.join(cfg.output_dir,f"{rxnId}.tsv")
    # need_fluxes=model.optimize().fluxes[abs(model.optimize().fluxes)>1e-6]
    # need_fluxes = pfba_solution.fluxes[abs(pfba_solution.fluxes)>1e-6]  # abs(pfba_solution.fluxes)>1e-6 gets the true or false result of each reaction, and finally returns true
    with open(flux_table, 'w') as flux:  
        for r,v in need_fluxes.items():
            rxns = model.reactions.get_by_id(r) 
            # equ = rxns.build_reaction_string()
            # simple_model.add_reactions([rxns])    
            # add_rxn(simple_model, rxns.id, equ)
            try:
                check = rxns.check_mass_balance()  
                flux.write(f"{r}\t{round(v,5)}\t{rxns.reaction}\t{rxns.build_reaction_string(use_metabolite_names=True)}\t{rxns.bounds}\t{check}\n") 
            except:
                flux.write(f"{r}\t{round(v,5)}\t{rxns.reaction}\t{rxns.build_reaction_string(use_metabolite_names=True)}\t{rxns.bounds}\tno_check_mass_balance\n") 
    # simple_model.add_reactions(flux_rxns)
    # for met in simple_model.metabolites:
    #     all_met.append(met.id)
    # common_factor_list=list(set(total_common_factor_list).intersection(set(all_met)))
    # pathway_df = pd.read_table(flux_table)
    # pathway_df.columns = ['id','fluxes','equ','bounds','check']
    # pathway_df.set_index('id',inplace=True)
    # d3flux.update_cofactors(simple_model, common_factor_list)
    # html = d3flux.flux_map(simple_model,excluded_reactions =exclude_rxn, figsize=(1500,1550),flux_dict=pathway_df['fluxes'])
    # html_file = os.path.join(cfg.output_dir,f"{rxnId}.html")
    # with open(html_file, "w")as wf:
    #     wf.write(html.data)
    # try:
    #     pathway_tsv_visualization(flux_table,cofactor_switch = "T",flow="True",outputdir=cfg.output_dir,rxnId=rxnId,model=model)
    # except Exception as e:
    #     print(str(e))
    # pathway_tsv_visualization(flux_table,cofactor_switch = "T",flow="True",id_or_name="True",outputdir=cfg.output_dir,rxnId=rxnId,model=model,substrate='',product=rxnId)
    pathway_tsv_visualization(flux_table,cofactor_switch = "T",flow="True",outputdir=cfg.output_dir,rxnId=rxnId,model=model)


def get_substance_approach(model, need_fluxes, metId):
    """"""
    substance_flux = []
    for r,v in need_fluxes.items():
        rxns = model.reactions.get_by_id(r) 
        substance_approach = {
            "approach(ID)": metId,
            "reaction(ID)" : r,
            "equation(ID)" : rxns.reaction,
            "equation(Name)" : rxns.build_reaction_string(use_metabolite_names=True),
            "check_mass_balance" : convert_check_mass_balance_to_str(rxns),
            "flux" : round(v,3),
            "l_b" : rxns.lower_bound,
            "u_b" : rxns.upper_bound
        }
        substance_flux.append(substance_approach)
    return substance_flux

def check_rule(model_info, model, ids, v, cfg:object):
    """"""
    rxns = model.reactions.get_by_id(ids)
    rules2 = Rules2(ids, cfg, v)  
    rules2.get_all_rules(model_info, model)
    for rxn in model_info['reactions']:
        if ids == rxn['id']:
            if rxn['balance'] == 'false' or rxn['c_balance'] == 'false':
                model.reactions.get_by_id(ids).bounds = (0,0)
                break
            if 'rule_conflict' in rxn.keys():
                if v < 0 : model.reactions.get_by_id(ids).bounds = (0,1000) 
                if v > 0 : model.reactions.get_by_id(ids).bounds = (-1000,0)
            else:
                model.reactions.get_by_id(ids).bounds = (0,0)



def add_back_reactions_net(model_info, model, check_model, grate_delete_rxn, identifier, num, cfg:object):
    """
    Add the checked reaction back to see if target product can still be generated infinitely
    """
    infinite_rxn, all_need_fluxes = [], {}
    for rxn in model_info['reactions']:
        # rxn[f"{identifier}_modify"] = 'false'
        for rxnId in grate_delete_rxn:
            if rxnId == rxn['id']:
                model.reactions.get_by_id(rxnId).bounds = check_model.reactions.get_by_id(rxnId).bounds
                if model.slim_optimize() >= num:
                    if model.slim_optimize() > 0:
                        pfba_solution = pfba(model)
                        need_fluxes = pfba_solution.fluxes[abs(pfba_solution.fluxes)>1e-6] 
                    else:
                        need_fluxes = {}
                    if len(need_fluxes) > 0:
                        get_visualiza_html(model, rxnId, need_fluxes, cfg)
                        all_need_fluxes.update(need_fluxes)
                    rxns = model.reactions.get_by_id(rxnId) 
                    rxn_bounds = rxns.bounds           
                    if rxn['balance'] == 'false':
                        rxns.bounds = (0,0)
                        rxn['bounds'] = [0,0]
                        rxn[f"{identifier}_modify"] = "true"
                        infinite_rxn.append(rxnId)
                    else:
                        if pfba_solution.fluxes[rxnId] > 0:
                            rxns.bounds = (-1000,0)
                            rxn['bounds'] = [-1000,0]
                            rxn[f"{identifier}_modify"] = "true"
                            infinite_rxn.append(rxnId)
                        if pfba_solution.fluxes[rxnId] < 0:
                            rxns.bounds = (0,1000)
                            rxn['bounds'] = [0,1000]
                            rxn[f"{identifier}_modify"] = "true"
                            infinite_rxn.append(rxnId)         
    return all_need_fluxes, infinite_rxn

def get_net_approach(model, yieldId, max_rate):
    """"""
    met = model.metabolites.get_by_id(yieldId)
    approach_info = {
        "substance(ID)": yieldId,
        "substance(Name)": met.name,
        "formula": met.formula,
        "objective_value" : round(model.slim_optimize(),2),
        "maximum_yield": round(max_rate,2),
    }
    return approach_info

def get_net_approach2(model, netId):
    """"""
    met = model.metabolites.get_by_id(netId)
    approach_info = {
        "substance(ID)": netId,
        "substance(Name)": met.name,
        "formula": met.formula,
        "objective_value" : round(model.slim_optimize(),2)
    }
    return approach_info

def convert_check_mass_balance_to_str(rxns):
    """"""
    convert_balance = []
    mass_balance = rxns.check_mass_balance()
    for element,val in mass_balance.items():
        convert_balance.extend([f"{element} : {round(val,3)}"])
    return ', '.join(convert_balance)

def old_get_net_infinite_info(model_info, model, model_control_info, identifier, flag):
    """
    Get response corrections
    """
    bounds_modification = ''
    for rxn in model_info['reactions']:
        if f"{identifier}_modify" in rxn.keys() and rxn[f"{identifier}_modify"] == "true" and rxn['rules']:
            rxns = model.reactions.get_by_id(rxn['id'])
            if rxn['bounds'] == [0,0] : bounds_modification = "close"
            if rxn['bounds'] == [-1000,0] : bounds_modification = "<--"
            if rxn['bounds'] == [0,1000] : bounds_modification = "-->"
            infiniteInfo = {"reaction_id" : rxn["id"],
                        "reactive_expression" : rxn['rxn_exp_name'], 
                        "reaction_error_reason" : ','.join(list(rxn['rules'].keys())),
                        "reaction_balance" : convert_check_mass_balance_to_str(rxns),
                        "reaction_modifications" : bounds_modification}
            model_control_info[f"{flag}"]['model_revision'].append(infiniteInfo)

def get_net_infinite_info(model_info, model, identifier):
    """
    Get response corrections
    """
    bounds_modification, temp = '', []
    for rxn in model_info['reactions']:
        if f"{identifier}_modify" in rxn.keys() and rxn[f"{identifier}_modify"] == "true" and rxn['rules']:
            rxns = model.reactions.get_by_id(rxn['id'])
            if rxn['bounds'] == [0,0] : bounds_modification = "close"
            if rxn['bounds'] == [-1000,0] : bounds_modification = "<--"
            if rxn['bounds'] == [0,1000] : bounds_modification = "-->"
            infiniteInfo = {"reaction_id" : rxn["id"],
                        "equation(ID)" : rxn['rxn_exp_id'], 
                        "equation(Name)" : rxn['rxn_exp_name'], 
                        "reaction_error_reason" : ','.join(list(rxn['rules'].keys())),
                        "check_mass_balance" : convert_check_mass_balance_to_str(rxns),
                        "modifications" : bounds_modification,
                        "l_b" : rxn['bounds'][0],
                        "u_b" : rxn['bounds'][1]}
            model_info["revision_num"] += 1
            temp.append(infiniteInfo)
            model_info['modified_rxn_id'][rxn['id']] = rxns.bounds
    return temp

def get_yield_infinite_info(model_info, model):
    """"""
    temp = []
    if model_info['need_close_rely_rxn']:
        need_close_rely_rxn = model_info['need_close_rely_rxn']
        for rxn in model_info['reactions']:
            if rxn['id'] == need_close_rely_rxn:
                rxns = model.reactions.get_by_id(rxn['id'])
                infiniteInfo = {"reaction_id" : rxn["id"],
                            "equation(ID)" : rxn['rxn_exp_id'], 
                            "equation(Name)" : rxn['rxn_exp_name'], 
                            "reaction_error_reason" : ','.join(list(rxn['rules'].keys())),
                            "check_mass_balance" : convert_check_mass_balance_to_str(rxns),
                            "modifications" : "close",
                            "l_b" : rxn['bounds'][0],
                            "u_b" : rxn['bounds'][1]}
                temp.append(infiniteInfo)
                model_info['modified_rxn_id'][rxn['id']] = rxns.bounds
    if "need_gap_rxn" in model_info.keys():
        need_gap_rxn = model_info['need_gap_rxn']
        for rxnId in need_gap_rxn:
            rxns = model.reactions.get_by_id(rxnId)
            infiniteInfo = {"reaction_id" : rxnId,
                        "equation(ID)" : rxns.reaction, 
                        "equation(Name)" : rxns.build_reaction_string(use_metabolite_names=True), 
                        "reaction_error_reason" : "gap_rxn",
                        "check_mass_balance" : convert_check_mass_balance_to_str(rxns),
                        "modifications" : "gap_add",
                        "l_b" : rxns.lower_bound,
                        "u_b" : rxns.upper_bound}
            temp.append(infiniteInfo)
            model_info['modified_rxn_id'][rxnId] = rxns.bounds
    return temp

def reduct_modelinfo_modify(model_info):
    for rxn in model_info['reactions']:
        if "nadhs_modify" in rxn.keys():
            rxn["nadhs_modify"] = ""
        if "atps_modify" in rxn.keys():
            rxn["atps_modify"] = ""
        if "nets_modify" in rxn.keys():
            rxn["nets_modify"] = ""
        if "yields_modify" in rxn.keys():
            rxn["yields_modify"] = ""
        if "atpms_modify" in rxn.keys():
            rxn["atpms_modify"] = ""

def get_other_net_infinite_info(model_info, model, all_need_fluxes):
    """
    Get response corrections
    """
    temp = []
    for ids,v in all_need_fluxes.items():
        if ids in model_info["all_rxn_id"]:
            rxns = model.reactions.get_by_id(ids)
            infiniteInfo = {"reaction_id" : rxns.id,
                        "equation(ID)" : rxns.reaction, 
                        "equation(Name)" : rxns.build_reaction_string(use_metabolite_names=True), 
                        "check_mass_balance" : convert_check_mass_balance_to_str(rxns),
                        "l_b" : rxns.lower_bound,
                        "u_b" : rxns.upper_bound}
            temp.append(infiniteInfo)
    return temp

def recover_modified_rxn(model, check_model, model_control_info, identifier):
    """"""
    reas = []
    if "model_revision" in model_control_info[identifier].keys():
        for rea in model_control_info[identifier]["model_revision"]:
            reaId = rea["reaction_id"]
            reas.append(reaId)
            model.reactions.get_by_id(reaId).bounds = check_model.reactions.get_by_id(reaId).bounds
            return reas

def boundary_restoration(model_info, model, identifier):
    """
    Response to changes each cycle, restoring bounds in time
    """
    for rxn in model_info['reactions']:
        if f"{identifier}_modify" in rxn.keys() and rxn[f"{identifier}_modify"] == "true":
            model.reactions.get_by_id(rxn['id']).bounds = rxn['bounds']     
            rxn[f"{identifier}_modify"] = 'false'
    if model_info['need_close_rely_rxn']:
        need_close_rely_rxn = model_info['need_close_rely_rxn']
        model.reactions.get_by_id(need_close_rely_rxn).bounds = (0,0)

def return_restoration(model_info, model, check_model, biomasses):
    """"""
    if model_info['need_close_rely_rxn']:
        need_close_rely_rxn = model_info['need_close_rely_rxn']
        model.reactions.get_by_id(need_close_rely_rxn).bounds = (0,0)
    if "need_gap_rxn" in model_info.keys():
        need_gap_rxn = model_info['need_gap_rxn'] 
        # biomasses = Biomasses(cfg)
        general_library = biomasses.get_general_library(model) 
        biomasses.add_gap_rxn(model, need_gap_rxn, general_library, check_model)
    if "need_reduct_rxn" in model_info.keys():
        for rxnId in model_info['need_reduct_rxn']:
            model.reactions.get_by_id(rxnId).bounds = check_model.reactions.get_by_id(rxnId).bounds

def get_final_net_fluxes(modelInfo, model,check_model):
    """"""
    final_netId_flux, modelInfo["final_flux"] = [], {}
    # set_c_source_supply(modelInfo, model, 'nets')
    # set_auto_source_supply(modelInfo, model, check_model, 'nets')
    if len(modelInfo['net_generation']) == 0:
        return "No net generation"
    for netId in modelInfo['net_generation']:
        with model:
            met = model.metabolites.get_by_id(netId)
            if met.name in ACCOA and met.compartment in C_COMPARTMENT:
                object_rxn_id = add_accoa(model, str(met.id))
            else:
                object_rxn_id = add_demand(modelInfo, model, netId)
            if not object_rxn_id:
                continue
            model.objective = object_rxn_id  
            final_netId_flux.extend([f"{netId} : {round(model.slim_optimize(),3)}"])
            modelInfo["final_flux"][f"{netId}"] = round(model.slim_optimize(),3)
    return ', '.join(final_netId_flux)


def get_final_yield_fluxes(modelInfo, model):
    """"""
    final_yield_flux = []
    if len(modelInfo['yield_generation']) == 0:
        return "No yield generation"
    for yieldId in modelInfo['yield_generation']:
        with model:
            met = model.metabolites.get_by_id(yieldId)
            if met.name in ACCOA and met.compartment in C_COMPARTMENT:
                object_rxn_id = add_accoa(model, str(met.id))
            else:
                object_rxn_id = add_demand(modelInfo, model, yieldId)
            if not object_rxn_id:
                continue
            model.objective = object_rxn_id
            temp_max_rate = max_reduced_degree_rate(model, yieldId, modelInfo)
            final_yield_flux.extend([f"{yieldId} : {round(temp_max_rate,3)}"])
            modelInfo["final_flux"][f"{yieldId}"] = round(temp_max_rate,3)
    return ', '.join(final_yield_flux)


def write_biomass(model_control_info, temp_list, bio_type):
    """"""
    model_control_info['check_biomass_production'][f"{bio_type}"].extend(temp_list)    
    # print(f"{bio_type}:::::")
    # print(model_control_info['check_biomass_production'][f"{bio_type}"])                   


def get_final_fluxes(model_info, model, check_model, model_control_info):
    """"""
    final_flux = ["final_biomass", "final_nadh", "final_atp", "final_netld", "final_yield"]
    model_control_info["final_flux"] = dict.fromkeys(final_flux, "")
    initial_rxn_id = model_info["initial_rxn"]["biomass_rxn_id"]
    if "ADD_ATPM" in model.reactions:
        atpm_id = "ADD_ATPM"
    else:
        atpm_id = get_atpm_rxn(model_info, model, 'ATP', 'ADP')
    set_model_objective(model_info, model, atpm_id)
    final_atp = round(model.slim_optimize(),3)
    # write_flux_file(model_info, model, atpm_id,self.cfg)
    if "ADD_ATPM" in model.reactions:
        model.reactions.remove('ADD_ATPM')
    if "ADD_NADH" in model.reactions:
        nadh_id = "ADD_NADH"
    else:
        nadh_id = add_nadh_rxn(model)
    set_model_objective(model_info, model, nadh_id)
    final_nadh = round(model.slim_optimize(),3)
    # write_flux_file(model_info, model, nadh_id,self.cfg)
    model.reactions.remove('ADD_NADH')
    final_netld_flux = get_final_net_fluxes(model_info, model, check_model)
    if is_autotrophic(model_info):
        final_yield_flux = "This is an autotrophic strain, no need to calculate the yield"
    else:
        final_yield_flux = get_final_yield_fluxes(model_info, model)
    model.objective = initial_rxn_id
    final_biomass_flux = round(model.slim_optimize(),3)
    model_control_info["final_flux"] = {'final_biomass':final_biomass_flux,
                                        'final_nadh':final_nadh,
                                        'final_atp':final_atp,          
                                        'final_netld':final_netld_flux,
                                        'final_yield':final_yield_flux}


def comparison_quantitative(model_control_info ,model_info):
    """"""
    reduce_temp, energy_temp, net_temp, yield_temp, bio_temp = [], [], [], [], []
    xtp = ['A','C','G','U','I']
    reduces = {"Reducing power" : "NADH",
            "Initial" : model_control_info['initial_flux']["initial_nadh"],
            "Final" : model_control_info['final_flux']["final_nadh"]}
    reduce_temp.append(reduces)
    temp = {"nadh" : 0,
            "NADPH" : 0,
            "FADH2" : 0,
            "FMNH2" : 0,
            "Q8H2" : 0,
            "MQL8" : 0,
            "DMMQL8" : 0}
    for k in xtp:
        energys = {"Energy" : f"{k}TP",
                   "Initial" : model_control_info['initial_flux'][f"initial_{k}tp"],
                   "Final" : 0}
        energy_temp.append(energys)
    for k in model_info['net_generation']:
        nets = {"Substance" : k,
                "Initial" : model_info['initial_flux']["initial_net"][k],
                "Final" : model_info["final_flux"][k]}
        net_temp.append(nets)
    if is_autotrophic(model_info):
        yield_temp = ["This is an autotrophic strain, no need to calculate the yield"]
    else:
        for k in model_info['yield_generation']:
            yields = {"Substance" : k,
                    "Initial" : model_control_info['initial_flux']["initial_yield"][k],
                    "Final" : model_info["final_flux"][k]}
            yield_temp.append(yields)
    bios = {"Biomass" : "Biomass",
            "Initial" : model_control_info['initial_flux']["initial_biomass"],
            "Final" : model_control_info["final_flux"]["final_biomass"]}
    bio_temp.append(bios)
    model_control_info["quantitative_comparison_before_and_after_correction"] = {"reducing_equivalents_production" : reduce_temp,
                                                                                 "energy_production" : energy_temp,
                                                                                 "metabolite_production" : net_temp,
                                                                                 "metabolite_yield" : yield_temp,
                                                                                 "biomass_production" : bio_temp}
    del model_control_info["initial_flux"]
    del model_control_info["final_flux"]
    

def keep_decimal_places(reaction):
    """"""
    fwd_arrow, rev_arrow, reversible_arrow, arrow = '-->','<--','<=>', ''
    equation = reaction.reaction
    if fwd_arrow in equation:
        arrow = fwd_arrow
    elif rev_arrow in equation:
        arrow = rev_arrow
    elif reversible_arrow in equation:
        arrow = reversible_arrow
    reactant_str = ' + '.join([f"{format(abs(coefficient), '.3e')} {metabolite.name}" for metabolite, coefficient in reaction.metabolites.items() if coefficient < 0])
    product_str = ' + '.join([f"{format(abs(coefficient), '.3e')} {metabolite.name}" for metabolite, coefficient in reaction.metabolites.items() if coefficient > 0])
    equation_rounded = f"{reactant_str} {arrow} {product_str}"
    reactant_str_id = ' + '.join([f"{format(abs(coefficient), '.3e')} {metabolite.id}" for metabolite, coefficient in reaction.metabolites.items() if coefficient < 0])
    product_str_id = ' + '.join([f"{format(abs(coefficient), '.3e')} {metabolite.id}" for metabolite, coefficient in reaction.metabolites.items() if coefficient > 0])
    equation_rounded_id = f"{reactant_str_id} {arrow} {product_str_id}"
    return equation_rounded, equation_rounded_id

def convert_nan_to_null(model):
    """"""
    for met in model.metabolites:
        # if pd.isna(met.formula) or met.formula == 'nan' or not met.formula or met.formula == 'null' or met.formula is None:
        #     print(met,met.formula)
        #     met.formula = ''
        if pd.isna(met.formula) or met.formula == 'nan' or met.formula is None or not met.formula or met.formula == 'null':
            # print(met,met.formula,'..')
            met.formula = ""
            # print(met,met.formula,'..')
        if pd.isna(met.charge) or met.charge == 'nan' or met.charge is None or met.charge == 'null':
            # print(met,met.charge,',,')
            met.charge = 0
            # print(met,met.charge,',,')


def convert_list_to_string(model_control_info, model_check_info):
    """"""
    model_control_info['check_biomass_production']["Biomass_information"] = "\n".join(model_control_info['check_biomass_production']["Biomass_information"])
    model_control_info['check_biomass_production']["Gapfilling_of_biomass_components"] = "\n".join(model_control_info['check_biomass_production']["Gapfilling_of_biomass_components"])
    model_control_info['check_biomass_production']["Check_small_molecules"] = "\n".join(model_control_info['check_biomass_production']["Check_small_molecules"])
    model_control_info['check_biomass_production']["Check_macromolecules"] = "\n".join(model_control_info['check_biomass_production']["Check_macromolecules"])
    model_control_info['check_biomass_production']["Normalization_of_biomass"] = "\n".join(model_control_info['check_biomass_production']["Normalization_of_biomass"])
    model_control_info['check_biomass_production']["Check_synthesizability_of_biomass_components"] = "\n".join(model_control_info['check_biomass_production']["Check_synthesizability_of_biomass_components"])
    # model_control_info['check_biomass_production']["model_calculation_conditions:"] = '\n'.join(model_control_info['check_biomass_production']["model_calculation_conditions:"])


def change_model_control_info(model_file, model_control_info):
    """Change the model control info"""
    model_control_info["validate_sbml_model"] = {}
    validate_info = cobra.io.sbml.validate_sbml_model(model_file)
    model_control_info["validate_sbml_model"]["validate_info"] = "Something went wrong reading the SBML model. Most likely the SBML model is not valid. Please check that your model is valid using the `cobra.io.sbml.validate_sbml_model` function or via the online validator at http://sbml.org/validator . `(model, errors) = validate_sbml_model(filename)` If the model is valid and cannot be read please open an issue at https://github.com/opencobra/cobrapy/issues ."
    model_control_info["validate_sbml_model"]["validate_model"] = validate_info
    return model_control_info


def get_rely_rxn(model, model_info, check_model, object_rxn_id, need_fluxes):
    """"""
    rely_rxn = []
    # 一开始biomass没找到或者biomass初始值为0，就不需要找依赖反应了
    if not model_info["initial_rxn"]["biomass_rxn_id"] or model_info["initial_rxn"]["biomass_rxn_flux"] == 0:
        return rely_rxn
    with model:
        set_c_source_supply(model_info, model, 'atps', check_model)
        set_auto_source_supply(model_info, model, check_model, 'atps')
        # model.reactions.get_by_id(model_info["initial_rxn"]["biomass_rxn_id"]).bounds = (0,1000)
        model.objective = model_info["initial_rxn"]["biomass_rxn_id"]
        print('...............',model.slim_optimize(),'.................................')
         
        for rxn in model_info["reactions"]:
            if 'nadhs_modify' in rxn.keys() or 'atps_modify' in rxn.keys() or 'nets_modify' in rxn.keys() or 'yields_modify' in rxn.keys():
                # print('model_bound',model.reactions.get_by_id(rxn['id']).bounds,check_model.reactions.get_by_id(rxn['id']).bounds)
                model.reactions.get_by_id(rxn['id']).bounds = check_model.reactions.get_by_id(rxn['id']).bounds
                # print(rxn['id'],model.slim_optimize(),'.................................')
               
        
        # if 'DM_12dgr160_c' == object_rxn_id:
        #     # model.reactions.get_by_id('GLCD').bounds = (0,0)
        #     # print('GLCD',model.slim_optimize(),'////////////////////////////////////////////////////////')
        #     final_model = f"tmp/bigg/ICN718/{model}.xml"
        #     cobra.io.write_sbml_model(model,final_model)
        # print(model_info["initial_rxn"]["biomass_rxn_id"])
        # print(model.reactions.get_by_id(model_info["initial_rxn"]["biomass_rxn_id"]).bounds)
        print('...............',model.slim_optimize(),'222.................................')
        if model.slim_optimize() <= 1e-6:
            return rely_rxn
        
        for ids,v in need_fluxes.items():
            if ids == object_rxn_id:
                continue
            if ids in model_info['exchange_rxns']:
                continue
            bounds = model.reactions.get_by_id(ids).bounds
            model.reactions.get_by_id(ids).bounds = (0,0)
            # print(ids,model.reactions.get_by_id(ids).bounds,model.slim_optimize(),'....................................................')
            if model.slim_optimize() < 1e-6 or model.slim_optimize() == 'nan':
                rely_rxn.append(ids)
            # print(ids, model.slim_optimize(),model.reactions.get_by_id(ids).bounds)
            # model.reactions.get_by_id(ids).bounds = check_model.reactions.get_by_id(ids).bounds
            model.reactions.get_by_id(ids).bounds = bounds
    return rely_rxn

def write_model_info(model_info,cfg:object):
    """"""
    try:
        modelInfo = json.dumps(model_info, ensure_ascii=False, allow_nan = True, indent=1)
        with open(cfg.model_info, "w", newline='',) as f:
            f.write(modelInfo)
        return cfg.model_info
    except Exception as e:
        print(repr(e),'write_model_info.....................')
   
def get_model_info(cfg:object):
    """"""
    with open(cfg.model_info, 'r') as f:
        model_info = json.load(f)
    return model_info

def write_result(model_check_infos,cfg:object):
    """"""
    result = json.dumps(model_check_infos, ensure_ascii=False, allow_nan = True, indent=1)
    with open(cfg.result_file, "w", newline='\n',) as f:
        f.write(result)
    return cfg.result_file

def write_result2(model_control_info,cfg:object):
    """"""
    result = json.dumps(model_control_info, ensure_ascii=False, allow_nan = True, indent=1)
    with open(cfg.result_file2, "w", newline='\n',  errors='ignore') as f:
        f.write(result)
    return cfg.result_file2

def write_result3(model_control_info,cfg:object):
    """"""
    result = json.dumps(model_control_info, ensure_ascii=False, allow_nan = True, indent=1)
    with open(cfg.result_file3, "w", newline='\n',) as f:
        f.write(result)
    return cfg.result_file3

def write_result4(model_control_info,cfg:object):
    """"""
    result = json.dumps(model_control_info, ensure_ascii=False, allow_nan = True, indent=1)
    with open(cfg.result_file4, "w", newline='\n',) as f:
        f.write(result)
    return cfg.result_file4

def write_final_model(model, cfg:object, file_path:str):
    """"""
    try:
        if file_path.endswith(".json"):
            final_model = f"{cfg.output_dir}/{model}.json"
            print('test',final_model)
            cobra.io.save_json_model(model,final_model)
        elif file_path.endswith(".yaml"):
            final_model = f"{cfg.output_dir}/{model}.yaml"
            cobra.io.save_yaml_model(model,final_model)
        elif file_path.endswith(".mat"):
            final_model = f"{cfg.output_dir}/{model}.mat"
            cobra.io.save_matlab_model(model,final_model)
        else:
            final_model = f"{cfg.output_dir}/{model}.xml"
            print('test',final_model)
            # model2 = cobra.io.read_sbml_model("/home/dengxiao/mqc/tmp/other/iCac802_norm2/COBRAModel.xml")
            # print('test',final_model)
            # r1,r2=[],[]
            # for rxn in model.reactions:
            #     r1.append(rxn.id)
            #     for rxn2 in model2.reactions:
            #         r2.append(rxn2.id)
            #         if rxn.id == rxn2.id:
            #             if rxn.bounds!=rxn2.bounds:
            #                 print(rxn.id,rxn.bounds,rxn2.bounds)
            # print('ttttt')
            # print([k for k in r1 if k not in list(set(r2))],'xxx')
            # print([k for k in list(set(r2)) if k not in r1],'zzz')
            cobra.io.write_sbml_model(model,final_model)
    except:
        final_model = f"{cfg.output_dir}/{model}.json"
        print('test',final_model)
        cobra.io.save_json_model(model,final_model )
    print('刚写下的模型生长速率:',model.slim_optimize(),'............')
    return final_model

def write_check_model(model, cfg:object, file_path:str):
    """"""
    # if file_path.endswith(".json"):
    #     final_model = f"{cfg.output_dir}/check_model.json"
    #     print('test',final_model)
    #     cobra.io.save_json_model(model,final_model)
    # elif file_path.endswith(".yaml"):
    #     final_model = f"{cfg.output_dir}/check_model.yaml"
    #     cobra.io.save_yaml_model(model,final_model)
    # elif file_path.endswith(".mat"):
    #     final_model = f"{cfg.output_dir}/check_model.mat"
    #     cobra.io.save_matlab_model(model,final_model)
    # else:
    #     final_model = f"{cfg.output_dir}/check_model.xml"
    #     print('test',final_model)
    #     cobra.io.write_sbml_model(model,final_model)
    model_dic = model_to_dict(model, sort=False)
    final_model = f"{cfg.output_dir}/check_model.json"
    with open(f'{cfg.output_dir}/check_model.json', 'w') as f:
        json.dump(model_dic,f)
    # try:
    #     final_model = f"{cfg.output_dir}/check_model.xml"
    #     print('test',final_model)
    #     cobra.io.write_sbml_model(model,final_model)
    # except:
    #     final_model = f"{cfg.output_dir}/check_model.json"
    #     print('test',final_model)
    #     cobra.io.save_json_model(model,final_model )
    return final_model

def get_new_model(model_path, rxns_job, cfg:object):
    """
    rxns_job : list
    """
    output_dir = cfg.output_dir
    if model_path.endswith(".json"):
        model = cobra.io.load_json_model(model_path)
    elif model_path.endswith(".yaml"):
        model = cobra.io.load_yaml_model(model_path)
    elif model_path.endswith(".mat"):
        model = cobra.io.load_matlab_model(model_path)
    else:
        model = cobra.io.read_sbml_model(model_path)
    # if model_path.endswith(".json"):
    #     model = cobra.io.load_json_model(model_path)
    # else:
    #     model = cobra.io.read_sbml_model(model_path)
    if rxns_job:
        for modify_rxn in rxns_job:
            rxn = model.reactions.get_by_id(modify_rxn["reaction_id"])
            rxn.reaction = modify_rxn["equation(ID)"]
            rxn.lower_bound = modify_rxn["l_b"]
            rxn.upper_bound = modify_rxn["u_b"]
    # model.reactions.get_by_id('FDR').bounds=(-10,1000)
    if model_path.endswith(".json"):
        final_model = f"{output_dir}/new_{model}.json"
        cobra.io.save_json_model(model,final_model)
    elif model_path.endswith(".yaml"):
        final_model = f"{output_dir}/new_{model}.yaml"
        cobra.io.save_yaml_model(model,final_model)
    elif model_path.endswith(".mat"):
        final_model = f"{output_dir}/new_{model}.mat"
        cobra.io.save_matlab_model(model,final_model)
    else:
        final_model = f"{output_dir}/new_{model}.xml"
        cobra.io.write_sbml_model(model,final_model)
    # try:
    #     final_model = f"{output_dir}/new_{model}.xml"
    #     cobra.io.write_sbml_model(model,final_model)
    # except:
    #     final_model = f"{output_dir}/new_{model}.json"
    #     cobra.io.save_json_model(model,final_model )
    return final_model

def save_model(model_path, model_job, output_dir):
    """
    save model.

    Parameters
    ----------
    model_path : the path of the current model
    model_job : dict
        {"reaction_id": "EX_h_e", "equation(ID)": "h_e <=> ", "equation(Name)": "H+ <=> ", "reaction_error_reason": "modify_pmf_rxn",
        "check_mass_balance": "charge : -1.0, H : -1.0", "modifications": "-->", "l_b": 0, "u_b": 1000}
 
    Return
    ------
    final_model : cobra.Model
        The model after modified

    """
    # if model_path.endswith(".json"):
    #     model = cobra.io.load_json_model(model_path)
    # else:
    #     model = cobra.io.read_sbml_model(model_path)
    if model_path.endswith(".json"):
        model = cobra.io.load_json_model(model_path)
    elif model_path.endswith(".yaml"):
        model = cobra.io.load_yaml_model(model_path)
    elif model_path.endswith(".mat"):
        model = cobra.io.load_matlab_model(model_path)
    else:
        model = cobra.io.read_sbml_model(model_path)
    if model_job:
        for modify_rxn in model_job:
            rxn = model.reactions.get_by_id(modify_rxn["reaction_id"])
            rxn.reaction = modify_rxn["equation(ID)"]
            rxn.lower_bound = modify_rxn["l_b"]
            rxn.upper_bound = modify_rxn["u_b"]
    # try:
    #     final_model = f"{output_dir}/{model}.xml"
    #     cobra.io.write_sbml_model(model,final_model)
    # except:
    #     final_model = f"{output_dir}/{model}.json"
    #     cobra.io.save_json_model(model,final_model )
    if model_path.endswith(".json"):
        final_model = f"{output_dir}/new_{model}.json"
        cobra.io.save_json_model(model,final_model)
    elif model_path.endswith(".yaml"):
        final_model = f"{output_dir}/new_{model}.yaml"
        cobra.io.save_yaml_model(model,final_model)
    elif model_path.endswith(".mat"):
        final_model = f"{output_dir}/new_{model}.mat"
        cobra.io.save_matlab_model(model,final_model)
    else:
        final_model = f"{output_dir}/new_{model}.xml"
        cobra.io.write_sbml_model(model,final_model)
    return final_model

        
def get_ids(iterable):
    """Retrieve the identifier of a number of objects."""
    return [element.id for element in iterable]

def truncate(sequence):
    """
    Create a potentially shortened text display of a list.

    Parameters
    ----------
    sequence : list
        An indexable sequence of elements.

    Returns
    -------
    str
        The list as a formatted string.

    """
    LIST_SLICE = 5
    if len(sequence) > LIST_SLICE:
        return ", ".join(sequence[:LIST_SLICE] + ["..."])
    else:
        return ", ".join(sequence)