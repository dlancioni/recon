import os
from src.fslib import FsLib
from src.utillib import UtilLib

fslib = FsLib()
utillib = UtilLib()

class ConfigLib:

    def __init__(self):
        pass
    
    def get(self, id=0):
        path = fslib.get_path_config("app.cfg")
        app = fslib.open_json(path)
        for config in app["AppConfig"]:
            if config["Key"] == str(id):
                return str(config["Value"]).strip()
            
    def get_mask(self, mask=""):
        path = fslib.get_path_config("mask.cfg")
        app = fslib.open_json(path)
        for config in app["Masks"]:
            if str(config["Key"]).lower() == str(mask).lower():
                return str(config["Value"]).strip()        
        return ""

    def get_holiday(self, date=""):
        mask = self.get_mask("yyyy-mm-dd")
        date = date.strftime(mask)
        path = fslib.get_path_config("holiday.cfg")
        app = fslib.open_json(path)
        for config in app["Holidays"]:
            if config["Key"] == str(date):
                return True
        return False