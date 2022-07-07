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

    def process(self, recon):
        self.method = "corelib.process()"
        self.logger.info(f"{self.method}: Start method")
        dblib = DbLib()
        utillib = UtilLib()
        setuplib = SetupLib()
        fslib = FsLib()
        try:
            """ get recon and setup info """
            recon = setuplib.get_recon_info(recon)
            self.id = recon["Id"]
            self.name = recon["Name"]
            app_path = fslib.get_dir_parent(fslib.get_dir())
            setup = fslib.get_json(app_path + "\\setup.json")
            """ create log per recon """
            log_path = setup["log"] 
            if log_path.find("etc:") > -1:
                log_path = fslib.get_dir_etc()
            log_name = self.name.strip().lower()
            log_name = f"[log] [{log_name}].txt"
            log_path += f"\\{log_name}"
            log_format = "%(asctime)s %(levelname)s %(message)s"
            logging.basicConfig(filename = log_path, filemode = "w", datefmt='%Y-%m-%d %H:%M:%S', format = log_format, level=logging.DEBUG)
            logger = logging.getLogger()
            utillib.log(f"Running recon {self.name}")
            """ validate json file """
            cn = dblib.begin_tran()
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
            self.logger.error(f"{self.method}:Fail to reconcile: {str(err)} ")
            return
        dblib.commit_tran(cn)
        self.logger.info(f"{self.method}:End method")