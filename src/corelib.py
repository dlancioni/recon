import os
import sys
import json
import logging
from src.baselib import BaseLib
from src.dblib import DbLib
from src.fslib import FsLib
from src.sqllib import SqlLib
from src.etllib import EtlLib
from src.cfglib import ConfigLib
from src.arealib import AreaLib
from src.utillib import UtilLib
from src.setuplib import SetupLib
from src.reconlib import ReconLib
fslib = FsLib()
sqllib = SqlLib()
utillib = UtilLib()
cfglib = ConfigLib()

class CoreLib(BaseLib):

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.logger = logging.getLogger(__name__)
        
    def create_log_file(self):
        self.log_info(f"Create log file per recon")
        fslib = FsLib()
        file_name = f"[log] [{self.name.strip().lower()}].txt"
        log_path = fslib.get_path_log(file_name)
        log_format = "%(asctime)s %(levelname)s %(message)s"
        logging.basicConfig(filename = log_path, filemode = "w", datefmt='%Y-%m-%d %H:%M:%S', format = log_format, level=logging.DEBUG)
        logger = logging.getLogger()
        return logger

    def process(self, recon):
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
            path = fslib.get_path_recon(cfglib.get_config("recon_dir"), recon)
            recon = fslib.open_json(path)
            self.id = recon["Id"]
            self.name = recon["Name"]
            """ create log and validate recon """            
            logger = self.create_log_file()
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
            etllib.process(cn, recon)
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