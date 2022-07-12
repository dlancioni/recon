import os
import time
import logging
from datetime import datetime
from src.fslib import FsLib
from src.utillib import UtilLib
from src.baselib import BaseLib

fslib = FsLib()
utillib = UtilLib()

class MsgLib(BaseLib):

    def __init__(self):
        self.method = ""
        self.logger = logging.getLogger(__name__)
        self.console = "Console"
        self.validation = "Validation"
        self.label = "Label"

    def get_value(self, session, key, param=[]):
        path = fslib.get_path_config("app.json")
        config = fslib.open_json(path)
        language = str(config["catalog"])
        catalog = f"catalog_{language}.json"
        path = fslib.get_path_config(catalog)
        dictionary = fslib.open_json(path)
        value = str(dictionary[str(session)][str(key)])
        i = 0
        for item in param:
            i = i + 1
            old = "{" + str(i) + "}"
            new = f"{item}"
            value = value.replace(old, new)
        return value
    
    def print(self, msg):
        now = datetime.now()
        dt = str(time.strftime("%Y-%m-%d %H:%M:%S", now.timetuple()))
        msg = f"{dt}: {msg}"
        print(msg)