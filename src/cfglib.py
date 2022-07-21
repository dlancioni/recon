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