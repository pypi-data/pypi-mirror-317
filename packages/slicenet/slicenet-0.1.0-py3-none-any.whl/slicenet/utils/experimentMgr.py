import sys
import os
import csv
import copy
sys.path.append('../slicenet')
from slicenet.mgrs.nfMgr import NfMgr
from slicenet.mgrs.sliceMgr import SliceMgr
from slicenet.mgrs.serviceMgr import ServiceMgr
from slicenet.entities.slicelet import Slicelet
from slicenet.utils.experiment import Experiment
from slicenet.utils.slicenetlogger import slicenetLogger as logger
from datetime import datetime


from typing import List, Dict


class ExperimentMgr:

    def __init__(self):
        self.experiments : List[Experiment] = []
        self.exp_dir = ""

    def loadExperimentsFromDir(self, in_dir: str, out_dir: str = "") -> bool:
        if os.path.exists(in_dir):
            self.exp_dir = in_dir
            for f in os.listdir(in_dir):
                if f.endswith('.yaml'):
                    abs_f = in_dir + "/" + f
                    self.experiments.append(Experiment(abs_f))
            if out_dir != "" and os.path.exists(out_dir):
                self.exp_dir = out_dir
            else:
                logger.error(f'Unable to set output dir to {out_dir}. Reverting outputs to {in_dir}')
            return True 
        else:
            logger.error(f'Invalid path or dir: {in_dir}')
            return False

    def loadExperimentsFromFiles(self, exp_list: List[str], out_dir:str = "") -> bool:
        for f in exp_list:
            if os.path.isfile(f) and f.endswith('.yaml'):
                self.experiments.append(Experiment(f))
            else:
                logger.error(f'Invalid path or file: {f}')
                return False
        self.exp_dir = os.getcwd()
        if out_dir != "" and os.path.exists(out_dir):
            self.exp_dir = out_dir
        else:
            logger.error(f'Unable to set output dir to {out_dir}. Reverting outputs to cwd {self.exp_dir}')        
        return True
    
    def prepareRow(self, eType: str, name: str, id :str, adm: str, his: str) -> List[str]:
        row = []
        row.append(eType)
        row.append(name)
        row.append(id)
        row.append(adm)
        row.append(his)
        return row
    
    def prepareRowWithSliceHistory(self, eType: str, name: str, id :str, adm: str, his_1: str, his_2: str, his_3: str, his_4:str) -> List[str]:
        row = []
        row.append(eType)
        row.append(name)
        row.append(id)
        row.append(adm)
        row.append(his_1)
        row.append(his_2)
        row.append(his_3)
        row.append(his_4)
        return row

    
    def saveInference(self):
        ts = datetime.now().strftime('%d%m%Y%H%M%S')
        for exp in self.experiments:
            fname = exp.exp_name + "_" + ts
            fname_infra = f"{self.exp_dir}/{fname}-infra.csv"
            fname_slicelets = f"{self.exp_dir}/{fname}-slicelets.csv"

            with open(fname_infra, 'w', newline='') as f:
                csvW = csv.writer(f)
                header = ["Entity", "Name", "ID", "Admitted?", "Event History"]
                csvW.writerow(header)
                for _,v in exp.exp_clouds.items():
                    aRow = self.prepareRow("Cloud", v.name, str(v.id), str(v.get_exp_status()), str(v.eventHistory))
                    csvW.writerow(aRow)
                for _,v in exp.exp_nfs.items():
                    aRow = self.prepareRow("NFs", v.name, str(v.id), str(v.get_exp_status()), str(v.eventHistory))
                    csvW.writerow(aRow)
                for _,v in exp.exp_slices.items():
                    aRow = self.prepareRow("Slices", v.name, str(v.id), str(v.get_exp_status()), str(v.eventHistory))
                    csvW.writerow(aRow)

            with open(fname_slicelets, 'w', newline='') as f:
                csvW = csv.writer(f)
                header = ["Epoch", "Name", "ID", "Admitted?", "Scheduled At", "Started At", "Ended At", "Overall Delay(sec)"]
                csvW.writerow(header)
                index = 1
                for e in exp.exp_epoch_slicelets:
                    for _,v in e.items():
                        aRow = self.prepareRowWithSliceHistory(index, v.name, str(v.id), str(v.get_exp_status()), 
                                               v.eventHistory['Slicelet Scheduled'] if v.get_exp_status() else "N/A",
                                               v.eventHistory['Slicelet Started'] if v.get_exp_status() else "N/A",
                                               v.eventHistory['Slicelet Ended'] if v.get_exp_status() else "N/A",
                                               v.eventHistory['Slicelet Delay'] if v.get_exp_status() else "N/A"
                                               )
                        csvW.writerow(aRow)
                    index += 1

    def deployAndLaunch(self):
        for exp in self.experiments:
            # Register Clouds
            for _,v in exp.exp_clouds.items():
                NfMgr.registerCloud(v)
            
            for k,v in exp.exp_policies.items():
                if k == "NfMgr":
                    NfMgr.setSchedularPolicy(v)

            # Deploy Nfs
            for _,v in exp.exp_nfs.items():
                v.exp_admitted = NfMgr.deployNf(v)

            # Deploy Slices
            for _,v in exp.exp_slices.items():
                v.exp_admitted = SliceMgr.deploySlice(v)

            # Register Services
            for _,v in exp.exp_services.items():
                v.exp_admitted = ServiceMgr.registerService(v)

            # Schedule Slicelets
            for _,v in exp.exp_slicelets.items():
                ServiceMgr.scheduleSlicelet(v)

            # for each epoch
            for e in range(exp.exp_epoch):

                logger.info(f'Launching experiment {exp.exp_name} for epoch {e}')

                # Launch Experiment
                ServiceMgr.launchExperiment()

                # perform a deep copy
                e_epoch_slicelets : Dict[str, Slicelet] = copy.deepcopy(exp.exp_slicelets)

                # update Slicelets with experiment data
                for _,v in ServiceMgr.slicelets.items():
                    e_epoch_slicelets[v.name] = v
                    logger.info(f'Updating slicelet {v.name} for epoch {e}')
                
                # save this epoch
                exp.exp_epoch_slicelets.append(copy.deepcopy(e_epoch_slicelets))

                # tear down slicelet services
                ServiceMgr.slicelets.clear()

if __name__ == '__main__':
    import os
    import logging
    
    logger = logging.getLogger('example')

    logging.basicConfig(format='%(asctime)s %(name)s %(module)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    
    example_config = os.getcwd() + "/examples/example1.yaml"

    experiment1 = Experiment(example_config)
    ExperimentMgr.deployAndLaunch(exp=experiment1)
    logger.info("After experiment")
    #experiment1.displaySliceletStatistics()
    for k,v in experiment1.exp_nfs.items():
        logger.info(f"{k} was admitted? {v.get_exp_status()}")
    for k,v in experiment1.exp_slicelets.items():
        logger.info(f"Slicelet {v.name} {v.eventHistory} {v.initRandomDelaySecs}")
    logger.info("Checking if this prints")