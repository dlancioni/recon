import sys
import os
from src.sqllib import SqlLib
from src.corelib import CoreLib
lib = CoreLib()
os.system("cls")

f1  = ["name", "age"]
t1   = ["text", "integer"]
f2  = ["name", "age", "salary"]
t2   = ["text", "integer", "decimal"]


f1  = ["name", "age"]
t1   = ["text", "integer"]
f2  = []
t2   = []
f,t = lib.get_table_structure(f1, t1, f2, t2)

print(f)
print(t)

