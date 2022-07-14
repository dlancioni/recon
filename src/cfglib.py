import os
from src.fslib import FsLib
from src.utillib import UtilLib

fslib = FsLib()
utillib = UtilLib()

class ConfigLib:

    def __init__(self):
        pass

    def get_config(self, key):
        path = fslib.get_path_config("app.cfg")
        config = fslib.open_json(path)
        value = str(config[key])
        value = value.strip()
        return value