import os
import sys
import json
import logging
from src.fslib import FsLib
from src.etllib import EtlLib
from src.sqllib import SqlLib
from src.utillib import UtilLib
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
        
    def get_transaction(self):
        cn = dblib.get_connection()
        cursor = cn.cursor()
        cursor.execute("begin")
        self.logger.info(f"{self.method}:Start new database transaction")        
        return cursor

    def create_recon_area(self, cursor, setup):
        self.method = "CoreLib.create_recon_area()"
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
        id = setup["Id"]
        tb = f"tb{id}1"
        sql = sqllib.get_create_table_definition(tb, fields, types)
        cursor.execute(sql)
        tb = f"tb{id}2"
        sql = sqllib.get_create_table_definition(tb, fields, types)
        cursor.execute(sql)
        self.logger.info(f"{self.method}:Recon area sucessfuly created")

    def import_data(self, cursor, setup):
        self.method = "CoreLib.import_data()"
        ds = setup["Datasources"][0]
        etllib = EtlLib(self.id, self.name)
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
        cursor.execute("select * from tb11")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        
    def process(self):
        self.method = "CoreLib.process()"
        self.logger.info(f"{self.method}: Start method")
        try:
            setup = self.get_recon_info()
            self.id = setup["Id"]
            self.name = setup["Name"]
            cursor = self.get_transaction()
            self.create_recon_area(cursor, setup)
            self.import_data(cursor, setup)
            self.print(cursor)
        except:
            cursor.execute("rollback")
            self.logger.error(f"{self.method}:Fail to reconcile ")
        cursor.execute("commit")
        self.logger.info(f"{self.method}:End method")