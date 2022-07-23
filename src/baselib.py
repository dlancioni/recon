import os
from src.utillib import UtilLib
from src.msglib import MsgLib

class BaseLib:
    def __init__(self, tb1=""):
        tb1 = tb1
        tb2 = ""

    def tagfv(self, doc, tag_en, tag_pt):
        f, v = "", ""
        tag_en = tag_en.capitalize().strip()
        tag_pt = tag_pt.capitalize().strip()
        if tag_en in doc:
            f = tag_en
            v = doc[tag_en]
            return f, v
        if tag_pt in doc:
            f = tag_pt
            v = doc[tag_pt]
        return f, v

    def tagf(self, doc, tag_en="", tag_pt="", mandatory=True):
        f, v = self.tagfv(doc, tag_en, tag_pt)
        if mandatory == True:
            if f == "":
                msglib = MsgLib()
                msg = f"{tag_en}/{tag_pt}"
                msg = msglib.get_value(msglib.validation, "M5", [msg])
                raise Exception(msg)
        return f

    def tagv(self, doc, tag_en="", tag_pt="", mandatory=True):
        f, v = self.tagfv(doc, tag_en, tag_pt)
        return v