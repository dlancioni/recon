import logging
from sqlite3 import Error
from src.sqllib import SqlLib
from src.baselib import BaseLib
from src.utillib import UtilLib

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

    def aggregate(self, cn, recon):
        """ aggregate and group imported data into temporary table """
        self.method = "reconlib.aggregate()"        
        sql = ""
        grouping_key = ""
        funcs = []
        sqllib = SqlLib()
        if "Function" in recon:
            funcs = recon["Function"]
        field_list = sqllib.get_field_list(self.fields, self.types, funcs)
        sql = ""
        sql += f"insert into {self.tmp1} ({field_list}) "
        sql += f"select {field_list} from {self.tb1}"
        sql += f"group by {grouping_key}" if grouping_key != "" else ""
        cn.execute(sql)
        sql = ""
        sql += f"insert into {self.tmp2} ({field_list}) "
        sql += f"select {field_list} from {self.tb2}"
        sql += f"group by {grouping_key}" if grouping_key != "" else ""
        cn.execute(sql)
        
    def match_key(self, cn, recon):
        """ set the id to parent id on the other side  """
        self.method = "reconlib.match()"
        sqllib = SqlLib()
        rule = recon["Rule"]
        fields_key = recon["Key"]
        matching_key = sqllib.get_sql_key(self.tmp1, self.tmp2, fields_key)
        cn.execute(f"update {self.tmp1} set id_parent = (select id from {self.tmp2} where 1=1 {matching_key})")
        cn.execute(f"update {self.tmp2} set id_parent = (select id from {self.tmp1} where 1=1 {matching_key})")
        cn.execute(f"update {self.tmp1} set id_parent = 0 where id_parent is null")
        cn.execute(f"update {self.tmp2} set id_parent = 0 where id_parent is null")
        cn.execute(f"update {self.tmp1} set recon='{self.name}', rule='{rule}', status='matched' where id_parent <> 0")
        cn.execute(f"update {self.tmp2} set recon='{self.name}', rule='{rule}', status='matched' where id_parent <> 0")
        print(1)
    def compare(self, cn, recon):
        """ compare the records and relegate the status """
        self.method = "reconlib.match()"
        sql = ""
        utillib = UtilLib()
        sqllib = SqlLib()
        rule = recon["Rule"]
        fields_key = recon["Key"]
        fields_compare = recon["Compare"]
        matching_key = sqllib.get_sql_key(self.tmp1, self.tmp2, fields_key)
        fields_key = [(f"{self.tmp1}.{field}") for field in fields_key]
        fields_key = sqllib.get_field_list(fields_key)
        """ keep difference and status in tmp3 """
        tablename = self.tmp3
        for field in fields_compare:
            cn.execute(f"drop table if exists {tablename}")
            field = field.lower()
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
            cn.execute(sql)
            """ stamp the differences in tmp1/tmp2 tables """
            for side in range(1,3):
                temps = self.tmp1 if side == 1 else self.tmp2
                matching_key = sqllib.get_sql_key(temps, self.tmp3, recon["Key"])
                cn.execute(f"alter table {temps} add {field}_diff text default ''")
                cn.execute(f"update {temps} set {field}_diff = (select difference from {self.tmp3} where equality = 0 {matching_key})")
                cn.execute(f"update {temps} set {field}_diff = '' where {field}_diff is null")
                cn.execute(f"update {temps} set status = 'divergent' where {field}_diff <> ''")

    def stamp(self, cn, recon):
        """ update the final status from grouped tmp table to flat table """
        self.method = "reconlib.stamp()"
        utillib = UtilLib()
        sqllib = SqlLib()
        rule = recon["Rule"]
        fields_key = recon["Key"]
        match_info = ["id_parent", "recon", "rule", "status"]
        matching_key1 = sqllib.get_sql_key(self.tb1, self.tmp1, fields_key)
        matching_key2 = sqllib.get_sql_key(self.tb2, self.tmp2, fields_key)
        for field in match_info:
            cn.execute(f"update {self.tb1} set {field} = (select {field} from {self.tmp1} where 1=1 {matching_key1})")
            cn.execute(f"update {self.tb2} set {field} = (select {field} from {self.tmp2} where 1=1 {matching_key2})")

    def process(self, cn, setup):
        """ reconcile the positions """
        self.method = "reconlib.process()"
        utillib = UtilLib()
        try:
            recons = setup["Recons"]
            for recon in recons:
                self.aggregate(cn, recon)
                self.match_key(cn, recon)
                self.compare(cn, recon)
                self.stamp(cn, recon)
        except Error as err:
            message = f"{self.method}: SQL Error -> {str(err)}"
            utillib.log(message)
            self.logger.error(message)
        except BaseException as err:
            self.logger.error(f"{self.method}: General error: {str(err)}")
        finally:
            self.logger.info(f"{self.method}: Done")