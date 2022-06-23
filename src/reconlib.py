import logging
from src.sqllib import SqlLib

class ReconLib:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.logger = logging.getLogger(__name__)
        
    def aggregate(self):
        """ aggregate and group imported data into temporary table """
        self.method = "reconlib.aggregate()"
        sql = ""
        sqlib = SqlLib()
        
    def match(self):
        """ set the id to parent id on the other side  """
        self.method = "reconlib.match()"
        sql = ""
        sqlib = SqlLib()
        
    def compare(self):
        """ compare the records and relegate the status """
        self.method = "reconlib.match()"
        sql = ""
        sqlib = SqlLib()
        
    def stamp(self):
        """ update the final status from grouped tmp table to flat table """
        self.method = "reconlib.stamp()"
        sql = ""
        sqlib = SqlLib()        

    """ reconcile the positions """
    def process(self, cursor, setup):
        self.method = "reconlib.reconcile()"
        sql = ""
        sqlib = SqlLib()
        try:
            pass                
        except:
            self.logger.error(f"{self.method}:Last SQL command {sql}")
            self.logger.error(f"{self.method}:Error importing the file {path}")