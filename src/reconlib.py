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

dblib = DbLib()
msglib = MsgLib()
sqllib = SqlLib()
utillib = UtilLib()
cfglib = ConfigLib()

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
        
    def prepare(self, cn, recon):
        loglib = LogLib("ReconLib", "prepare")
        field_name = ""
        self.matched = msglib.get_value(msglib.label, "L11")
        self.divergent = msglib.get_value(msglib.label, "L12")
        self.orphan = msglib.get_value(msglib.label, "L13")        
        for field in self.tagv(recon, "Fields", "Campos"):
            field_name = self.tagv(field, "Name", "Nome")
            field_name = f"[{field_name}]"
            if self.tagv(field, "Tipo", "Type").lower() in ["key", "chave"]:
                self.field_key.append(field_name)
            if self.tagv(field, "Tipo", "Type").lower() in ["compare", "comparar"]:
                self.field_compare.append(field_name)
        self.rule_count += 1
        loglib.log(loglib.INFO, f"Fiekd Key: {str(self.field_key)}")
        loglib.log(loglib.INFO, f"Fiekd Compare: {str(self.field_compare)}")

    def aggregate(self, cn, recon):
        loglib = LogLib("ReconLib", "aggregate")
        sql = ""
        rows_affected = 0
        funcs = []
        field = self.tagf(recon, "Fields", "Campos")
        grouping_key = sqllib.get_field_key(recon[field])
        field_list = sqllib.get_field_list(recon[field], False)
        value_list = sqllib.get_field_list(recon[field], True)
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
        
    def match_key(self, cn, recon):
        loglib = LogLib("ReconLib", "match_key")
        rows_affected = 0
        rule = self.tagv(recon, "Rule", "Regra")
        field = self.tagf(recon, "Fields", "Campos")
        matching_key = sqllib.get_sql_key(self.tmp1, self.tmp2, recon[field])
        for side in range(1, 3):
            tmp1 = self.tmp1 if side == 1 else self.tmp2
            tmp2 = self.tmp2 if side == 1 else self.tmp1
            sql = ""
            sql += f"update {tmp1} set "
            sql += f"recon='{self.name}', "
            sql += f"rule='{rule}', "
            sql += f"status = '{self.matched}', "
            sql += f"id_parent = {tmp2}.id "
            sql += f"from {tmp2} "
            sql += f"where 1=1 "
            sql += f"{matching_key}"
            rows_affected = dblib.execute(cn, sql)
        loglib.log(loglib.INFO, f"Match key successfuly completed")

    def compare(self, cn, recon):
        loglib = LogLib("ReconLib", "compare")
        sql = ""
        fields_key = ""
        count = 0
        rows_affected = 0
        rule = self.tagv(recon, "Rule", "Regra")
        field = self.tagf(recon, "Fields", "Campos")
        matching_key = sqllib.get_sql_key(self.tmp1, self.tmp2, recon[field])
        """ create temp table  to compare fields """
        for field in self.field_key:
            fields_key += f"{self.tmp1}.{field}, "
        fields_key = fields_key.strip()[:-1]
        """ keep difference and status in tmp3 """
        for field in self.field_compare:
            count += 1
            tablename = self.tmp3            
            tablename += str(count)
            sql = f"drop table if exists {tablename}"
            dblib.execute(cn, sql)
            sql = ""
            tmp1 = f"{self.tmp1}.{field}"
            tmp2 = f"{self.tmp2}.{field}"
            sql += f" create table {tablename} as"
            sql += f" select"
            sql += f" {fields_key}"
            sql += f", ({tmp1} || '/' || {tmp2}) difference"
            sql += f", ({tmp1} = {tmp2}) equality"
            sql += f" from {self.tmp1}, {self.tmp2}"
            sql += f" where {self.tmp1}.status = '{self.matched}'"
            sql += f" {matching_key}"
            rows_affected = dblib.execute(cn, sql)
        loglib.log(loglib.INFO, f"Field comparison successfuly completed")
            
    def stamp_tmp(self, cn, recon):
        loglib = LogLib("ReconLib", "stamp_tmp")
        count = 0
        rows_affected = 0
        field_name = ""
        label = msglib.get_value(msglib.label, "L10")
        for field in self.field_compare:
            count += 1
            tmp3 = f"{self.tmp3}{str(count)}"
            for side in range(1,3):
                _field = self.tagf(recon, "Fields", "Campos")                
                temps = self.tmp1 if side == 1 else self.tmp2
                matching_key = sqllib.get_sql_key(temps, tmp3, recon[_field])
                field_name = sqllib.field_diff(field, label)
                loglib.log(loglib.INFO, f"Stamping field (alter table): {field_name}")
                self.field_with_diff.append(field_name)
                if self.rule_count == 1:
                    sql = f"alter table {temps} add {field_name} text default ''"
                    rows_affected = dblib.execute(cn, sql)
                sql = ""
                sql += f"update {temps} set "
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

    def stamp_tb(self, cn, recon):
        loglib = LogLib("ReconLib", "stamp_tb")
        field_list = ""
        rows_affected = 0
        """ stamp the differences from tmps in tbs """
        rule = self.tagv(recon, "Rule", "Regra")
        field = self.tagf(recon, "Fields", "Campos")
        match_result = ["Id_Parent", "Recon", "Rule", "Status"]
        compare_result = self.field_with_diff
        matching_key1 = sqllib.get_sql_key(self.tb1, self.tmp1, recon[field])
        matching_key2 = sqllib.get_sql_key(self.tb2, self.tmp2, recon[field])
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
            recons = self.tagv(recon, "Recon", "Conciliacao")
            for recon in recons:                
                rule_name = self.tagv(recon, "Rule", "Regra")
                msg = msglib.set_time(msglib.get_value(msglib.console, "M6", [rule_name]))                
                loglib.log(loglib.INFO, f"Processing rule: {rule_name}")
                progress_bar = ShadyBar(msg, max=5)                
                progress_bar.next()
                self.prepare(cn, recon)
                self.aggregate(cn, recon)
                progress_bar.next()
                self.match_key(cn, recon)
                progress_bar.next()
                self.compare(cn, recon)
                progress_bar.next()
                self.stamp_tmp(cn, recon)
                self.stamp_tb(cn, recon)
                progress_bar.next()
                progress_bar.finish()
            self.drop_tmp(cn)                
        except Error as err:
            msg = f"SQL Error -> {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)
        except BaseException as err:
            msg = f"General error -> {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)