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

    def get_data(self, rows, fields):
        lines = ""
        for field in fields:
            lines += f"{msglib.get_value(msglib.label, field)};"
        lines += f"\n"
        for row in rows:
            for i in range(0, len(fields)):
                lines += str(row[i]) + ";"
            lines += "\n"
        return lines

    def create_report_synthetic(self, cn, file):                
        sql = ""
        sql += f"select "
        sql += f"Recon, Rule, Status, count(Status) Total "
        sql += f"from tmp{self.id}1 "
        sql += f"group by Status"
        rows = dblib.query(cn, sql)
        fields = ["L4", "L5", "L6", "L7"]
        lines = self.get_data(rows, fields)
        self.save_file(file, lines)
        
    def create_report_analytic(self, cn, file, side):
        tb = f"tb{self.id}{side}"
        sql = ""
        sql += f"select "
        sql += f"Recon, Rule, Status "
        sql += f"from {tb} "
        rows = dblib.query(cn, sql)
        fields = ["L4", "L5", "L6"]
        lines = self.get_data(rows, fields)
        self.save_file(file, lines)

    def process(self, cn, recon):
        self.method = "reportlib.process()"
        try:
            """ path to generate reports """
            path = fslib.get_path_report(cfglib.get_config("path_report"))
            """ create synthetic report (totals) """
            report = msglib.get_value(msglib.label, "L1")
            file = fslib.join(path, f"[{report}] [{self.name}].csv")
            self.create_report_synthetic(cn, file)
            """ create analytic report """
            report = msglib.get_value(msglib.label, "L2")            
            label = msglib.get_value(msglib.label, "L3")
            for side in range(1, 3):
                file = fslib.join(path, f"[{report}] [{label} {side}] [{self.name}].csv")
                self.create_report_analytic(cn, file, side)
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