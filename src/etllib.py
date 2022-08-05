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
from src.setuplib import SetupLib
from src.cfglib import ConfigLib

dblib = DbLib()
fslib = FsLib()
sqlib = SqlLib()
msglib = MsgLib()
utillib = UtilLib()
setuplib = SetupLib()
cfglib = ConfigLib()

class EtlLib(BaseLib):

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.logger = logging.getLogger(__name__)
        
    def count(self, file):
        lines = 0
        with open(file, "r") as file:
            lines = len(file.readlines())
        return lines
    
    def get_path(self, ds):
        if setuplib.tag_value(ds, "Path", False) == "":
            path = fslib.get_path_file(cfglib.get(3))
        else:
            path = setuplib.tag_value(ds, "Path", False)
        if fslib.is_dir(path) == False:
            raise Exception(msglib.get("V19", [path]))        
        filename = setuplib.tag_value(ds, "File")
        path = fslib.join(path, filename)        
        if fslib.is_file(path) == False:
            raise IOError(msglib.get("V4", [path]))
        return path, filename

    def import_file(self, cn, ds):
        loglib = LogLib("EtlLib", "import_file")
        sql = ""       
        side = setuplib.tag_value(ds, "Side")       
        fields = setuplib.tag_value(ds, "Fields")
        separator = setuplib.tag_value(ds, "Separator")
        start = int(setuplib.tag_value(ds, "Start"))
        tb = f"tb{self.id}{side}"
        path, filename = self.get_path(ds)
        first = True
        error_count = 0
        rows_affected = 0
        rows_imported = 0
        row = 0
        fl = sqlib.get_field_list(fields)
        count = self.count(path)
        msg = msglib.get("M5", [setuplib.tag_value(ds, "File")])
        msg = msglib.set_time(msg)
        progress_bar = ShadyBar(msg, max=count-1)
        loglib.log(loglib.INFO, f"File info: [{path}] [{filename}] [{separator}] [{count}] [{str(fl)}]")
        with open(path, "r", encoding='UTF-8') as file:
            for line in file.readlines():
                row += 1
                if (row >= start) and (str(line.strip()) != ""):

                    values = line.split(separator)

                    for field in fields:

                        position = int(field["Id"]) -1
                        value = str(values[position]).strip()

                        if value == "":
                            field_type = default_value = setuplib.tag_value(field, "Type")
                            if field_type.lower() in ["integer", "inteiro", "decimal"]:
                                value = 0

                        default_value = setuplib.tag_value(field, "Default Value")
                        if default_value != "":
                            value = default_value
                        field["Value"] = value

                    vl = sqlib.get_value_list(fields)
                    sql = sqlib.get_sql_insert(tb, fl, vl)

                    try:
                        rows_affected = dblib.execute(cn, sql)
                        rows_imported += 1
                        progress_bar.next()
                    except Error as err:
                        pass                        
                        error_count += 1                                                   
                        loglib.log(loglib.INFO, f"Error to manipulate data [{sql}]: {str(err)}")

        progress_bar.finish()
        loglib.log(loglib.INFO, f"File sucessfully imported")
        
    def process(self, cn, recon):
        loglib = LogLib("EtlLib", "process")
        try:
            datasources = setuplib.tag_value(recon, "Datasources")
            for datasource in datasources:
                self.import_file(cn, datasource)
        except Error as err:
            cat = msglib.get("E1")
            msg = f"{cat} {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)
        except IOError as err:
            cat = msglib.get("E2")
            msg = f"{cat} {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)
        except BaseException as err:
            cat = msglib.get("E3")
            msg = f"{cat} {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)