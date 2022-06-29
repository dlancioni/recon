import os
import sys
import json
import logging
from src.sqllib import SqlLib

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


    def create_recon_area(self, cursor, setup):
        self.method = "arealib.create_recon_area()"
        sqllib = SqlLib()
        id = setup["Id"]        
        f1, t1, f2, t2 = self.merge_datasources(setup)
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
        return fields, types