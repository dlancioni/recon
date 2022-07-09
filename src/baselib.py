import os
from src.utillib import UtilLib

class BaseLib:
    def __init__(self, tb1=""):
        tb1 = tb1
        tmp1 = ""
        tb2 = ""
        tmp2 = ""
        last_error = ""
        cn = ""
        
    def log_info(self, message):
        UtilLib().log(message)
        self.logger.info(f"{self.method}: {message}")

    def log_error(self, message):
        UtilLib().log(message)
        self.logger.info(f"{self.method}: {message}")    