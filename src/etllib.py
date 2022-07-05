import logging
from sqlite3 import Error
from src.baselib import BaseLib
from src.sqllib import SqlLib
from src.fslib import FsLib
from src.dblib import DbLib

class EtlLib(BaseLib):

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

    def import_file(self, cn, ds):
        self.method = "etllib.import_file()"
        sql = ""
        sqlib = SqlLib()
        dblib = DbLib()        
        side = ds["Side"]
        tb = f"tb{self.id}{side}"
        path = self.get_file(ds["File"])
        separator = ds["Separator"]
        fields = ds["Fields"]
        first = True
        error_count = 0
        try:
            fl = sqlib.get_field_list(fields)
            with open(path, "r") as file:
                for line in file.readlines():
                    if not first:
                        values = line.split(separator)
                        for field in fields:
                            position = int(field["Id"]) -1
                            field["Value"] = values[position]
                        vl = sqlib.get_value_list(fields)
                        sql = sqlib.get_sql_insert(tb, fl, vl)
                        try:
                            dblib.execute(cn, sql)
                        except Error as err:
                            error_count += 1
                            self.logger.error(f"{self.method}: Error to manipulate data [{sql}]: {str(err)}")
                    first = False
        except IOError as err:
            message = f"{self.method}: File manipulation error {path} -> {str(err)}"
            utillib.log(message)
            self.logger.error(message)            
        except BaseException as err:
            message = f"{self.method}: General error -> {str(err)}"
            utillib.log(message)
            self.logger.error(message)
        finally:
            self.logger.info(f"{self.method}: Done")

    def process(self, cn, setup):
        """ import positions """
        self.method = "etllib.process()"
        try:
            datasources = setup["Datasources"]
            for datasource in datasources:
                self.import_file(cn, datasource)
        except BaseException as err:
            self.logger.error(f"{self.method}: General error: {str(err)}")
        finally:
            self.logger.info(f"{self.method}: Done")
