import logging
from sqlite3 import Error
from src.sqllib import SqlLib
from src.baselib import BaseLib
from src.utillib import UtilLib
from src.dblib import DbLib
from src.msglib import MsgLib

dblib = DbLib()
sqllib = SqlLib()
utillib = UtilLib()
msglib = MsgLib()

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
        
    def prepare(self, cn, recon):
        """ keep common information in class level """
        self.method = "reconlib.prepare()"
        field_name = ""
        for field in self.tagv(recon, "Fields", "Campos"):
            field_name = self.tagv(field, "Name", "Nome")
            field_name = f"[{field_name}]"
            if self.tagv(field, "Tipo", "Type").lower() in ["key", "chave"]:
                self.field_key.append(field_name)
            if self.tagv(field, "Tipo", "Type").lower() in ["compare", "comparar"]:
                self.field_compare.append(field_name)

    def aggregate(self, cn, recon):
        """ aggregate, group and order imported data into temporary table """
        self.method = "reconlib.aggregate()"        
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
            sql = ""
            sql += f"insert into {tmp} ({field_list}) "
            sql += f"select {value_list} from {tb} "
            sql += f"group by {grouping_key} " if grouping_key != "" else ""
            sql += f"order by {grouping_key} " if grouping_key != "" else ""
            rows_affected = dblib.execute(cn, sql)
        
    def match_key(self, cn, recon):
        """ set id as id_parent plus recon details in both sides  """
        self.method = "reconlib.match_key()"
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
            sql += f"status = 'Matched', "
            sql += f"id_parent = {tmp2}.id "
            sql += f"from {tmp2} "
            sql += f"where 1=1 "
            sql += f"{matching_key}"
            rows_affected = dblib.execute(cn, sql)

    def compare(self, cn, recon):
        """ compare the records and relegate the status from matched to divergent """
        self.method = "reconlib.compare()"
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
            sql += f" where {self.tmp1}.status = 'Matched'"
            sql += f" {matching_key}"
            rows_affected = dblib.execute(cn, sql)
            
    def stamp_tmp(self, cn, recon):
        """ stamp the differences from tmp3 in tmp1/tmp2 tables """        
        self.method = "reconlib.stamp_tmp()"
        count = 0
        rows_affected = 0
        field_name = ""
        for field in self.field_compare:
            count += 1
            tmp3 = f"{self.tmp3}{str(count)}"
            for side in range(1,3):
                _field = self.tagf(recon, "Fields", "Campos")                
                temps = self.tmp1 if side == 1 else self.tmp2
                matching_key = sqllib.get_sql_key(temps, tmp3, recon[_field])
                field_name = sqllib.field_diff(field)
                self.field_with_diff.append(field_name)
                sql = f"alter table {temps} add {field_name} text default ''"
                rows_affected = dblib.execute(cn, sql)
                sql = ""
                sql += f"update {temps} set "
                sql += f"status = 'Divergent', "
                sql += f"{field_name} = {tmp3}.difference "
                sql += f"from {tmp3} "
                sql += f"where {tmp3}.equality = 0 "
                sql += f"{matching_key}"
                rows_affected = dblib.execute(cn, sql)
        self.field_with_diff = list(dict.fromkeys(self.field_with_diff))

    def stamp_tb(self, cn, recon):
        """ update the final status from grouped tmp table to flat table """
        self.method = "reconlib.stamp_tb()"
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
        """ stamp compare information in final table """
        for side in range(1, 3):
            for field in compare_result:
                tb = self.tb1 if side == 1 else self.tb2
                tmp = self.tmp1 if side == 1 else self.tmp2
                matching_key = matching_key1 if side == 1 else matching_key2
                sql = f"alter table {tb} add {field} text default ''"
                rows_affected = dblib.execute(cn, sql)
                sql = f"update {tb} set {field} = {tmp}.{field} from {tmp} where 1=1 {matching_key}"
                rows_affected = dblib.execute(cn, sql)

    def process(self, cn, recon):
        """ reconcile the positions """
        self.method = "reconlib.process()"
        try:
            recons = self.tagv(recon, "Recon", "Conciliacao")
            for recon in recons:
                msglib.print(msglib.get_value(msglib.console, "M8", [self.tagv(recon, "Rule", "Regra")]))
                self.prepare(cn, recon)
                self.aggregate(cn, recon)
                msglib.print(msglib.get_value(msglib.console, "M9"))
                self.match_key(cn, recon)
                msglib.print(msglib.get_value(msglib.console, "M10"))
                self.compare(cn, recon)
                msglib.print(msglib.get_value(msglib.console, "M11"))
                self.stamp_tmp(cn, recon)
                self.stamp_tb(cn, recon)
                msglib.print(msglib.get_value(msglib.console, "M12"))
        except Error as err:
            msg = f"SQL Error -> {str(err)}"
            self.log_error(msg)
            raise Exception(msg)
        except BaseException as err:
            msg = f"General error -> {str(err)}"
            self.log_error(msg)
            raise Exception(msg)