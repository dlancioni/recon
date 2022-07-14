import logging
from sqlite3 import Error
from progress.bar import ShadyBar
from src.baselib import BaseLib
from src.sqllib import SqlLib
from src.fslib import FsLib
from src.dblib import DbLib
from src.utillib import UtilLib
from src.msglib import MsgLib
from src.loglib import LogLib

dblib = DbLib()
fslib = FsLib()
sqlib = SqlLib()
msglib = MsgLib()
utillib = UtilLib()

class EtlLib(BaseLib):

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.app_path = ""
        self.logger = logging.getLogger(__name__)
        
    def count(self, file):
        lines = 0
        with open(file, "r") as file:
            lines = len(file.readlines())
        return lines

    def import_file(self, cn, ds):
        loglib = LogLib("EtlLib", "import_file")
        sql = ""       
        side = self.tagv(ds, "Side", "Lado")
        path = self.tagv(ds, "Path", "Caminho")
        file = self.tagv(ds, "File", "Arquivo")
        fields = self.tagv(ds, "Fields", "Campos")
        separator = self.tagv(ds, "Separator", "Separador")
        tb = f"tb{self.id}{side}"        
        path = fslib.get_path_file(path, file)
        first = True
        error_count = 0
        rows_affected = 0
        rows_imported = 0
        fl = sqlib.get_field_list(fields)
        count = self.count(path)
        msg = msglib.get_value(msglib.console, "M5", [self.tagv(ds, "File", "Arquivo")])
        msg = msglib.set_time(msg)
        progress_bar = ShadyBar(msg, max=count-1)
        loglib.log(loglib.INFO, f"File info: [{path}] [{file}] [{separator}] [{count}] [{str(fl)}]")
        with open(path, "r") as file:
            for line in file.readlines():
                if not first and str(line.strip()) != "":
                    values = line.split(separator)
                    for field in fields:
                        position = int(field["Id"]) -1
                        field["Value"] = values[position]
                    vl = sqlib.get_value_list(fields)
                    sql = sqlib.get_sql_insert(tb, fl, vl)
                    try:
                        rows_affected = dblib.execute(cn, sql)
                        rows_imported += 1
                        progress_bar.next()
                    except Error as err:
                        error_count += 1                                                   
                        loglib.log(loglib.INFO, f"Error to manipulate data [{sql}]: {str(err)}")
                first = False
        progress_bar.finish()
        loglib.log(loglib.INFO, f"File sucessfully imported")
    def process(self, cn, recon):
        loglib = LogLib("EtlLib", "process")
        try:
            datasources = self.tagv(recon, "Datasources", "Dados")
            for datasource in datasources:
                self.import_file(cn, datasource)
        except Error as err:
            msg = f"SQL Error -> {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)
        except IOError as err:
            msg = f"File manipulation error -> {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)
        except BaseException as err:
            msg = f"General error -> {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)