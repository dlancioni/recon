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

    def merge_datasources(self, recon):
        f1, t1 = [], []
        f2, t2 = [], []
        datasources = self.tagv(recon, "Datasources", "Dados")
        for datasource in datasources:
            side = self.tagv(datasource, "Side", "Lado")
            fields = self.tagv(datasource, "Fields", "Campos")
            for field in fields:
                if side == 1:                    
                    f1.append(self.tagv(field, "Name", "Nome"))
                    t1.append(self.tagv(field, "Type", "Tipo"))
                else:
                    f2.append(self.tagv(field, "Name", "Nome"))
                    t2.append(self.tagv(field, "Type", "Tipo"))
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
            msg = f"SQL Error -> {str(err)}"
            self.log_error(msg)
            raise Exception(msg)
        except BaseException as err:
            msg = f"General error -> {str(err)}"
            self.log_error(msg)
            raise Exception(msg)
        return fields, types