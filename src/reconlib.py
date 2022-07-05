import logging
from sqlite3 import Error
from src.sqllib import SqlLib
from src.baselib import BaseLib
from src.utillib import UtilLib
from src.dblib import DbLib

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
        
    def prepare(self, cn, recon):
        """ keep common information in class level """
        self.method = "reconlib.prepare()"
        dblib = DbLib()
        sqllib = SqlLib()
        for field in recon["Fields"]:
            if str(field["Type"]).strip().lower() == "key":
                self.field_key.append(str(field["Name"]).strip().lower())
            if str(field["Type"]).strip().lower() == "compare":
                self.field_compare.append(str(field["Name"]).strip().lower())                

    def aggregate(self, cn, recon):
        """ aggregate, group and order imported data into temporary table """
        self.method = "reconlib.aggregate()"        
        sql = ""
        funcs = []
        sqllib = SqlLib()
        dblib = DbLib()
        grouping_key = sqllib.get_field_key(recon["Fields"])
        field_list = sqllib.get_field_list(recon["Fields"], False)
        value_list = sqllib.get_field_list(recon["Fields"], True)
        for side in range(1, 3):
            tb = self.tb1 if side == 1 else self.tb2
            tmp = self.tmp1 if side == 1 else self.tmp2
            sql = ""
            sql += f"insert into {tmp} ({field_list}) "
            sql += f"select {value_list} from {tb} "
            sql += f"group by {grouping_key} " if grouping_key != "" else ""
            sql += f"order by {grouping_key} " if grouping_key != "" else ""
            dblib.execute(cn, sql)
        
    def match_key(self, cn, recon):
        """ set id as id_parent plus recon details in both sides  """
        self.method = "reconlib.match()"
        sqllib = SqlLib()
        dblib = DbLib()
        rule = recon["Rule"]
        matching_key = sqllib.get_sql_key(self.tmp1, self.tmp2, recon["Fields"])
        for side in range(1, 3):
            tmp1 = self.tmp1 if side == 1 else self.tmp2
            tmp2 = self.tmp2 if side == 1 else self.tmp1
            sql = ""
            sql += f"update {tmp1} set "
            sql += f"recon='{self.name}', "
            sql += f"rule='{rule}', "
            sql += f"status='matched', "
            sql += f"id_parent = {tmp2}.id "
            sql += f"from {tmp2} "
            sql += f"where 1=1 "
            sql += f"{matching_key}"
            dblib.execute(cn, sql)

    def compare(self, cn, recon):
        """ compare the records and relegate the status from matched to divergent """
        self.method = "reconlib.compare()"
        sql = ""
        fields_key = ""
        utillib = UtilLib()
        sqllib = SqlLib()
        dblib = DbLib()
        rule = recon["Rule"]
        matching_key = sqllib.get_sql_key(self.tmp1, self.tmp2, recon["Fields"])
        """ create temp table  to compare fields """
        for field in self.field_key:
                fields_key += f"{self.tmp1}.{field}, "
        fields_key = fields_key.strip()[:-1].lower()
        """ keep difference and status in tmp3 """
        tablename = self.tmp3
        for field in self.field_compare:
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
            sql += f" where {self.tmp1}.status = 'matched'"
            sql += f" {matching_key}"
            dblib.execute(cn, sql)

    def stamp(self, cn, recon):
        """ update the final status from grouped tmp table to flat table """
        self.method = "reconlib.stamp()"
        utillib = UtilLib()
        sqllib = SqlLib()
        dblib = DbLib()
        """ stamp the differences from tmp3 in tmp1/tmp2 tables """
        for field in self.field_compare:
            for side in range(1,3):
                temps = self.tmp1 if side == 1 else self.tmp2
                matching_key = sqllib.get_sql_key(temps, self.tmp3, recon["Fields"])
                sql = f"alter table {temps} add {field}_diff text default ''"
                dblib.execute(cn, sql)
                sql = ""
                sql += f"update {temps} set "
                sql += f"status = 'divergent', "
                sql += f"{field}_diff = {self.tmp3}.difference "
                sql += f"from {self.tmp3} "
                sql += f"where {self.tmp3}.equality = 0 "
                sql += f"{matching_key}"
                dblib.execute(cn, sql)
        """ stamp the differences from tmps in tbs """
        rule = recon["Rule"]
        match_info = ["id_parent", "recon", "rule", "status"]
        matching_key1 = sqllib.get_sql_key(self.tb1, self.tmp1, recon["Fields"])
        matching_key2 = sqllib.get_sql_key(self.tb2, self.tmp2, recon["Fields"])
        for field in match_info:
            sql = f"update {self.tb1} set {field} = {self.tmp1}.{field} from {self.tmp1} where 1=1 {matching_key1}"
            dblib.execute(cn, sql)
            sql = f"update {self.tb2} set {field} = {self.tmp2}.{field} from {self.tmp2} where 1=1 {matching_key2}"
            dblib.execute(cn, sql)            

    def process(self, cn, setup):
        """ reconcile the positions """
        self.method = "reconlib.process()"
        utillib = UtilLib()
        try:
            recons = setup["Recons"]
            for recon in recons:
                self.prepare(cn, recon)
                self.aggregate(cn, recon)
                self.match_key(cn, recon)
                self.compare(cn, recon)
                self.stamp(cn, recon)
        except Error as err:
            message = f"{self.method}: SQL Error -> {str(err)}"
            utillib.log(message)
            self.logger.error(message)
        except BaseException as err:
            message = f"{self.method}: General error -> {str(err)}"
            utillib.log(message)
            self.logger.error(message)
        finally:
            self.logger.info(f"{self.method}: Done")