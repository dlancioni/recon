import logging
from src.sqllib import SqlLib

class EtlLib:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def import_file(self, cursor, ds):
        self.method = "EtlLib.import_file()"        
        self.logger.info(f"{self.method}: Start method")
        sqlib = SqlLib()
        tablename = ds["Table"]
        path = ds["Name"]
        separator = ds["Separator"]
        field_list = ds["Field"]
        type_list = ds["Type"]
        masks = ds["Mask"]
        first = True
        try:
            with open(path, "r") as file:
                for line in file.readlines():
                    if not first:
                        value_list = line.split(separator)
                        if len(field_list) == len(value_list) and len(field_list) == len(masks):
                            fields, types, values = [], [], []
                            for k, v in enumerate(field_list):
                                fields.append(field_list[k])
                                types.append(type_list[k])
                                values.append(value_list[k])
                            fl = sqlib.get_field_list(fields)
                            vl = sqlib.get_value_list(fields, types, values, masks)
                            sql = sqlib.get_sql_insert(tablename, fl, vl)
                            cursor.execute(sql)
                        else:
                            self.logger.error(f"{self.method}:Fields, Types and Masks are not the same size {path}")
                            return False
                    first = False
        except:
            self.logger.error(f"{self.method}:Last SQL command {sql}")
            self.logger.error(f"{self.method}:Error importing the file {path}")
        self.logger.info(f"{self.method}:End method")