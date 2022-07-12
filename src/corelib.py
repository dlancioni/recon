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
from src.reportlib import ReportLib

dblib = DbLib()
fslib = FsLib()
msglib = MsgLib()
sqllib = SqlLib()
utillib = UtilLib()
cfglib = ConfigLib()
setuplib = SetupLib()

class CoreLib(BaseLib):

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.logger = logging.getLogger(__name__)
        
    def open_recon(self, recon):        
        if type(recon) == dict:
            return recon
        else:
            path = fslib.get_path_recon(cfglib.get_config("path_recon"), recon)
            recon = fslib.open_json(path)
        return recon
        
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
        try:
            """ create new transaction for each recon """
            cn = dblib.begin_tran()
            """ open json recon or file """
            recon = self.open_recon(recon)
            """ validate key info """            
            setuplib.validate_info(recon)
            self.id = self.tagv(recon, "Id", "Id")
            self.name = self.tagv(recon, "Name", "Nome")
            msglib.print(msglib.get_value(msglib.console, "M4", [self.id, self.name]))
            """ create log and validate recon """            
            logger = self.create_log_file()
            setuplib.validate(recon)
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
            """ generate reports """
            reportlib = ReportLib(self.id, self.name)
            reportlib.process(cn, recon)
            """ commit info """
            dblib.commit_tran(cn)            
            """ generate output """
            return True, ""
        except BaseException as err:
            dblib.rollback_tran(cn)
            return False, str(err)
