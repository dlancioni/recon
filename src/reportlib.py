import os
import sys
import json
import logging
from src.baselib import BaseLib
from src.dblib import DbLib
from src.fslib import FsLib
from src.sqllib import SqlLib
from src.cfglib import ConfigLib
from src.utillib import UtilLib
from src.msglib import MsgLib

dblib = DbLib()
fslib = FsLib()
sqllib = SqlLib()
utillib = UtilLib()
cfglib = ConfigLib()
msglib = MsgLib()

class ReportLib(BaseLib):

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.logger = logging.getLogger(__name__)

    def save_file(self, file, lines):
        with open(file, "w") as f:
            f.write(lines)

    def create_report_sintetic(self, cn, file):                
        line = ""
        line += f"{msglib.get_value(msglib.label, 'L1')};" # recon
        line += f"{msglib.get_value(msglib.label, 'L2')};" # rule
        line += f"{msglib.get_value(msglib.label, 'L3')};" # status
        line += f"{msglib.get_value(msglib.label, 'L4')};" # total
        line += f"\n"
        sql = f"select Recon, Rule, Status, count(Status) Total from tmp{self.id}1 group by Status"
        rows = dblib.query(cn, sql)
        for row in rows:
            line += str(row[0]) + ";" # Recon
            line += str(row[1]) + ";" # Rule
            line += str(row[2]) + ";" # Satus
            line += str(row[3]) + ";" # Total
            line += "\n"
        self.save_file(file, line)

    def process(self, cn, recon):
        self.method = "reportlib.process()"
        try:
            """ create output files """
            path = fslib.get_path_report(cfglib.get_config("path_report"))

            """ create sintetic report (totals) """
            file = fslib.join(path, f"[Sintetico][{self.name}].csv")
            self.create_report_sintetic(cn, file)

            """ create analytic report (side 1) """
            f1 = fslib.join(path, f"[Analitico][Lado 1][{self.name}].csv")
            
            """ create analytic report (side 2) """
            f2 = fslib.join(path, f"[Analitico][Lado 2][{self.name}].csv")
            
            
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