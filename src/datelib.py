import os
from src.cfglib import ConfigLib
from src.msglib import MsgLib

cfglib = ConfigLib()
msglib = MsgLib()

class DateLib:

    def __init__(self):
        pass
            
    def get_mask(self, mask=""):
        mask_python = cfglib.get_mask(mask)
        if mask_python.strip() == "":
            raise Exception(msglib.get("M24", [mask]))
        return mask_python
            
    def get_holiday(self, date=""):
        is_holiday = cfglib.get_holiday(date)
        return is_holiday