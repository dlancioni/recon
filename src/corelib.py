import os
import sys
import json
import logging
from src.dblib import Db
from src.fslib import FsLib
from src.sqllib import SqlLib
from src.etllib import EtlLib
from src.arealib import AreaLib
from src.utillib import UtilLib
from src.setuplib import SetupLib
from src.reconlib import ReconLib

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

    def import_text_file(self, cursor, setup):
        self.method = "corelib.import_text_file()"
        etllib = EtlLib(self.id, self.name)        
        for datasource in setup["Datasources"]:
            filename = datasource["Source"]
            etllib.import_file(cursor, datasource)
            self.logger.info(f"{self.method}:File sucessfuly imported: {filename}")
            
    def reconcile(self, cursor, setup):
        self.method = "corelib.reconcile()"
        reconlib = ReconLib(self.id, self.name)
        reconlib.process(cursor, setup)
        self.logger.info(f"{self.method}:Recon sucessfuly executed: {self.name}")
               
    def print(self, cursor):
        os.system("cls")        
        for side in range(1,3):
            print(f"Side{side}:")
            cursor.execute(f"select * from tb1{side}")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

    def process(self):
        self.method = "corelib.process()"
        self.logger.info(f"{self.method}: Start method")
        try:
            setuplib = SetupLib()
            setup = setuplib.get_recon_info()
            self.id = setup["Id"]
            self.name = setup["Name"]
            if not setuplib.validate(setup):
                self.logger.info(f"{self.method}: Setup is invalid, aborting this recon")
                return False

            cursor = self.get_cn()
            arealib = AreaLib(self.id, self.name)
            arealib.create_recon_area(cursor, setup)
            self.import_text_file(cursor, setup)
            self.reconcile(cursor, setup)
            self.print(cursor)
            
        except BaseException as err:
            cursor.execute("rollback")
            self.logger.error(f"{self.method}:Fail to reconcile: {str(err)} ")
        cursor.execute("commit")
        self.logger.info(f"{self.method}:End method")