from slicenet.mgrs.nfMgr import NfMgr
from tabulate import tabulate
from slicenet.entities.staticslice import StaticSlice
from slicenet.utils.slicenetlogger import slicenetLogger as logger
import uuid
from typing import List

class SliceMgr():
    
    slices = {}
    # sliceSvcsMap = {} not used

    def rollbackSliceNfs(rollNf_ids : List[uuid.UUID], slice_id : uuid.UUID):
        """ Rollback partial slice deployments from list of NFs for a given slice"""
        for nf_id in rollNf_ids:
            NfMgr.removeSlice(nf_id, slice_id)


    def deploySlice(slice: StaticSlice) -> bool:
        """Deploy a StaticSlice Object"""
        logger.debug(f"Deploying slice {slice.name} {slice.id}")
        if len(slice.sliceNfs) > 0:
            workingNf_ids = []
            for k,v in slice.sliceNfs.items():
                if not NfMgr.addSlice(k, v, slice.id):
                    logger.info(f"Did not add slice {slice.name}. Unable to satify {k} {v}")
                    logger.info(f"Rolling back partial slice deployments for {slice.name}")
                    SliceMgr.rollbackSliceNfs(workingNf_ids, slice.id)
                    return False
                else:
                    workingNf_ids.append(k)
            SliceMgr.slices[slice.id] = slice
            logger.info(f"Deployed slice {slice.name}")
            return True
        else:
            logger.info(f"Slice {slice.name} is empty. Skipped")
            return False
    
    def unDeploySlice(id: uuid.UUID):
        """UnDeploy a StaticSlice identified by its Id"""
        logger.debug(f"Un-Deploying slice {id}")
        slice = SliceMgr.slices[id]
        for k,_ in slice.sliceNfs.items():
            NfMgr.removeSlice(k, id)
        del(SliceMgr.slices[id])
    
    def addService(slice_id: uuid.UUID, weightage: float, service_id: uuid.UUID) -> bool:
        """Add a service identified by service_id to a slice identifed with slice_id for a weightage"""
        if slice_id in SliceMgr.slices:
            s: StaticSlice = SliceMgr.slices[slice_id]
        else:
            logger.info(f"Unable to add service {service_id} for slice {slice_id}. No such slice ")
            return False
        if s.addService(weightage/100, service_id):
            logger.info(f"Added service for slice {slice_id} using weight {weightage}")
            logger.debug(f"Added service {service_id} for slice {slice_id} using weight {weightage}")
            return True
        else:
            logger.info(f"Unable to add service {service_id} for slice {slice_id}. Insufficient Capacity ")
            return False
        
    
    def removeService(slice_id: uuid.UUID, service_id: uuid.UUID):
        """Remove a service identified by service_id from a slice identified by slice_id"""
        s : StaticSlice = SliceMgr.slices[slice_id]
        s.removeService(service_id)
        logger.debug(f"Removing service {service_id} from {slice_id}")
    
    def getSliceLoadLevelInfo(slice_id: uuid.UUID):
        """Return the current slice utilization ratio for given slice object"""
        a_slice : StaticSlice = SliceMgr.slices[slice_id]
        return a_slice.getSliceRemainingCapacity()

    def dumpSlices():
        """Dump slice info statistics on std out."""
        headers = ["Slice ID", "Slice Name", "Slice Availablity (%)"]
        items = []
        for k,v in SliceMgr.slices.items():
            item = [k,v.name, 100 - v.getSliceUtilRatio()]
            items.append(item)
        print(tabulate(items, headers, tablefmt="simple_grid"))
    
    def dumpSliceNfDistribution():
        """Dump the composition of slices"""
        headers = ["Slice ID", "Slice Name", "Nf Name"]
        items = []
        for k,v in SliceMgr.slices.items():
            nfs = ""
            for k,_ in v.sliceNfs.items():
                nfs = nfs + NfMgr.nfs[k].name + ","
            item = [k, v.name, nfs]
            items.append(item)
        print(tabulate(items, headers, tablefmt="simple_grid"))