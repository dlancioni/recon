import os
import time
import logging
from src.fslib import FsLib
from datetime import datetime
from src.utillib import UtilLib

fslib = FsLib()
utillib = UtilLib()

class MsgLib():

    def __init__(self):
        self.method = ""
        self.logger = logging.getLogger(__name__)
        self.console = "Console"
        self.validation = "Validation"
        self.label = "Label"
        
    def set_time(self, msg):
        now = datetime.now()
        dt = str(time.strftime("%Y-%m-%d %H:%M:%S", now.timetuple()))
        msg = f"{dt}: {msg}"
        return msg

    def get_value(self, session, key, param=[], language=""):
        key = str(key).upper()
        session = str(session).capitalize()
        if language.strip().lower() == "":
            config = fslib.open_json(fslib.get_path_config("app.cfg"))
            language = str(config["catalog"])
        path = fslib.get_path_config(f"catalog_{language}.cfg")
        catalog = fslib.open_json(path)
        value = str(catalog[str(session)][str(key)])
        i = 0
        for item in param:
            i = i + 1
            old = "{" + str(i) + "}"
            new = f"{item}"
            value = value.replace(old, new)
        return value
    
    def print(self, msg):
        msg = self.set_time(msg)
        print(msg)