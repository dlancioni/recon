import os
import time
import logging
from src.fslib import FsLib
from datetime import datetime
from src.utillib import UtilLib
from src.cfglib import ConfigLib

fslib = FsLib()
utillib = UtilLib()
cfglib = ConfigLib()

class MsgLib():

    def __init__(self):
        self.method = ""
        self.logger = logging.getLogger(__name__)

    def set_time(self, msg):
        now = datetime.now()
        dt = str(time.strftime("%Y-%m-%d %H:%M:%S", now.timetuple()))
        msg = f"{dt}: {msg}"
        return msg
    
    def print(self, msg):
        msg = self.set_time(msg)
        print(msg)    
        
    def get(self, code, param=[], language=""):
        code = str(code).upper()
        if language.strip().lower() == "":
            language = cfglib.get(7)
        path = fslib.get_path_config(f"catalog.cfg")
        catalog = fslib.open_json(path)
        for item in catalog["Catalog"]:
            if item["code"] == code:
                value = item[language]
                break
        i = 0
        for item in param:
            i = i + 1
            old = "%" + str(i)
            new = f"{item}"
            value = value.replace(old, new)
        return value