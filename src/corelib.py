import os
import json
os.system("cls")

class CoreLib:

    def __init__(self):
        pass

    def get_table_structure(self, f1, t1, f2, t2):
        if len(f1) != len(t1) or len(f2) != len(t2): return [],[]
        f = list(dict.fromkeys(f1 + f2))
        t = list(dict.fromkeys(t1 + t2))
        return f, t