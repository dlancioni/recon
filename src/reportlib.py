import os
import sys
import json
import shutil
import logging
from sqlite3 import Error
from src.baselib import BaseLib
from src.dblib import DbLib
from src.fslib import FsLib
from src.sqllib import SqlLib
from src.cfglib import ConfigLib
from src.utillib import UtilLib
from src.msglib import MsgLib
from src.loglib import LogLib

dblib = DbLib()
fslib = FsLib()
msglib = MsgLib()
sqllib = SqlLib()
utillib = UtilLib()
cfglib = ConfigLib()

class ReportLib(BaseLib):

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.logger = logging.getLogger(__name__)

    def save_file(self, file, lines):
        saved = False
        error = []
        try:
            with open(file, "w") as f:
                f.write(lines)
            saved = True
            error = []
        except BaseException as err:
            saved = False
            error = [err.errno, err.strerror]
        return saved, error

    def create_report_synthetic(self, cn):
        sql = ""        
        lines = ""
        path = fslib.get_path_report(cfglib.get_config("path_report"))
        report = msglib.get_value(msglib.label, "L1")
        file = fslib.join(path, f"[{self.name}] [{report}].csv")
        
        sql += f" select * from"
        sql += f" ("
        sql += f" select"
        sql += f" 1 Side,"
        sql += f" Recon, Rule, Status, count(Status) Total"
        sql += f" from tb{self.id}1"
        sql += f" group by Status"
        sql += f"  union all"
        sql += f" select"
        sql += f" 2 Side,"
        sql += f" Recon, Rule, Status, count(Status) Total"
        sql += f" from tb{self.id}2"
        sql += f" group by Status"
        sql += f" ) "
        sql += f" order by Side, Recon, Rule, Status"        
        rows = dblib.query(cn, sql)
        fields = ["L3", "L4", "L5", "L6", "L7"]
        for field in fields:
            lines += f"{msglib.get_value(msglib.label, field)};"
        lines += f"\n"
        for row in rows:
            for i in range(0, len(fields)):
                lines += str(row[i]) + ";"
            lines += "\n"
        status, error = self.save_file(file, lines)
        if status == False:
            if error[0] == 13:
                msg = msglib.get_value(msglib.console, "M7", [file])
                raise Exception(msg)
        return file    
        
    def create_report_analytic(self, cn, side):
        report = msglib.get_value(msglib.label, "L2")
        label = msglib.get_value(msglib.label, "L3")
        path = fslib.get_path_report(cfglib.get_config("path_report"))
        file = fslib.join(path, f"[{self.name}] [{report}] [{label} {side}].csv")
        lines = ""
        sql = ""
        tb = f"tb{self.id}{side}"
        sql += f"select "
        sql += f"* "
        sql += f"from {tb} "
        rows = dblib.query(cn, sql)
        fields = ["L8", "L9", "L4", "L5", "L6"]
        for field in fields:
            lines += f"{msglib.get_value(msglib.label, field)};"
        first = len(fields)
        total = len(cn.description)
        for i in range(first, total):
            label = str(cn.description[i][0]).strip()
            lines += f"{label};"
        lines += f"\n"
        for row in rows:
            for i in range(0, total):
                lines += str(row[i]) + ";"
            lines += "\n"
        status, error = self.save_file(file, lines)
        if status == False:
            if error[0] == 13:
                msg = msglib.get_value(msglib.console, "M7", [file])
                raise Exception(msg)
        return file            

    def process(self, cn, recon):
        self.method = "reportlib.process()"
        reports = []
        try:
            reports.append(self.create_report_synthetic(cn))
            for side in range(1, 3):
                reports.append(self.create_report_analytic(cn, side))
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
        return reports