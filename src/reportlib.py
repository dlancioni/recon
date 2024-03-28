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
from src.constlib import const

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

    def print_report(self, type=0, reports="", side=0):
        path = reports[const.REPORT_PATH]
        col_side = 0 if type == 1 else 1
        with open(path, encoding="UTF-8") as file:
            rows = csv.reader(file, delimiter = ';')
            table = PrettyTable(next(rows))            
            for row in rows:
                if int(side) == 1 or int(side) == 2:
                    if int(row[col_side]) == int(side):
                        table.add_row(row)
                else:
                    table.add_row(row)
            print(table)            
    
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
            if label != const.FIELD_STATUS:
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
        filename = f"[{self.name}] [{report}].csv"        
        path = fslib.get_path_report(cfglib.get(4))
        if fslib.is_dir(path) == False:
            raise Exception(msglib.get("V16", [path]))
        path = fslib.join(path, filename)
        tb1 = f"tb{self.id}{1}"
        tb2 = f"tb{self.id}{2}"
        sql = ""
        sql += "select * from "
        sql += "("
        sql += f"select * from {tb1}"
        sql += f" union "
        sql += f"select * from {tb2}"
        sql += f") tb "
        sql += f"order by tb.{const.FIELD_SIDE} "
        rows = dblib.query(cn, sql)
        with open(path, "w", encoding="UTF-8") as f:
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
                        info = "" if str(row[i]) == "None" else str(row[i])
                        line += info + ";"
                line = line[:-1]
                line += "\n"
                f.write(line)
                progress_bar.next()
            progress_bar.finish()
        return [filename, path]
    

    def create_report_synthetic(self, cn):
        loglib = LogLib("Reportlib", "create_report_synthetic")
        sql = ""
        line = ""
        report = msglib.get("L1")
        filename = f"[{self.name}] [{report}].csv"
        path = fslib.get_path_report(cfglib.get(4))
        if fslib.is_dir(path) == False:
            raise Exception(msglib.get("V16", [path]))
        path = fslib.join(path, filename)
        sql += f" select {const.FIELD_SIDE}, {const.FIELD_STATUS}, Total from"
        sql += f" ("
        sql += f" select"
        sql += f" {const.FIELD_SIDE}, {const.FIELD_ID_STATUS}, {const.FIELD_STATUS}, count({const.FIELD_STATUS}) Total"
        sql += f" from tb{self.id}1"
        sql += f" group by {const.FIELD_STATUS}"
        sql += f" union all"
        sql += f" select"
        sql += f" {const.FIELD_SIDE}, {const.FIELD_ID_STATUS}, {const.FIELD_STATUS}, count({const.FIELD_STATUS}) Total"
        sql += f" from tb{self.id}2"
        sql += f" group by {const.FIELD_STATUS}"
        sql += f" ) "
        sql += f" order by {const.FIELD_SIDE}, {const.FIELD_ID_STATUS}"
        rows = dblib.query(cn, sql)
        with open(path, "w", encoding="UTF-8") as f:
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
        return [filename, path]

    def process(self, cn, recon):
        loglib = LogLib("Reportlib", "process")
        reports = []
        try:
            reports.append(self.create_report_synthetic(cn))
            reports.append(self.create_report_analytic(cn))
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
        return reports
    
    