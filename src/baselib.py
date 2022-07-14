import os
from src.utillib import UtilLib

class BaseLib:
    def __init__(self, tb1=""):
        tb1 = tb1
        tmp1 = ""
        tb2 = ""
        tmp2 = ""
        last_error = ""
        cn = ""

    def tagfv(self, doc, tag_en="", tag_pt=""):
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
        
    def tagf(self, doc, tag_en="", tag_pt=""):
        f, v = self.tagfv(doc, tag_en, tag_pt)
        return f
    def tagv(self, doc, tag_en="", tag_pt=""):
        f, v = self.tagfv(doc, tag_en, tag_pt)
        return v