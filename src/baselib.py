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
        self.logger.info(f"{self.method}: {message}")

    def log_error(self, message):
        self.logger.info(f"{self.method}: {message}")
        
    def tagv(self, doc, tag_en="", tag_pt=""):
        tag_en = tag_en.capitalize().strip()
        tag_pt = tag_pt.capitalize().strip()
        value = doc[tag_en] if tag_en in doc else doc[tag_pt]
        return value        