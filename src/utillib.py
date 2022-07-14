import os
from src.dblib import DbLib

dblib = DbLib()

class UtilLib:

    def __init__(self):
        pass

    def get_result(self, cn, id):
        result  = ["Results", "", ""]
        console = ["Console", "", ""]
        result[1] = dblib.query(cn, f"select * from tb{id}1", False)
        result[2] = dblib.query(cn, f"select * from tb{id}2", False)
        console[1] = dblib.query(cn, f"select * from tb{id}1", True)
        console[2] = dblib.query(cn, f"select * from tb{id}2", True)        
        return result, console

    def cls(self):
        os.system("cls||clear")