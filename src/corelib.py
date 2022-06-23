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
        
    def validate(self, setup):
        self.method = "CoreLib.validate()"
        message = ""
        side1 = False
        side2 = False
        self.logger.info(f"{self.method}: Validating {self.name}")
        if str(setup["Id"]).strip() == "":
            message = f"Id is missing"
        if str(setup["Name"]).strip() == "": 
            message = f"Name is missing"
        for ds in setup["Datasources"]:
            if str(ds["Side"]) != "1" and str(ds["Side"]) != "2":
                message = f"Side is invalid or missing, must be 1 or 2"
            if str(ds["Side"]) == "1":
                side1 = True
            if str(ds["Side"]) == "2":
                side2 = True
            if str(ds["Name"]).strip() == "":
                message = f"Side name is missing"
            if str(ds["Source"]).strip() == "":
                message = f"Source is missing"
            if str(ds["Separator"]).strip() == "":
                message = f"Separator is missing"
            if len(ds["Field"]) == 0:
                message = f"Field definition not found"
            if len(ds["Type"]) == 0:
                message = f"Type definition not found"
            if len(ds["Mask"]) == 0:
                message = f"Mask definition not found"
            if len(ds["Field"]) != len(ds["Type"]):
                message = f"Field and Type definition are different"
            if len(ds["Field"]) > 0 and len(ds["Field"]) != len(ds["Mask"]):
                message = f"Field and Mask definition are different"
        if side1 == False:
            message = f"Configuration for side 1 not found"
        if side2 == False:
            message = f"Configuration for side 2 not found"
        if message != "":
            self.logger.info(f"{self.method}: {message}")
            os.system("cls")
            print(message)
            return False
        self.logger.info(f"{self.method}: {self.name.strip()} sucessfuly validated")
        return True

    def get_cn(self):
        self.method = "CoreLib.get_cn()"
        cn = dblib.get_connection()
        cursor = cn.cursor()
        cursor.execute("begin")
        self.logger.info(f"{self.method}: Start new database transaction")        
        return cursor

    def create_recon_area(self, cursor, setup):
        self.method = "CoreLib.create_recon_area()"
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
        self.method = "CoreLib.import_text_file()"
        etllib = EtlLib(self.id, self.name)        
        for datasource in setup["Datasources"]:
            filename = datasource["Source"]
            etllib.import_file(cursor, datasource)
            self.logger.info(f"{self.method}:File sucessfuly imported: {filename}")
        
    def get_recon_info(self):
        self.method = "CoreLib.get_recon_info()"
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
        self.method = "CoreLib.process()"
        self.logger.info(f"{self.method}: Start method")
        try:
            cursor = self.get_cn()            
            setup = self.get_recon_info()
            self.id = setup["Id"]
            self.name = setup["Name"]            
            if not self.validate(setup):
                self.logger.info(f"{self.method}: Setup is invalid, aborting this recon")
                return False
            self.create_recon_area(cursor, setup)
            self.import_text_file(cursor, setup)
            self.print(cursor)
        except:
            cursor.execute("rollback")
            self.logger.error(f"{self.method}:Fail to reconcile ")
        cursor.execute("commit")
        self.logger.info(f"{self.method}:End method")