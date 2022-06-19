
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

    def create_recon_area(self, cursor, setup):
        self.method = "CoreLib.create_recon_area()"
        tablename = setup["Side 1"]["Datasource"][0]["Table"]
        f1 = setup["Side 1"]["Datasource"][0]["Field"]
        t1 = setup["Side 1"]["Datasource"][0]["Type"]
        f2 = setup["Side 1"]["Datasource"][0]["Field"]
        t2 = setup["Side 1"]["Datasource"][0]["Type"]                
        fields, types = sqllib.get_table_structure(f1, t1, f2, t2)
        sql = sqllib.get_create_table_definition(tablename, fields, types)        
        cursor.execute(sql)
        self.logger.info(f"{self.method}:Recon area sucessfuly created")        

    def import_data(self, cursor, setup):
        self.method = "CoreLib.import_data()"
        ds = setup["Side 1"]["Datasource"][0]
        etllib.import_file(cursor, ds)
        self.logger.info(f"{self.method}:Files imported sucessfuly")        
        
    def get_recon_info(self):
        self.method = "CoreLib.get_recon_info()"
        path = fslib.get_dir_etc("Saldo x Extrato.json")
        setup = fslib.get_json(path)
        self.logger.info(f"{self.method}:Setup loaded sucessfuly")
        return setup
        
    def print(self, cursor):
        os.system("cls")
        cursor.execute("select * from tb_saldo")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        
    def process(self):
        self.method = "CoreLib.process()"
        self.logger.info(f"{self.method}: Start method")
        try:            
            cn = dblib.get_connection()
            cursor = cn.cursor()
            cursor.execute("begin")
            setup = self.get_recon_info()            
            self.logger.info(f"{self.method}:Transaction started")
            self.create_recon_area(cursor, setup)
            self.import_data(cursor, setup)
            self.print(cursor)
        except:
            cursor.execute("rollback")
            self.logger.error(f"{self.method}:Fail to reconcile ")
        cursor.execute("commit")
        self.logger.info(f"{self.method}:End method")