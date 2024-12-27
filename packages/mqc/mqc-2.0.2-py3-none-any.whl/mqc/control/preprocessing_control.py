# -*- coding: utf-8 -*-

import cobra
import pandas as pd
import re 

from mqc.defaults import *
from ..utils import add_rxn
from mqc.config import Config

class Preprocess():
    """
    Model preprocessing related.

    Attributes
    ----------
    diff_results : python.Dictionary
        The dictionary structure of memote.MemoteResult objects.
    configuration : memote.MemoteConfiguration
        A memote configuration structure.

    """
    
    def __init__(self, file_path:str,cfg:Config):
        """
        load initial model.

        Parameters
        ----------
        file_path : str
            model file

        """
        self.cfg = cfg
        self.pattern = r"\([^()]*\)n"
        try:
            if file_path.endswith(".json"):
                self.model = cobra.io.load_json_model(file_path)
                self.check_model = cobra.io.load_json_model(file_path)
            elif file_path.endswith(".yaml"):
                self.model = cobra.io.load_yaml_model(file_path)
                self.check_model = cobra.io.load_yaml_model(file_path)
            elif file_path.endswith(".mat"):
                self.model = cobra.io.load_matlab_model(file_path)
                self.check_model = cobra.io.load_matlab_model(file_path)
            else:
                self.model = cobra.io.read_sbml_model(file_path)
                self.check_model = cobra.io.read_sbml_model(file_path)
        except:
            self.model = ""
            return None
       



    def add_bigg_formula(self):
        """
        Add formula and charge to bigg.

        Parameters
        ----------
        model : cobra.Model

        Return
        ------
        cobra.Model
            Model after adding formula and charge

        """
        bigg_pd = pd.read_excel("mqc/summary/bigg-met.xlsx")
        bigg_pd_formula = dict(zip(bigg_pd['id'], bigg_pd['formula']))
        bigg_pd_charge = dict(zip(bigg_pd['id'], bigg_pd['charge']))
        for met in self.model.metabolites:
            if met.id in list(bigg_pd['id']):
                met.formula = bigg_pd_formula[f"{met.id}"]
                met.charge = bigg_pd_charge[f"{met.id}"]


    def add_meta_formula(self, meta_met):  
        """
        Add formula to meta.

        Parameters
        ----------
        model : cobra.Model

        Return
        ------
        cobra.Model
            Model after adding formula 

        """
        df = pd.read_excel(self.cfg.meta_met)
        meta_formula = dict(zip(df['meta_id'], df['formula']))
        for metId in meta_met:
            met = self.model.metabolites.get_by_id(metId)
            if metId.split('@')[0] in list(df['meta_id']):   
                if met.formula and met.formula != 'X':
                    met.formula = re.sub(self.pattern, "", met.formula)
                else:
                    met.formula = str(meta_formula[metId.split('@')[0]])
            if not met.compartment:
                met.compartment = metId.split('@')[-1]
        

    def add_exchange_rxn(self, met_exchange):
        """
        Add formula to meta.

        Parameters
        ----------
        model : cobra.Model

        Return
        ------
        cobra.Model
            Model after adding formula 

        """
        h_c, h2o_c, pi_c, nh4_c, o2_c, co2_c, so4_c = '', '', '', '', '', '', ''
        for met in self.model.metabolites:
            if met.id in H : h_c = met.id 
            if met.id in H2O : h2o_c = met.id 
            if met.id in PI : pi_c = met.id 
            if met.id in NH4 : nh4_c = met.id 
            if met.id in O2 : o2_c = met.id 
            if met.id in CO2 : co2_c = met.id 
            if met.id in SO4 : so4_c = met.id 
        print(h_c, h2o_c, pi_c, nh4_c, o2_c, co2_c, so4_c,'add_exchange_rxn.................')
        rxn_name = ['add_h2o_exchange', 'add_nh4_exchange', 'add_pi_exchange', 'add_h_exchange', 'add_o2_exchange', 'add_co2_exchange', 'add_so4_exchange']
        rxn_exp = [h2o_c + ' <=>', nh4_c + ' <=>', pi_c + ' <=>', h_c + ' <=>', o2_c + ' <=>', co2_c + ' <=>', so4_c + ' <=>']
        for i in range(7):
            if rxn_name[i] == met_exchange:
                add_rxn(self.model, rxn_name[i], rxn_exp[i])
                add_rxn(self.check_model, rxn_name[i], rxn_exp[i])
      
 


    def add_seed_formula(self, seed_met):
        """
        Add formula to modelseed.

        Parameters
        ----------
        model : cobra.Model

        Returns
        -------
        cobra.Model
            Model after adding formula 

        """
        df = pd.read_excel(self.cfg.modelseed_met)
        modelseed_formula = dict(zip(df['id'], df['formula']))
        modelseed_name = dict(zip(df['id'], df['name']))
        modelseed_charge = dict(zip(df['id'], df['charge']))
        for metId in seed_met:
            met = self.model.metabolites.get_by_id(metId)
            if metId.split('_')[0] in list(df['id']):  
                met.name = modelseed_name[met.id.split('_')[0]]
                if met.formula and met.formula != 'X':
                    met.formula = re.sub(self.pattern, "", met.formula)
                else:
                    met.formula = str(modelseed_formula[met.id.split('_')[0]])
                if met.charge:
                    pass
                else:
                    if not pd.isna(modelseed_charge[met.id.split('_')[0]]):
                        met.charge = int(modelseed_charge[met.id.split('_')[0]])
            if not met.compartment:
                met.compartment = metId.split('_')[-1]


    def add_virtual_formula(self, virtual_met):
        """
        Add formula to modelseed.

        Parameters
        ----------
        model : cobra.Model

        Returns
        -------
        cobra.Model
            Model after adding formula 

        """
        df = pd.read_excel(self.cfg.virtual_met)
        virtual_formula = dict(zip(df['ID'], df['Formula']))
        virtual_name = dict(zip(df['ID'], df['Name']))
        virtual_charge = dict(zip(df['ID'], df['Charge']))
        for metId in virtual_met: 
            met = self.model.metabolites.get_by_id(metId) 
            for ids in df['ID']:  
                if metId.split('[')[0] == ids.split('[')[0]:
                    # met = self.model.metabolites.get_by_id(metId)
                    if met.formula and met.formula != 'X':
                        met.formula = re.sub(self.pattern, "", met.formula)
                    else:
                        met.formula = str(virtual_formula[ids])
                    if met.charge:
                        pass
                    else:
                        if not pd.isna(virtual_charge[ids]):
                            met.charge = int(virtual_charge[ids])
                    if met.name:
                        pass
                    else:
                        met.name = virtual_name[ids]
            if not met.compartment:
                met.compartment = metId.split('[')[-1].split(']')[0]

    def change_virtual_to_bigg(self, virtual_met):
        """
        使用 re.sub 函数匹配并替换字符串中的方括号为下划线
        正则表达式 r'\[(.*?)\]' 用于匹配方括号及其内容，其中 \[ 和 \] 分别匹配左方括号和右方括号，(.*?) 匹配方括号中的内容
        替换字符串 r'_\1' 中的 _ 表示要替换的字符，\1 表示正则表达式中第一个捕获组（即方括号中的内容）
        """
        for metId in virtual_met: 
            met = self.model.metabolites.get_by_id(metId) 
            met.id = re.sub(r'\[(.*?)\]', r'_\1', metId)

    def bind_id_name(self):
        """
        Through the original form, bind the reaction id and name.

        Parameters
        ----------
        model : cobra.Model

        Returns
        -------
        cobra.Model
            Model after adding formula 
        
        Notes
        -----
        The name directly read from the model is very messy, and it is difficult to directly extract the name

        """
        df = pd.read_excel("mqc/summary/modelseed_metabolites.xlsx")
        modelseed_id_to_name = dict(zip(df['id'], df['name']))
        return modelseed_id_to_name



    def add_kegg_formula(self, kegg_met):
        """Add formula to kegg"""
        kegg_met = pd.read_excel(self.cfg.kegg_met)
        kegg_formula = dict(zip(kegg_met['id'], kegg_met['formula']))
        kegg_name = dict(zip(kegg_met['id'], kegg_met['name']))
        kegg_charge = dict(zip(kegg_met['id'], kegg_met['charge']))
        for metId in kegg_met:
            if metId in list(kegg_met['id']):
                met = self.model.metabolites.get_by_id(metId)
                met.name = kegg_name[metId]
                if met.formula and met.formula != 'X':
                    met.formula = re.sub(self.pattern, "", met.formula)
                else:
                    met.formula = str(kegg_formula[metId])
                if met.charge:
                    pass
                else:
                    if not pd.isna(kegg_charge[metId]):
                        met.charge = int(kegg_charge[metId])


    def add_other_formula(self, other_met):
        """Add formula to metacyc"""
        bigg_metacyc_met = pd.read_excel(self.cfg.bigg_metacyc)
        bigg_metacyc_formula = dict(zip(bigg_metacyc_met['id'], bigg_metacyc_met['formula']))
        bigg_metacyc_charge = dict(zip(bigg_metacyc_met['id'], bigg_metacyc_met['charge']))
        bigg_metacyc_name = dict(zip(bigg_metacyc_met['id'], bigg_metacyc_met['name']))
        for metId in other_met:
            met = self.model.metabolites.get_by_id(metId)
            if metId in list(bigg_metacyc_met['id']):      # 代谢物ID在总表里面，就可以对formula进行添加
                met.name = bigg_metacyc_name[metId]
                if met.formula and met.formula != 'X': # formula存在时检测是否有问题
                    met.formula = re.sub(self.pattern, "", met.formula)
                else:
                    met.formula = str(bigg_metacyc_formula[metId])
                if met.charge:
                    pass
                else:
                    if not pd.isna(bigg_metacyc_charge[metId]):
                        met.charge = int(bigg_metacyc_charge[metId])
            else:  # 代谢物ID不在总表里面，需要对formula进行检测，将'C10H17O8PR2(C5H8O5PR)n'这种不合法formula变为'C10H17O8PR2'
                if met.formula and met.formula != 'X':
                    met.formula = re.sub(self.pattern, "", met.formula)     
            if not met.formula:
                for ids in list(bigg_metacyc_met['id']):
                    if metId.replace('_', '') == ids.replace('_', '') and ids.count('_') == metId.count('_') + 1:
                        if '__' in ids:
                            met.formula = str(bigg_metacyc_formula[ids])
            if not met.charge:
                for ids in list(bigg_metacyc_met['id']):
                    if metId.replace('_', '') == ids.replace('_', '') and ids.count('_') == metId.count('_') + 1:
                        if '__' in ids:
                            if not pd.isna(bigg_metacyc_charge[ids]):
                                met.charge = int(bigg_metacyc_charge[ids])
            if not met.compartment:
                met.compartment = metId.split('_')[-1]
                print(met.id,'add_other_formula.................',met.compartment)
            # if 'CHARGE' in met.notes and met.notes['CHARGE']=='NaN':
            #     met.notes['CHARGE'] = 0
  