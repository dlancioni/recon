import logging
from sqlite3 import Error
from src.sqllib import SqlLib
from src.fslib import FsLib

class EtlLib:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.logger = logging.getLogger(__name__)
        
    def get_file(self, path=""):
        fslib = FsLib()
        if path.find("etc:") > -1:
            tmp = path.split(":")
            path = fslib.get_dir_etc(tmp[1])
        return path

    def import_file(self, cursor, ds):
        self.method = "etllib.import_file()"
        sql = ""
        sqlib = SqlLib()
        side = ds["Side"]
        tablename = f"tb{self.id}{side}"
        path = self.get_file(ds["File"])
        separator = ds["Separator"]
        field_list = ds["Field"]
        type_list = ds["Type"]
        masks = ds["Mask"]
        first = True
        error_count = 0
        try:
            with open(path, "r") as file:
                for line in file.readlines():
                    if not first:
                        value_list = line.split(separator)
                        if len(field_list) == len(masks):
                            fields, types, values = [], [], []
                            for k, v in enumerate(field_list):
                                fields.append(field_list[k])
                                types.append(type_list[k])
                                values.append(value_list[k])
                            fl = sqlib.get_field_list(fields)
                            vl = sqlib.get_value_list(fields, types, values, masks)
                            sql = sqlib.get_sql_insert(tablename, fl, vl)
                            try:
                                cursor.execute(sql)
                            except Error as err:
                                error_count += 1
                                self.logger.error(f"{self.method}: Error to manipulate data [{sql}]: {str(err)}")
                        else:
                            self.logger.error(f"{self.method}: Fields, Types and Masks are not the same size {path}")
                            return False
                    first = False
        except IOError as err:
            self.logger.error(f"{self.method}: Error to manipulate file {path}: {str(err)}")
        except BaseException as err:
            self.logger.error(f"{self.method}: General error {path}: {str(err)}")
        finally:
            self.logger.info(f"{self.method}: Done")
                