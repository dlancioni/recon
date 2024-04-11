import os
from datetime import datetime
from src.cfglib import ConfigLib
from src.msglib import MsgLib
from src.loglib import LogLib

cfglib = ConfigLib()
msglib = MsgLib()

class DateLib:

    def __init__(self):
        pass

    def to_date(self, string, mask):
        try:
            mask_python = self.get_mask(mask)
            dt = datetime.strptime(string, mask_python)
            return dt            
        except ValueError as err:            
            cat = msglib.get("E2")
            msg = msglib.get("M25", [string, mask])
            raise Exception(msg)
    
    def to_string(self, date, mask):
        mask = self.get_mask(mask)
        dt = datetime.strftime(date, mask)
        return dt    
            
    def get_mask(self, mask=""):
        mask_python = cfglib.get_mask(mask)
        if mask_python.strip() == "":
            raise Exception(msglib.get("M24", [mask]))
        return mask_python
            
    def get_holiday(self, date=""):
        is_holiday = cfglib.get_holiday(date)
        return is_holiday
    
    def is_business_day(self, date=""):
        is_business_day = cfglib.get_holiday(date)
        if date.weekday() == 5 or date.weekday() == 6:
            is_business_day = True
        return is_business_day
    
