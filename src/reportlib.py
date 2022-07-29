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
        
    def print_csv(self, filename, side=0):
        with open(filename, encoding="UTF-8") as file:
            rows = csv.reader(file, delimiter = ';')
            table = PrettyTable(next(rows))            
            for row in rows:
                if int(side) == 1 or int(side) == 2:
                    if int(row[1]) == int(side):
                        table.add_row(row)
                else:
                    table.add_row(row)
            print(table)

    def print_report(self, reports, index):
        synt = 0
        anal = 1
        index = int(index)
        if index in [0,1,2,12]:
            if index in [0]:
                print(reports[synt])
                self.print_csv(reports[synt])
            if index in [1, 2, 12]:
                print(reports[anal])
                self.print_csv(reports[anal], index)

    def create_report_synthetic(self, cn):
        loglib = LogLib("Reportlib", "create_report_synthetic")
        sql = ""
        line = ""
        path = fslib.get_path_report(cfglib.get(4))
        report = msglib.get("L1")
        file = fslib.join(path, f"[{self.name}] [{report}].csv")
        sql += f" select Side, Status, Total from"
        sql += f" ("
        sql += f" select"
        sql += f" Side, Id_Status, Status, count(Status) Total"
        sql += f" from tb{self.id}1"
        sql += f" group by Status"
        sql += f" union all"
        sql += f" select"
        sql += f" Side, Id_Status, Status, count(Status) Total"
        sql += f" from tb{self.id}2"
        sql += f" group by Status"
        sql += f" ) "
        sql += f" order by Side, Id_Status"
        rows = dblib.query(cn, sql)
        with open(file, "w", encoding="UTF-8") as f:
            msg = msglib.set_time(msglib.get("M9"))
            progress_bar = ShadyBar(msg, max=len(rows))        
            # header
            fields = ["L3", "L6", "L7"]
            line = ""
            for field in fields:
                line += f"{msglib.get(field)};"
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
        fields = ["L8", "L3", "L4", "L5", "L6"]
        for field in fields:
            line += f"{msglib.get(field)};"
        first = len(fields)
        total = len(cn.description)
        for i in range(first, total):
            label = str(cn.description[i][0]).strip()           
            if label != "status":
                line += f"{label};"
        line = line[:-1]
        line += f"\n"
        return line

    def create_report_analytic(self, cn, side=1):
        loglib = LogLib("Reportlib", "create_report_analytic")
        sql = ""
        line = ""
        report = msglib.get("L2")
        label = msglib.get("L3")
        path = fslib.get_path_report(cfglib.get(4))
        filename = fslib.join(path, f"[{self.name}] [{report}].csv")
        tb1 = f"tb{self.id}{1}"
        tb2 = f"tb{self.id}{2}"
        sql = ""
        sql += "select * from "
        sql += "("
        sql += f"select * from {tb1}"
        sql += f" union "
        sql += f"select * from {tb2}"
        sql += ") tb "
        sql += "order by tb.side "        
        rows = dblib.query(cn, sql)
        with open(filename, "w", encoding="UTF-8") as f:
            msg = msglib.set_time(msglib.get("M8"))
            progress_bar = ShadyBar(msg, max=len(rows))
            total = len(cn.description)
            # header
            line = self.create_report_analytic_header(cn)
            f.write(line)
            # contents
            line = ""
            col_id_status = 4
            for row in rows:
                line = ""            
                for i in range(0, total):
                    if i != col_id_status:
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
            reports.append(self.create_report_analytic(cn))
        except Error as err:
            cat = msglib.get("E1")
            msg = f"{cat} -> {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)
        except IOError as err:
            cat = msglib.get("E2")
            msg = f"{cat} -> {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)
        except BaseException as err:
            cat = msglib.get("E3")
            msg = f"{cat} -> {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)
        return reports