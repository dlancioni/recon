import logging
from sqlite3 import Error
from src.baselib import BaseLib
from src.sqllib import SqlLib
from src.fslib import FsLib
from src.dblib import DbLib
from src.utillib import UtilLib
from src.msglib import MsgLib

sqlib = SqlLib()
dblib = DbLib()
fslib = FsLib()
utillib = UtilLib()
msglib = MsgLib()

class EtlLib(BaseLib):

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.app_path = ""
        self.logger = logging.getLogger(__name__)

    def import_file(self, cn, ds):
        self.method = "etllib.import_file()"
        sql = ""       
        side = ds["Side"]
        path = ds["Path"]
        file = ds["File"]
        fields = ds["Fields"]
        separator = ds["Separator"]
        tb = f"tb{self.id}{side}"        
        path = fslib.get_path_file(path, file)
        first = True
        error_count = 0
        rows_affected = 0
        rows_imported = 0
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
                        rows_affected = dblib.execute(cn, sql)
                        rows_imported += 1
                    except Error as err:
                        error_count += 1                           
                        self.log_error(f"Error to manipulate data [{sql}]: {str(err)}")
                first = False
        
    def process(self, cn, recon):
        """ import positions """
        self.method = "etllib.process()"
        try:
            datasources = recon["Datasources"]
            for datasource in datasources:
                msglib.print(msglib.get_value(msglib.console, "M7", [datasource['File']]))
                self.import_file(cn, datasource)
        except Error as err:
            msg = f"SQL Error -> {str(err)}"
            self.log_error(msg)
            raise Exception(msg)
        except IOError as err:
            msg = f"File manipulation error -> {str(err)}"
            self.log_error(msg)
            raise Exception(msg)
        except BaseException as err:
            msg = f"General error -> {str(err)}"
            self.log_error(msg)
            raise Exception(msg)