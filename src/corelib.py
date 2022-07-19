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
from src.loglib import LogLib

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
        msg = ""
        if type(recon) == dict:
            return recon
        else:
            try:              
                filename = str(recon.split(".")[0]) +".cfg"
                path = cfglib.get_config("path_recon")
                path = fslib.get_path_recon(path, filename)
                msg = msglib.get_value(msglib.validation, "M4", [path])
                recon = fslib.open_json(path)
            except json.decoder.JSONDecodeError:
                print("There was a problem accessing the equipment data.")
            except BaseException as err:
                raise Exception(msg)
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
        debug = 0
        path_temp = ""        
        loglib = LogLib("CoreLib", "process")
        try:
            """ create new transaction for each recon """
            path_temp = cfglib.get_config("path_temp")
            debug = int(cfglib.get_config("debug"))
            loglib.log(loglib.INFO, f"Debug mode: {True if debug == 1 else False}")
            cn = dblib.get_connection(path_temp, debug)
            cn = dblib.begin_tran(cn, debug)
            """ open json recon or file """
            recon = self.open_recon(recon)
            """ validate key info """
            setuplib.validate_info(recon)
            self.id = self.tagv(recon, "Id", "Id")
            self.name = self.tagv(recon, "Name", "Nome")
            """ create log and validate recon """
            logger = self.create_log_file()
            setuplib.validate(recon)
            loglib.log(loglib.INFO, "Validation OK, ready to create area")
            msglib.print(msglib.get_value(msglib.console, "M4", [self.id, self.name]))            
            """ create recon area """
            arealib = AreaLib(self.id, self.name)
            fields, types = arealib.process(cn, recon)
            loglib.log(loglib.INFO, "Area OK, ready to import files")
            """ import files """
            etllib = EtlLib(self.id, self.name)
            etllib.process(cn, recon)
            loglib.log(loglib.INFO, "Files OK, ready to execute reconciliation rules")
            """ reconcile data """
            reconlib = ReconLib(self.id, self.name, fields, types)
            reconlib.process(cn, recon)
            loglib.log(loglib.INFO, "Reconciliation OK, ready to generate reports")
            """ generate reports """
            reportlib = ReportLib(self.id, self.name)
            reports = reportlib.process(cn, recon)
            loglib.log(loglib.INFO, "Reports OK, ready to commit the process")
            """ commit info """
            dblib.commit_tran(cn, debug)
            return True, "", reports
        except BaseException as err:
            dblib.rollback_tran(cn, debug)
            loglib.log(loglib.ERROR, f"{str(err)}")            
            return False, str(err), ""