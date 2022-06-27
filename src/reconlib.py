import logging
from sqlite3 import Error
from src.sqllib import SqlLib
from src.baselib import BaseLib

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
        sql = f"update {self.tmp1} set recon='{self.name}', rule='{rule}', status='Matched', id_parent = (select id from {self.tmp2} where 1 = 1 {matching_key})"
        cn.execute(sql)
        sql = f"update {self.tmp2} set recon='{self.name}', rule='{rule}', status='Matched', id_parent = (select id from {self.tmp1} where 1 = 1 {matching_key})"
        cn.execute(sql)

    def compare(self, cn, recon):
        """ compare the records and relegate the status """
        self.method = "reconlib.match()"
        sql = ""
        sqllib = SqlLib()
        rule = recon["Rule"]
        fields_key = recon["Key"]
        fields_compare = recon["Compare"]
        field_list = sqllib.get_field_list(fields_key)
        matching_key = sqllib.get_sql_key(self.tmp1, self.tmp2, fields_key)
        tablename = self.tmp3       
        for field in fields_compare:
            cn.execute(f"drop table if exists {tablename}")
            sql = ""
            tmp1 = f"{self.tmp1}.{field}"
            tmp2 = f"{self.tmp2}.{field}"
            sql += f" create table {tablename} as select"
            sql += f" {field_list}"
            sql += f", ({tmp1} + '/' + {tmp2}) difference"
            sql += f", ({tmp1} = {tmp2}) equals"
            sql += f" from {self.tmp1}, {self.tmp2}"
            sql += f" where 1 = 1 {matching_key}"
            sql = sql.lower()
            cn.execute(sql)
        
    def stamp(self):
        """ update the final status from grouped tmp table to flat table """
        self.method = "reconlib.stamp()"
        sql = ""
        sqllib = SqlLib()

    def process(self, cn, setup):
        """ reconcile the positions """
        self.method = "reconlib.process()"
        try:
            recons = setup["Recons"]
            for recon in recons:
                self.aggregate(cn, recon)
                self.match_key(cn, recon)
                self.compare(cn, recon)
        except Error as err:
            self.logger.error(f"{self.method}: Error to manipulate data [{sql}]: {str(err)}")
        except BaseException as err:
            self.logger.error(f"{self.method}: General error: {str(err)}")
        finally:
            self.logger.info(f"{self.method}: Done")