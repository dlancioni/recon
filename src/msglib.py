import os
from src.fslib import FsLib
from src.utillib import UtilLib
fslib = FsLib()
utillib = UtilLib()

class MsgLib:

    def __init__(self):
        pass

    def get_value(self, session, key):
        # figure out current language
        path = fslib.get_path_config("app.json")
        config = fslib.open_json(path)
        language = str(config["catalog"])
        # get message
        catalog = f"catalog_{language}.json"
        path = fslib.get_path_config(catalog)
        dictionary = fslib.open_json(path)
        value = str(dictionary[str(session)][str(key)])
        # all good
        return value
    
    def print(self, session, key):
        import time
        from datetime import datetime
        now = datetime.now()
        dt = str(time.strftime("%Y-%m-%d %H:%M:%S", now.timetuple()))
        msg = self.get_value(str(session), str(key))
        msg = f"{dt}: {msg}"
        print(msg)