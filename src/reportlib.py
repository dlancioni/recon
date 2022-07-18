import os
import csv
import sys
import json
import shutil
import logging
from prettytable import from_csv
from prettytable import PrettyTable
from sqlite3 import Error
from src.baselib import BaseLib
from src.dblib import DbLib
from src.fslib import FsLib
from src.sqllib import SqlLib
from src.cfglib import ConfigLib
from src.utillib import UtilLib
from src.msglib import MsgLib
from src.loglib import LogLib
from progress.bar import ShadyBar

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
        
    def print_csv(self, filename):
        
        pt = None  # to avoid it vanished at end of block...
        with open(filename, encoding="UTF-8") as file:
            data = csv.reader(file, delimiter = ';')
            table = PrettyTable(next(data))
            for row in data:
                table.add_row(row) 
            print(table)
        
    def print_report(self, reports, index):
        index = int(index)
        if index in [0,1,2,12]:
            utillib.cls()
            if index in [0, 1, 2]:
                print(reports[index])
                self.print_csv(reports[index])
            if index == 12:
                print(reports[1])
                self.print_csv(reports[1])
                print(reports[2])
                self.print_csv(reports[2])        

    def create_report_synthetic(self, cn):
        loglib = LogLib("Reportlib", "create_report_synthetic")
        sql = ""
        line = ""
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
        with open(file, "w", encoding="UTF-8") as f:
            msg = msglib.set_time(msglib.get_value(msglib.console, "M9"))
            progress_bar = ShadyBar(msg, max=len(rows))        
            # header
            fields = ["L3", "L4", "L5", "L6", "L7"]
            line = ""
            for field in fields:
                line += f"{msglib.get_value(msglib.label, field)};"
            line = line[:-1]
            line += f"\n"
            f.write(line)
            # contents            
            line = ""
            for row in rows:
                line = ""
                for i in range(0, len(fields)):
                    line += str(row[i]) + ";"
                line = line[:-1]
                line += "\n"
                f.write(line)
                progress_bar.next()
            progress_bar.finish()
        return file
    
    def create_report_analytic_header(self, cn):
        loglib = LogLib("Reportlib", "create_report_analytic_header")
        sql = ""        
        line = ""
        tb = f"tb{self.id}1"
        sql += f"select * from {tb}"
        rows = dblib.query(cn, sql)
        fields = ["L8", "L9", "L4", "L5", "L6"]
        for field in fields:
            line += f"{msglib.get_value(msglib.label, field)};"
        first = len(fields)
        total = len(cn.description)
        for i in range(first, total):
            label = str(cn.description[i][0]).strip()
            line += f"{label};"
        line = line[:-1]
        line += f"\n"
        return line

    def create_report_analytic(self, cn, side):
        loglib = LogLib("Reportlib", "create_report_analytic")
        sql = ""
        line = ""
        tb = f"tb{self.id}{side}"        
        report = msglib.get_value(msglib.label, "L2")
        label = msglib.get_value(msglib.label, "L3")
        path = fslib.get_path_report(cfglib.get_config("path_report"))
        filename = fslib.join(path, f"[{self.name}] [{report}] [{label} {side}].csv")
        sql = f"select * from {tb}"
        rows = dblib.query(cn, sql)
        with open(filename, "w", encoding="UTF-8") as f:
            msg = msglib.set_time(msglib.get_value(msglib.console, "M8", [side]))
            progress_bar = ShadyBar(msg, max=len(rows))
            total = len(cn.description)
            # header
            line = self.create_report_analytic_header(cn)
            f.write(line)
            # contents
            line = ""
            for row in rows:
                line = ""            
                for i in range(0, total):
                    line += str(row[i]) + ";"
                line = line[:-1]
                line += "\n"
                f.write(line)
                progress_bar.next()
            progress_bar.finish()
        return filename

    def process(self, cn, recon):
        loglib = LogLib("Reportlib", "process")
        reports = []
        try:
            reports.append(self.create_report_synthetic(cn))
            for side in range(1, 3):
                reports.append(self.create_report_analytic(cn, side))
        except Error as err:
            cat = msglib.get_value(msglib.exception, "E1")
            msg = f"{cat} -> {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)
        except IOError as err:
            cat = msglib.get_value(msglib.exception, "E2")
            msg = f"{cat} -> {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)
        except BaseException as err:
            cat = msglib.get_value(msglib.exception, "E3")
            msg = f"{cat} -> {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)
        return reports