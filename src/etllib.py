import logging
from src.sqllib import SqlLib

class EtlLib:

    def __init__(self):
        self.method = "EtlLib.import_file()"
        self.logger = logging.getLogger(__name__)

    def import_file(self, cn, ds):
        self.logger.info(f"{self.method}: Start reading information")
        sqlib = SqlLib()
        fields = []
        types = [] 
        values = []
        tablename = ds["Table"]
        path = ds["Name"]
        separator = ds["Separator"]
        field_list = ds["Field"]
        type_list = ds["Type"]
        masks = ds["Mask"]
        first = True
        with open(path, "r") as file:
            for line in file.readlines():
                if not first:
                    value_list = line.split(separator)
                    if len(field_list) == len(value_list):
                        for k, v in enumerate(field_list):
                            fields.append(field_list[k])
                            types.append(type_list[k])
                            values.append(value_list[k])
                        fl = sqlib.get_field_list(fields)
                        vl = sqlib.get_value_list(fields, types, values, masks)
                        sql = sqlib.get_sql_insert(tablename, fl, vl)
                        print(sql)
                first = False