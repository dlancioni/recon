import os
import sys
import json
import logging
from src.dblib import DbLib
from src.fslib import FsLib
from src.loglib import LogLib
from src.msglib import MsgLib
from src.sqllib import SqlLib
from src.etllib import EtlLib
from src.baselib import BaseLib
from src.arealib import AreaLib
from src.utillib import UtilLib
from src.cfglib import ConfigLib
from src.setuplib import SetupLib
from src.reconlib import ReconLib
from src.reportlib import ReportLib
from src.validlib import ValidationLib
from src.maillib import MailLib
from termcolor import colored, cprint

""" general declaration """
dblib = DbLib()
fslib = FsLib()
msglib = MsgLib()
sqllib = SqlLib()
utillib = UtilLib()
maillib = MailLib()
cfglib = ConfigLib()
setuplib = SetupLib()
validlib = ValidationLib()

class CoreLib(BaseLib):

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.logger = logging.getLogger(__name__)

    def process(self, recon):
        debug = 0
        status = False
        message = ""
        path_temp = ""
        loglib = LogLib("CoreLib", "process")
        try:           
            """ open json recon or file """
            recon = setuplib.open_recon(recon)
            self.id = setuplib.tag_value(recon, "Id")
            self.name = setuplib.tag_value(recon, "Name")
            logger = loglib.create_log_file(self.name)

            """ create new transaction for each recon """
            path_temp = fslib.get_path_log(cfglib.get(1))
            debug = int(cfglib.get(6))
            loglib.log(loglib.INFO, f"Debug mode: {True if debug == 1 else False}")
            cn = dblib.get_connection(path_temp, debug, self.name)
            cn = dblib.begin_tran(cn, debug)            
            
            """ validate recon """
            validlib.validate(recon)
            loglib.log(loglib.INFO, "Validation OK, ready to create area")
            msglib.print(msglib.get("M4", [self.id, self.name]))
            
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
            status = True
            message = ""

            """ notify succes """
            maillib.notify_success(recon)
            
        except BaseException as err:
            
            """ rollback info """
            message = str(err)
            status = False
            reports = []
            loglib.log(loglib.ERROR, f"{message}")
            dblib.rollback_tran(cn, debug)

            """ notify fail """
            maillib.notify_fail(recon, message)
            
        finally:
            
            """ present results in screen """
            if status == True:
                print(colored(msglib.set_time(msglib.get("M10", [self.name])), "green"))
            else:
                print(colored(msglib.set_time(msglib.get("M11", [self.name])), "red"))
                print(colored(msglib.set_time(message), "red"))
               
        """ finish current conciliation """
        return status, message, reports