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
    
    def persist(self, cn, fields):
        loglib = LogLib("EtlLib", "persist")        
        try:
            field_list = sqlib.get_field_list(fields)
            value_list = sqlib.get_value_list(fields)
            sql = sqlib.get_sql_insert(self.table_name, field_list, value_list)
            rows_affected = dblib.execute(cn, sql)
        except Error as err:
            pass                        
            loglib.log(loglib.INFO, f"Error to manipulate data [{sql}]: {str(err)}")
    
    def get_path(self, datasource):
        if setuplib.tag_value(datasource, "Path", False) == "":
            path = fslib.get_path_file(cfglib.get(3))
        else:
            path = setuplib.tag_value(datasource, "Path", False)
        if fslib.is_dir(path) == False:
            raise Exception(msglib.get("V19", [path]))        
        filename = setuplib.tag_value(datasource, "File")
        path = fslib.join(path, filename)        
        if fslib.is_file(path) == False:
            raise IOError(msglib.get("V4", [path]))
        return path, filename
    
    def empty_value(self, field_def, field_value=""):
        if field_value.strip() == "":
            field_type = setuplib.tag_value(field_def, "Type")
            if field_type.strip().lower() in ["integer", "inteiro", "decimal"]:
                field_value = 0
        return field_value
    
    def default_value(self, field_def, field_value=""):
        default_value = setuplib.tag_value(field_def, "Default Value")
        if default_value.strip() != "":
            field_value = str(default_value)
        return field_value
    
    def format_data(self, field_def, field_value):
        field_value = self.empty_value(field_def, field_value)
        field_value = self.default_value(field_def, field_value)
        return field_value
    
    def import_text_file(self, cn, datasource):
        row = 0
        field_value = ""
        path, filename = self.get_path(datasource)
        count = self.count(path)
        fields = self.fields
        start = int(setuplib.tag_value(datasource, "Start"))
        delimiter = setuplib.tag_value(datasource, "Delimiter")
        progress_bar = ShadyBar(msglib.set_time(msglib.get("M5", [filename])), max=count-1)        
        with open(path, "r", encoding='UTF-8') as file:
            for line in file.readlines():
                row += 1
                if (row >= start) and (str(line.strip()) != ""):
                    values = line.split(delimiter)
                    for field in fields:
                        position = int(field[setuplib.tag_name(field, "Position")]) -1
                        field_value = str(values[position]).strip()
                        field["Value"] = self.format_data(field, field_value)
                    self.persist(cn, fields)
                    progress_bar.next()
        progress_bar.finish()

    def process(self, cn, recon):
        loglib = LogLib("EtlLib", "process")
        try:
            datasources = setuplib.tag_value(recon, "Datasources")
            for datasource in datasources:
                type = setuplib.tag_value(datasource, "Type")
                side = setuplib.tag_value(datasource, "Side")
                self.table_name = f"tb{self.id}{side}"
                self.fields = setuplib.tag_value(datasource, "Fields")
                if type in ["Delimited", "Delimitado"]:
                    self.import_text_file(cn, datasource)
                loglib.log(loglib.INFO, f"File sucessfully imported")

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