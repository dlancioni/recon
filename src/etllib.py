import logging
from sqlite3 import Error
from src.baselib import BaseLib
from src.sqllib import SqlLib
from src.fslib import FsLib
from src.dblib import DbLib
from src.utillib import UtilLib

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
        rows_affected = 0
        rows_imported = 0
        utillib = UtilLib()
        try:
            self.log(f"Start importing delimited text file -> Side: {side} Path: {path}, Separator: {separator}")
            fl = sqlib.get_field_list(fields)
            self.log(f"Importing fields -> {str(fl)}")
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
                            rows_affected = dblib.execute(cn, sql)
                            rows_imported += 1
                        except Error as err:
                            error_count += 1                           
                            message = f"Error to manipulate data [{sql}]: {str(err)}"
                            utillib.log(message)
                            self.logger.error(message)
                            
                    first = False
        except IOError as err:
            message = f"File manipulation error {path} -> {str(err)}"
            utillib.log(message)
            self.logger.error(message)
        except BaseException as err:
            message = f"General error -> {str(err)}"
            utillib.log(message)
            self.logger.error(message)
        finally:
            message = f"File sucessfuly imported -> {str(rows_imported)} rows imported"
            utillib.log(message)
            self.logger.error(message)

    def process(self, cn, setup):
        """ import positions """
        self.method = "etllib.process()"
        utillib = UtilLib()        
        try:
            datasources = setup["Datasources"]
            message = f"Start processing datasources -> {str(len(datasources))} datasource(s)"
            utillib.log(message)
            self.logger.info(message)
            for datasource in datasources:
                message = f"Processing datasource -> {datasource['Name']}"
                utillib.log(message)
                self.logger.info(message)                
                self.import_file(cn, datasource)
        except BaseException as err:
            message = f"General error -> {str(err)}"
            utillib.log(message)
            self.logger.error(message)
        finally:
            message = f"Datasource(s) sucessfuly processed"
            utillib.log(message)
            self.logger.info(message)