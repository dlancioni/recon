import os
import sys
import json
import logging
from sqlite3 import Error
from src.sqllib import SqlLib
from src.utillib import UtilLib

class AreaLib:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.logger = logging.getLogger(__name__)

    def merge_datasources(self, setup):
        f1, t1 = [], []
        f2, t2 = [], []
        for datasource in setup["Datasources"]:
            side = datasource["Side"]
            fields = datasource["Fields"]
            for field in fields:
                if side == 1:
                    f1.append(field["Name"])
                    t1.append(field["Type"])
                else:
                    f2.append(field["Name"])
                    t2.append(field["Type"])
        return f1, t1, f2, t2                    

    def create_recon_area(self, cn, setup):
        sqllib = SqlLib()
        id = setup["Id"]        
        f1, t1, f2, t2 = self.merge_datasources(setup)
        fields, types = sqllib.get_table_structure(f1, t1, f2, t2)
        for side in range(1, 3):
            tb = f"tb{id}{side}"
            tmp = f"tmp{id}{side}"
            cn.execute(f"drop table if exists {tb}")
            cn.execute(f"drop table if exists {tmp}")
            cn.execute(sqllib.get_create_table_definition(tb, fields, types))
            cn.execute(sqllib.get_create_table_definition(tmp, fields, types))
        return fields, types
    
    def process(self, cn, setup):
        """ consolidate layout definition and create recon area (tables) """
        self.method = "arealib.process()"
        utillib = UtilLib()
        try:
            fields, types = self.create_recon_area(cn, setup)
        except Error as err:
            message = f"{self.method}: SQL Error -> {str(err)}"
            utillib.log(message)
            self.logger.error(message)
        except BaseException as err:
            self.logger.error(f"{self.method}: General error: {str(err)}")
            self.logger.error(message)            
        finally:
            self.logger.info(f"{self.method}: Done")
        return fields, types