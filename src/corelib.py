import os
import sys
import json
import logging
from src.dblib import DbLib
from src.fslib import FsLib
from src.sqllib import SqlLib
from src.etllib import EtlLib
from src.arealib import AreaLib
from src.utillib import UtilLib
from src.setuplib import SetupLib
from src.reconlib import ReconLib

fslib = FsLib()
sqllib = SqlLib()
utillib = UtilLib()

class CoreLib:

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.logger = logging.getLogger(__name__)

    def import_text_file(self, cursor, setup):
        etllib = EtlLib(self.id, self.name)        
        for datasource in setup["Datasources"]:
            filename = datasource["Source"]
            etllib.import_file(cursor, datasource)
            
    def reconcile(self, cursor, setup):
        reconlib = ReconLib(self.id, self.name)
        reconlib.process(cursor, setup)

    def process(self):
        self.method = "corelib.process()"
        self.logger.info(f"{self.method}: Start method")
        dblib = DbLib()
        utillib = UtilLib()
        try:
            setuplib = SetupLib()
            setup = setuplib.get_recon_info()
            self.id = setup["Id"]
            self.name = setup["Name"]
            if not setuplib.validate(setup):
                self.logger.info(f"{self.method}: Setup is invalid, aborting this recon")
                return False

            cn = dblib.begin_tran()
            arealib = AreaLib(self.id, self.name)
            arealib.create_recon_area(cn, setup)
            self.import_text_file(cn, setup)
            self.reconcile(cn, setup)
            utillib.print(cn)
            
        except BaseException as err:
            dblib.rollback_tran(cn)
            self.logger.error(f"{self.method}:Fail to reconcile: {str(err)} ")
        dblib.commit_tran(cn)
        self.logger.info(f"{self.method}:End method")