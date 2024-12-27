# -*- coding: utf-8 -*-

import multiprocessing
from multiprocessing import Pipe, Process
import matplotlib.pyplot as plt
import time 
import numpy as np
from mqc.config import Config
from mqc.utils import *


class Interface():
    """ """
    def __init__(self,cfg:Config) -> None:
        """ """
        self.cfg = cfg


    def get_reducing_power_initial_flux(self, model_info, model, model_control_info):
        """"""
        flag, exist_nadh, nadh_flux = 0, [], []
        nadh_name, temp = ['NADH','NADPH','FADH2','FMNH2','Q8H2','MQL8','DMMQL8'], []
        reas = [NADH_NAME,NADPH,FADH2,FMNH2,Q8H2_NAME,MQL8,DMMQL8]
        pro1s = [NAD_NAME,NADP,FAD,FMN,Q8_NAME,MQN8,DMMQ8]
        pro2 = H_NAME
        for i, name in enumerate(nadh_name):
            nadh_id = get_other_nadh_rxn(model, reas[i], pro1s[i], pro2, name)
            if not nadh_id:
                continue
            exist_nadh.append(name)
            model.reactions.get_by_id(nadh_id).bounds = (0,1000)
            set_model_objective(model_info, model, nadh_id) 
            nadh_flux.append(round(model.slim_optimize(),3))

        # plt.bar(exist_nadh, nadh_flux)
        # plt.xlabel("Reducing equivalent substances")
        # plt.ylabel("Optimal production rate")
        # plt.savefig(self.cfg.nadh_png,dpi=300)
        # plt.clf()
       
        return {'x_label':exist_nadh,'y_label':nadh_flux}
            



    def get_energy_initial_flux(self, model_info, model, model_control_info):
        """"""
        xtp, temp = ['A','C','G','U','I'], []
        flag, exist_atp, atp_flux = 0, [], []
        for k in xtp:
            atpm_id = get_atpm_rxn(model_info, model, f'{k}TP', f'{k}DP')
            if not atpm_id:
                continue
            exist_atp.append(f'{k}TP')
            model.reactions.get_by_id(atpm_id).bounds = (0,1000)
            set_model_objective(model_info, model, atpm_id)
            atp_flux.append(round(model.slim_optimize(),3))
        
        # plt.bar(exist_atp, atp_flux)
        # plt.xlabel("Energy substances")
        # plt.ylabel("Optimal production rate")
        # plt.savefig(self.cfg.atp_png,dpi=300)
   
        return {'x_label':exist_atp,'y_label':atp_flux}



    def check_yield_formula(self, model, metId):
        """"""
        calculate_met = ['C','H','O','N','P','S']
        met = model.metabolites.get_by_id(metId)
        if not set(met.elements.keys()).issubset(set(calculate_met)):
            return 0
        if pd.isna(met.formula) or 'R' in met.formula or 'X' in met.formula or met.formula == 'nan' or not met.formula or met.formula == 'null':
            return 0
        return 1

    def find_yield_generation_subprocess(self, model_info, model, metabolites,conn):
        """Get all carbonaceous species that exceed the maximum theoretical yield"""
        yield_generation, c_num = [], 0
        initial_yield_flux, temp, temps, substance_flux = [], [], [], []
        temp_degree, netName, maxRate, objRate = [], [], [], []
        pid = multiprocessing.current_process().pid
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),f'pid {pid} model.metabolites num:',len(metabolites))
        
        

        for met in metabolites:
            if re.search("C[A-Z]",str(met.formula)) or re.search("C[\d]",str(met.formula)): # Carbon followed by capital letters or numbers
                c_num += 1
                if self.check_yield_formula(model, met.id) == 0:
                    print(met,': formula不明确,不计算')
                    continue
                try:
                    with model:
                        if met.name in ACCOA and met.compartment in C_COMPARTMENT:
                            objectiveId = add_accoa(model, str(met.id))
                        else:
                            objectiveId = add_demand(model_info, model, met.id)
                        if not objectiveId:
                            continue
                        model.objective = objectiveId
                        # write_flux_file(model_info, model, objectiveId,self.cfg)
                        max_rate, temps = max_reduced_degree_rate(model, met.id, model_info)
                        temp_degree.extend(temps)
                        print(met.id,model.slim_optimize(),max_rate)
                        if max_rate == 0: # 含碳物质，最大得率如果是0不用算；formula含有[CHONPS]以外的不算
                            continue
                        
                        model_opt = model.slim_optimize()
                        netName.append(met.id)
                        maxRate.append(round(max_rate,2))
                        objRate.append(round(model_opt,2))
                        # print(f'pid {pid} met: ',met.id,' object: ',model_opt,'  max_rate: ',max_rate)
                except:
                    pass 
        # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),f' pid {pid} yield_generation:',yield_generation)
        
        conn.send({
            "netName" : netName,
            "maxRate":maxRate,
            "objRate":objRate
        })
        conn.close()
        

    def find_yield_initial_flux(self,model_info, model, model_control_info):
        """
        
        """
        print ("Running in parallel")
        if 'biomass' in model.reactions:
            initial_rxn_id = 'biomass'
        else:
            initial_rxn_id = model_info['initial_rxn']['biomass_rxn_id']

        model.objective = initial_rxn_id
        # get all model metabolites
        metabolites = model.reactions.get_by_id(initial_rxn_id).reactants
        print("metabolites num: ",len(metabolites))
        metabolites_num = len(metabolites)
        PROCESS_NUM = 10
        
        average = metabolites_num // 10
        remains = metabolites_num % 10
        # create a list to keep all processes
        processes = []

        # create a list to keep connections
        parent_connections = []
        
        # create a process per instance
        for i in range(PROCESS_NUM):
            if i == PROCESS_NUM -1:
                tmp_metabolites = metabolites[i*average:]
            else:
                tmp_metabolites =  metabolites[i*average:(i+1)*average]     
            # create a pipe for communication
            parent_conn, child_conn = Pipe()
            parent_connections.append(parent_conn)

            # create the process, pass instance and connection
            process = Process(target=self.find_yield_generation_subprocess, args=(model_info,model,tmp_metabolites, child_conn,))
            processes.append(process)

        # start all processes
        for process in processes:
            process.start()

        # make sure that all processes have finished
        for process in processes:
            process.join()


        netName, maxRate, objRate = [], [], []
        for parent_connection in parent_connections:
            response = parent_connection.recv()
            netName += response["netName"]
            maxRate += response["maxRate"]
            objRate += response["objRate"]

        return {'yield_met_id':netName,
                'max_rate':maxRate,
                'obj_rate':objRate}
        

   
 

    def check_control(self, model_info, model, model_check_info, type):
        """""" 
        if type == 'reduce':
            pear_data = self.get_reducing_power_initial_flux(model_info, model, model_check_info)
        elif type == 'energy':
            pear_data = self.get_energy_initial_flux(model_info, model, model_check_info)
        else:
            if is_autotrophic(model_info):
                pear_data = {}
            else:
                pear_data = self.find_yield_initial_flux(model_info, model, model_check_info)

       
        # pear_data={'reduce':reducing_data,'energy':energy_data,'yield':yield_data}
        return pear_data

   
        
        
        
        