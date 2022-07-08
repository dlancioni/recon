import os
import sys
import json
import logging
from src.baselib import BaseLib
from src.dblib import DbLib
from src.fslib import FsLib
from src.sqllib import SqlLib
from src.etllib import EtlLib
from src.arealib import AreaLib
from src.utillib import UtilLib
from src.setuplib import SetupLib
from src.reconlib import ReconLib
fslib = FsLib()
sqllib = SqlLib()
utillib = UtilLib()

class CoreLib(BaseLib):

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.logger = logging.getLogger(__name__)
        
    def create_log_file(self, app_path, config):
        self.log_info(f"Create log file per recon")
        log_dir = config["log"]
        log_name = self.name.strip().lower()
        log_name = f"[log] [{log_name}].txt"
        log_path = app_path + log_dir + f"\\{log_name}"
        log_format = "%(asctime)s %(levelname)s %(message)s"
        logging.basicConfig(filename = log_path, filemode = "w", datefmt='%Y-%m-%d %H:%M:%S', format = log_format, level=logging.DEBUG)
        cfg_path = app_path + "\\config.json"
        self.log_info(f"App path: {app_path}")
        self.log_info(f"Log path: {log_path}")        
        self.log_info(f"Config path: {cfg_path}")
        logger = logging.getLogger()
        return logger        

    def process(self, app_path, recon):
        self.method = "corelib.process()"
        self.logger.info(f"{self.method}: Start method")
        dblib = DbLib()
        utillib = UtilLib()
        setuplib = SetupLib()
        fslib = FsLib()
        
        try:
            """ create new transaction for each recon """
            cn = dblib.begin_tran()
            """ get recon info """
            config = fslib.get_json(app_path + "config.json")
            """ get recon info """            
            recon = setuplib.get_recon_info(app_path, config["recons"], recon)
            self.id = recon["Id"]
            self.name = recon["Name"]
            """ create log and validate recon """            
            logger = self.create_log_file(app_path, config)
            utillib.log(f"Running recon {self.id} {self.name}")
            self.log_info(f"Validate json setup")
            if not setuplib.validate(recon):
                self.logger.info(f"{self.method}: Setup is invalid, aborting this recon")
                return False
            """ create recon area """
            arealib = AreaLib(self.id, self.name)
            fields, types = arealib.process(cn, recon)
            """ import files """
            etllib = EtlLib(self.id, self.name)
            etllib.process(cn, app_path, recon)
            """ reconcile data """
            reconlib = ReconLib(self.id, self.name, fields, types)
            reconlib.process(cn, recon)
            """ generate output """
            utillib.print(cn)
        except BaseException as err:
            dblib.rollback_tran(cn)
            self.log_error("Transaction rollbacked")
            self.log_error(f"Fail to reconcile: {str(err)}")
            return
        dblib.commit_tran(cn)
        self.log_info(f"Transaction commited")        
        self.log_info(f"Recon sucessfuly executed")