import logging
from src.sqllib import SqlLib

class ReconLib:

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

    def aggregate(self, cn, recon):
        """ aggregate and group imported data into temporary table """
        self.method = "reconlib.aggregate()"        
        sql = ""
        grouping_key = ""
        sqllib = SqlLib()
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
        
    def match(self, cn):
        """ set the id to parent id on the other side  """
        self.method = "reconlib.match()"
        sql = f"update {self.tmp1} set id_parent = (select id from {self.tmp2} where {key}"
        cn.execute(sql)        
        sql = f"update {self.tmp2} set id_parent = (select id from {self.tmp1} where {key}"
        cn.execute(sql)
        
    def compare(self):
        """ compare the records and relegate the status """
        self.method = "reconlib.match()"
        sql = ""
        sqllib = SqlLib()
        
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

        except BaseException as err:
            self.logger.error(f"{self.method}:Last SQL command {str(err)}")