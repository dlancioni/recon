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
from src.msglib import MsgLib

fslib = FsLib()
sqllib = SqlLib()
utillib = UtilLib()
cfglib = ConfigLib()
msglib = MsgLib()

class CoreLib(BaseLib):

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.logger = logging.getLogger(__name__)
        
    def create_log_file(self):
        fslib = FsLib()
        file_name = f"[log] [{self.name.strip().lower()}].txt"
        log_path = fslib.get_path_log(cfglib.get_config("path_log"), file_name)
        log_format = "%(asctime)s %(levelname)s %(message)s"
        logging.basicConfig(filename = log_path, filemode = "w", datefmt='%Y-%m-%d %H:%M:%S', format = log_format, level=logging.DEBUG)
        logger = logging.getLogger()
        return logger

    def process(self, recon):
        self.method = "corelib.process()"
        dblib = DbLib()
        utillib = UtilLib()
        setuplib = SetupLib()
        fslib = FsLib()
        try:
            """ create new transaction for each recon """
            cn = dblib.begin_tran()
            """ get recon info """
            path = fslib.get_path_recon(cfglib.get_config("path_recon"), recon)
            recon = fslib.open_json(path)
            setuplib.validate_key(recon)
            self.id = recon["Id"]
            self.name = recon["Name"]
            msglib.print(msglib.get_value(msglib.console, "M4", [self.id, self.name]))
            """ create log and validate recon """            
            logger = self.create_log_file()
            if not setuplib.validate(recon):
                return False
            msglib.print(msglib.get_value(msglib.console, "M5"))
            """ create recon area """
            arealib = AreaLib(self.id, self.name)
            fields, types = arealib.process(cn, recon)
            msglib.print(msglib.get_value(msglib.console, "M6"))
            """ import files """
            etllib = EtlLib(self.id, self.name)
            etllib.process(cn, recon)
            """ reconcile data """
            reconlib = ReconLib(self.id, self.name, fields, types)
            reconlib.process(cn, recon)
            """ generate output """
            #utillib.print(cn)
        except BaseException as err:
            dblib.rollback_tran(cn)
            raise
        dblib.commit_tran(cn)