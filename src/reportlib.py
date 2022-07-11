import os
import sys
import json
import logging
from src.baselib import BaseLib
from src.dblib import DbLib
from src.fslib import FsLib
from src.sqllib import SqlLib
from src.cfglib import ConfigLib
from src.utillib import UtilLib
from src.msglib import MsgLib

fslib = FsLib()
sqllib = SqlLib()
utillib = UtilLib()
cfglib = ConfigLib()
msglib = MsgLib()

class ReportLib(BaseLib):

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.logger = logging.getLogger(__name__)

    def process(self, cn, recon):
        self.method = "reportlib.process()"
        try:
            """ generate output reports"""
            path = fslib.get_path_report(cfglib.get_config("path_report"))
            f1 = fslib.join(path, f"[Lado 1][{self.name}].txt")
            f2 = fslib.join(path, f"[Lado 2][{self.name}].txt")
            f3 = fslib.join(path, f"[Resumo][{self.name}].txt")
            #print(1)
            
            
        except BaseException as err:
            dblib.rollback_tran(cn)
