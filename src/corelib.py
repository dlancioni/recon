import os
import sys
import json
import logging
from src.baselib import BaseLib
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

class CoreLib(BaseLib):

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.logger = logging.getLogger(__name__)

    def process(self, recon):
        self.method = "corelib.process()"
        self.logger.info(f"{self.method}: Start method")
        dblib = DbLib()
        utillib = UtilLib()
        try:
            setuplib = SetupLib()
            setup = setuplib.get_recon_info(recon)
            self.id = setup["Id"]
            self.name = setup["Name"]
            if not setuplib.validate(setup):
                self.logger.info(f"{self.method}: Setup is invalid, aborting this recon")
                return False
            cn = dblib.begin_tran()
            
            super().__init__("abcde")

            arealib = AreaLib(self.id, self.name)
            fields, types = arealib.create_recon_area(cn, setup)

            etllib = EtlLib(self.id, self.name)
            etllib.process(cn, setup)

            reconlib = ReconLib(self.id, self.name, fields, types)
            reconlib.process(cn, setup)

            utillib.print(cn)
            
        except BaseException as err:
            dblib.rollback_tran(cn)
            self.logger.error(f"{self.method}:Fail to reconcile: {str(err)} ")
            return
        dblib.commit_tran(cn)
        self.logger.info(f"{self.method}:End method")