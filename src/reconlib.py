import logging
from sqlite3 import Error
from src.dblib import DbLib
from src.msglib import MsgLib
from src.sqllib import SqlLib
from src.baselib import BaseLib
from src.utillib import UtilLib
from src.cfglib import ConfigLib
from progress.bar import ShadyBar
from src.loglib import LogLib
from src.setuplib import SetupLib
from src.constlib import const

dblib = DbLib()
msglib = MsgLib()
sqllib = SqlLib()
utillib = UtilLib()
cfglib = ConfigLib()
setuplib = SetupLib()

class ReconLib(BaseLib):

    def __init__(self, id, name, fields, types):
        self.logger = logging.getLogger(__name__)
        self.id = id
        self.name = name
        self.fields = fields
        self.types = types
        self.tb1 = f"tb{self.id}1"
        self.tb2 = f"tb{self.id}2"
        self.tmp1 = f"tmp{self.id}1"
        self.tmp2 = f"tmp{self.id}2"
        self.tmp3 = f"tmp{self.id}3"
        self.field_key = []
        self.field_compare = []
        self.field_with_diff = []
        self.matched = ""
        self.divergent = ""
        self.orphan = ""
        self.rule_count = 0
        
    def prepare(self, cn, rule):
        loglib = LogLib("ReconLib", "prepare")
        field_name = ""
        self.matched = msglib.get("L11")
        self.divergent = msglib.get("L12")
        self.orphan = msglib.get("L13")
        for field in setuplib.tag_value(rule, "Fields"):
            field_name = setuplib.tag_value(field, "Name")
            field_name = f"[{field_name}]"
            if setuplib.tag_value(field, "Type").lower() in ["key", "chave"]:
                self.field_key.append(field_name)
            if setuplib.tag_value(field, "Type").lower() in ["compare", "comparar"]:
                self.field_compare.append(field_name)
            # stamp the type in recon definition    
            index = self.fields.index(field_name.replace("[", "").replace("]", ""))
            field["Datatype"] = self.types[index]
        self.rule_count += 1
        loglib.log(loglib.INFO, f"Fiekd Key: {str(self.field_key)}")
        loglib.log(loglib.INFO, f"Fiekd Compare: {str(self.field_compare)}")
        self.progress_bar.next()

    def aggregate(self, cn, rule):
        loglib = LogLib("ReconLib", "aggregate")
        sql = ""
        funcs = []
        rows_affected = 0
        field = setuplib.tag_name(rule, "Fields")
        grouping_key = sqllib.get_field_key(rule[field])
        field_list = sqllib.get_field_list(rule[field], False)
        value_list = sqllib.get_field_list(rule[field], True)
        for side in range(1, 3):
            tb = self.tb1 if side == 1 else self.tb2
            tmp = self.tmp1 if side == 1 else self.tmp2
            sql = f"delete from {tmp}"
            rows_affected = dblib.execute(cn, sql)
            sql = ""
            sql += f"insert into {tmp} ({field_list}) "
            sql += f"select {value_list}  "
            sql += f"from {tb} "
            sql += f"where status <> '{self.matched}' "
            sql += f"group by {grouping_key} " if grouping_key != "" else ""
            sql += f"order by {grouping_key} " if grouping_key != "" else ""
            rows_affected = dblib.execute(cn, sql)
        loglib.log(loglib.INFO, f"Data successfuly aggregated")
        self.progress_bar.next()

    def match_key(self, cn, rule):
        loglib = LogLib("ReconLib", "match_key")
        rows_affected = 0
        rule_name = setuplib.tag_value(rule, "Rule")
        field = setuplib.tag_name(rule, "Fields")
        matching_key = sqllib.get_sql_key(self.tmp1, self.tmp2, rule[field])
        for side in range(1, 3):
            tmp1 = self.tmp1 if side == 1 else self.tmp2
            tmp2 = self.tmp2 if side == 1 else self.tmp1
            sql = ""
            sql += f"update {tmp1} set "
            sql += f"recon='{self.name}', "
            sql += f"rule='{rule_name}', "
            sql += f"id_status='{const.STATUS_MATCHED}',"
            sql += f"status = '{self.matched}', "
            sql += f"id_parent = {tmp2}.id "
            sql += f"from {tmp2} "
            sql += f"where {tmp1}.status = '{self.orphan}' "
            sql += f"{matching_key}"
            rows_affected = dblib.execute(cn, sql)
        loglib.log(loglib.INFO, f"Match key successfuly completed")
        self.progress_bar.next()
        
    def get_tolerance(self, rule, fieldname):
        tolerance = 0
        fieldname = fieldname.strip().lower().replace("[", "").replace("]", "")
        field_name = setuplib.tag_name(rule, "Fields")
        fields = rule[field_name]
        for field in fields:
            field_name = setuplib.tag_value(field, "Name")
            rule_type = setuplib.tag_value(field, "Type")
            if rule_type.strip().lower() in ["compare", "comparar"]:
                if field_name.strip().lower() == fieldname:
                    if field["Datatype"].strip().lower() == "decimal":                
                        tol = setuplib.tag_value(field, "Tolerance")
                        if tol.strip() != "":
                            tolerance = float(tol)
                            break
        return tolerance

    def compare(self, cn, rule):
        loglib = LogLib("ReconLib", "compare")
        sql = ""
        fields_key = ""
        count = 0
        rows_affected = 0
        field = setuplib.tag_name(rule, "Fields")
        matching_key = sqllib.get_sql_key(self.tmp1, self.tmp2, rule[field])
        """ create temp table  to compare fields """
        for field in self.field_key:
            fields_key += f"{self.tmp1}.{field}, "
        fields_key = fields_key.strip()[:-1]
        """ keep difference and status in tmp3 """
        for field in self.field_compare:
            count += 1
            tablename = self.tmp3            
            tablename += str(count)           
            tolerance = self.get_tolerance(rule, field)
            sql = f"drop table if exists {tablename}"
            dblib.execute(cn, sql)
            sql = ""
            tmp1 = f"{self.tmp1}.{field}"
            tmp2 = f"{self.tmp2}.{field}"
            sql += f" create table {tablename} as"
            sql += f" select"
            sql += f" {fields_key}"
            sql += f", ({tmp1} || '/' || {tmp2}) difference"            
            if tolerance == 0:
                sql += f", ({tmp1} = {tmp2}) equality"
            else:    
                sql += f", (abs({tmp1} - {tmp2}) <= {tolerance}) equality"            
            sql += f" from {self.tmp1}, {self.tmp2}"
            sql += f" where {self.tmp1}.status = '{self.matched}'"
            sql += f" {matching_key}"
            rows_affected = dblib.execute(cn, sql)
        loglib.log(loglib.INFO, f"Field comparison successfuly completed")
        self.progress_bar.next()        
            
    def stamp_tmp(self, cn, rule):
        loglib = LogLib("ReconLib", "stamp_tmp")
        count = 0
        rows_affected = 0
        field_name = ""
        label = msglib.get("L10")
        for field in self.field_compare:
            count += 1
            tmp3 = f"{self.tmp3}{str(count)}"
            for side in range(1,3):
                _field = setuplib.tag_name(rule, "Fields")
                temps = self.tmp1 if side == 1 else self.tmp2
                matching_key = sqllib.get_sql_key(temps, tmp3, rule[_field])
                field_name = sqllib.field_diff(field, label)
                loglib.log(loglib.INFO, f"Stamping field (alter table): {field_name}")
                self.field_with_diff.append(field_name)
                if self.rule_count == 1:
                    sql = f"alter table {temps} add {field_name} text default ''"
                    rows_affected = dblib.execute(cn, sql)
                sql = ""
                sql += f"update {temps} set "
                sql += f"id_status='{const.STATUS_DIVERGENT}',"
                sql += f"status = '{self.divergent}', "
                sql += f"{field_name} = {tmp3}.difference "
                sql += f"from {tmp3} "
                sql += f"where {tmp3}.equality = 0 "
                sql += f"{matching_key}"
                rows_affected = dblib.execute(cn, sql)
            sql = f"drop table if exists {tmp3}"
            rows_affected = dblib.execute(cn, sql)
        self.field_with_diff = list(dict.fromkeys(self.field_with_diff))
        loglib.log(loglib.INFO, f"Fields with difference: {str(self.field_with_diff)}")
        self.progress_bar.next()

    def stamp_tb(self, cn, rule):
        loglib = LogLib("ReconLib", "stamp_tb")
        field_list = ""
        rows_affected = 0
        """ stamp the differences from tmps in tbs """
        field = setuplib.tag_name(rule, "Fields")
        match_result = ["Id_Parent", "Recon", "Rule", "Id_Status", "Status"]
        compare_result = self.field_with_diff
        matching_key1 = sqllib.get_sql_key(self.tb1, self.tmp1, rule[field])
        matching_key2 = sqllib.get_sql_key(self.tb2, self.tmp2, rule[field])
        """ stamp key information in final table """
        for side in range(1, 3):
            field_list = ""
            for field in match_result:
                tb = self.tb1 if side == 1 else self.tb2
                tmp = self.tmp1 if side == 1 else self.tmp2
                matching_key = matching_key1 if side == 1 else matching_key2
                field_list += f"{field} = {tmp}.{field}, "
            field_list = field_list.strip()[:-1]
            sql = f"update {tb} set {field_list} from {tmp} where 1=1 {matching_key}"
            rows_affected = dblib.execute(cn, sql)
        loglib.log(loglib.INFO, f"Key info stamped in final tables")
        """ stamp compare information in final table """
        for side in range(1, 3):
            for field in compare_result:
                tb = self.tb1 if side == 1 else self.tb2
                tmp = self.tmp1 if side == 1 else self.tmp2
                matching_key = matching_key1 if side == 1 else matching_key2
                if self.rule_count == 1:
                    sql = f"alter table {tb} add {field} text default ''"
                    rows_affected = dblib.execute(cn, sql)
                sql = f"update {tb} set {field} = {tmp}.{field} from {tmp} where 1=1 {matching_key}"
                rows_affected = dblib.execute(cn, sql)
        loglib.log(loglib.INFO, f"Compare info stamped in final tables")
        self.progress_bar.next()
                
    def drop_tmp(self, cn):
        loglib = LogLib("ReconLib", "drop_tmp")
        for side in range(1, 3):
            sql = f"drop table if exists tmp{self.id}{side}"
            rows_affected = dblib.execute(cn, sql)
            sql = f"alter table tb{self.id}{side} drop column Id_Parent"
            rows_affected = dblib.execute(cn, sql)            

    def process(self, cn, recon):
        loglib = LogLib("ReconLib", "process")
        try:
            recon = setuplib.tag_value(recon, "Recon")
            for rule in recon:
                rule_name = setuplib.tag_value(rule, "Rule")
                loglib.log(loglib.INFO, f"Processing rule: {rule_name}")
                msg = msglib.set_time(msglib.get("M6", [rule_name]))
                self.progress_bar = ShadyBar(msg, max=6)
                self.prepare(cn, rule)
                self.aggregate(cn, rule)
                self.match_key(cn, rule)
                self.compare(cn, rule)
                self.stamp_tmp(cn, rule)
                self.stamp_tb(cn, rule)
                self.progress_bar.finish()
            self.drop_tmp(cn)
        except Error as err:
            cat = msglib.get("E1")
            msg = f"{cat} {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)
        except BaseException as err:
            cat = msglib.get("E3")
            msg = f"{cat} {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)