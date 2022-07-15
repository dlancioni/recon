import os
import sys
import json
import logging
from sqlite3 import Error
from src.sqllib import SqlLib
from src.msglib import MsgLib
from src.utillib import UtilLib
from src.baselib import BaseLib
from src.loglib import LogLib
from src.dblib import DbLib

sqllib = SqlLib()
utillib = UtilLib()
dblib = DbLib()
msglib = MsgLib()

class AreaLib(BaseLib):

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.logger = logging.getLogger(__name__)

    def merge_datasources(self, recon):
        loglib = LogLib("AreaLib", "merge_datasources")        
        f1, t1 = [], []
        f2, t2 = [], []
        datasources = self.tagv(recon, "Datasources", "Dados")
        for datasource in datasources:
            side = self.tagv(datasource, "Side", "Lado")
            fields = self.tagv(datasource, "Fields", "Campos")
            for field in fields:
                if int(side) == 1:
                    f1.append(self.tagv(field, "Name", "Nome"))
                    t1.append(sqllib.get_field_type(self.tagv(field, "Type", "Tipo")))
                if int(side) == 2:
                    f2.append(self.tagv(field, "Name", "Nome"))
                    t2.append(sqllib.get_field_type(self.tagv(field, "Type", "Tipo")))
        loglib.log(loglib.INFO, str(f1) + str(f2))
        return f1, t1, f2, t2

    def create_recon_area(self, cn, setup):
        loglib = LogLib("AreaLib", "create_recon_area")
        id = setup["Id"]
        status = msglib.get_value(msglib.label, "L13")
        f1, t1, f2, t2 = self.merge_datasources(setup)
        fields, types = sqllib.get_table_structure(f1, t1, f2, t2)
        for side in range(1, 3):
            tb = f"tb{id}{side}"
            tmp = f"tmp{id}{side}"
            dblib.execute(cn, f"drop table if exists {tb}")
            dblib.execute(cn, f"drop table if exists {tmp}")
            dblib.execute(cn, sqllib.get_create_table_definition(tb, fields, types, status))
            dblib.execute(cn, sqllib.get_create_table_definition(tmp, fields, types, status))
        loglib.log(loglib.INFO, "Area created:")
        loglib.log(loglib.INFO, str(fields) + str(types))
        return fields, types
    
    def process(self, cn, recon):
        loglib = LogLib("AreaLib", "process")
        try:
            fields, types = self.create_recon_area(cn, recon)
        except Error as err:
            msg = f"SQL Error -> {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)
        except BaseException as err:
            msg = f"General error -> {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)
        return fields, types