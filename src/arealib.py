import os
import sys
import json
import logging
from sqlite3 import Error
from src.sqllib import SqlLib
from src.utillib import UtilLib
from src.baselib import BaseLib

class AreaLib(BaseLib):

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
        utillib = UtilLib()
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
    
    def process(self, cn, recon):
        """ consolidate layout definition and create recon area (tables) """
        self.method = "arealib.process()"
        utillib = UtilLib()
        try:
            fields, types = self.create_recon_area(cn, recon)
        except Error as err:
            self.log_error(f"SQL Error -> {str(err)}")
        except BaseException as err:
            self.log_error(f"General error -> {str(err)}")
        finally:
            pass
        return fields, types