
import os
import sys
import json
import logging
from src.dblib import Db
from src.fslib import FsLib
from src.etllib import EtlLib
from src.sqllib import SqlLib
from src.utillib import UtilLib

dblib = Db()
fslib = FsLib()
sqllib = SqlLib()
etllib = EtlLib()
utillib = UtilLib()

class CoreLib:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def import_data(self, cn):
        self.method = "CoreLib.import_data()"
        self.logger.info(f"{self.method}: Start method")
        path = fslib.get_dir_etc("Saldo x Extrato.json")
        setup = fslib.get_json(path)
        ds = setup["Side 1"]["Datasource"][0]
        cn.cursor().execute("create table if not exists tb_saldo (agencia integer, conta text, saldo real )")
        return EtlLib().import_file(cn, ds)
        self.logger.info(f"{self.method}:End method")        
        
    def process(self):
        self.method = "CoreLib.process()"
        self.logger.info(f"{self.method}: Start method")
        cn = dblib.get_connection()
        if not self.import_data(cn):
            self.logger.info(f"{self.method}:Fail to import data, aborting...")
            return False
        
        self.logger.info(f"{self.method}:Starting reconciliation process")
    
        self.logger.info(f"{self.method}:End method")