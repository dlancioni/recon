import os
import sys
import json
import logging
from src.fslib import FsLib
from src.etllib import EtlLib
from src.sqllib import SqlLib
from src.utillib import UtilLib
from src.setuplib import SetupLib
from src.dblib import Db

dblib = Db()
fslib = FsLib()
sqllib = SqlLib()
utillib = UtilLib()

class CoreLib:

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.logger = logging.getLogger(__name__)

    def get_cn(self):
        self.method = "corelib.get_cn()"
        cn = dblib.get_connection()
        cursor = cn.cursor()
        cursor.execute("begin")
        self.logger.info(f"{self.method}: Start new database transaction")        
        return cursor

    def create_recon_area(self, cursor, setup):
        self.method = "corelib.create_recon_area()"
        id = setup["Id"]        
        f1, t1 = [], []
        f2, t2 = [], []       
        for datasource in setup["Datasources"]:
            if datasource["Side"] == 1:
                f1 += datasource["Field"]
                t1 += datasource["Type"]
            if datasource["Side"] == 2:
                f2 += datasource["Field"]
                t2 += datasource["Type"]
        fields, types = sqllib.get_table_structure(f1, t1, f2, t2)
        for side in range(1, 3):
            tb = f"tb{id}{side}"
            sql = f"drop table if exists {tb}"
            cursor.execute(sql)
            sql = sqllib.get_create_table_definition(tb, fields, types)
            cursor.execute(sql)
            tb = f"tmp{id}{side}"
            sql = f"drop table if exists {tb}"
            cursor.execute(sql)
            sql = sqllib.get_create_table_definition(tb, fields, types)
            cursor.execute(sql)
        self.logger.info(f"{self.method}: Recon area sucessfuly created")

    def import_text_file(self, cursor, setup):
        self.method = "corelib.import_text_file()"
        etllib = EtlLib(self.id, self.name)        
        for datasource in setup["Datasources"]:
            filename = datasource["Source"]
            etllib.import_file(cursor, datasource)
            self.logger.info(f"{self.method}:File sucessfuly imported: {filename}")
            
    def reconcile(self, cursor, setup):
        self.method = "corelib.reconcile()"
        reconlib = reconlib(self.id, self.name)
        reconlib.process(cursor, setup)
        self.logger.info(f"{self.method}:File sucessfuly imported: {filename}")            
        
    def get_recon_info(self):
        self.method = "corelib.get_recon_info()"
        path = fslib.get_dir_etc("Saldo x Extrato.json")
        setup = fslib.get_json(path)
        self.logger.info(f"{self.method}: Setup loaded sucessfuly")
        return setup
        
    def print(self, cursor):
        os.system("cls")
        print("Side 1:")
        cursor.execute("select * from tb11")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        print("Side 2:")            
        cursor.execute("select * from tb12")
        rows = cursor.fetchall()
        for row in rows:
            print(row)            
        
    def process(self):
        self.method = "corelib.process()"
        self.logger.info(f"{self.method}: Start method")
        try:
            cursor = self.get_cn()            
            setup = self.get_recon_info()
            self.id = setup["Id"]
            self.name = setup["Name"]
            setuplib = SetupLib(self.id, self.name)
            if not setuplib.validate(setup):
                self.logger.info(f"{self.method}: Setup is invalid, aborting this recon")
                return False
            self.create_recon_area(cursor, setup)
            self.import_text_file(cursor, setup)
            self.print(cursor)
        except BaseException as err:
            cursor.execute("rollback")
            self.logger.error(f"{self.method}:Fail to reconcile: {str(err)} ")
        cursor.execute("commit")
        self.logger.info(f"{self.method}:End method")