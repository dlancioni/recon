import sys
import os
from src.sqllib import SqlLib
from src.corelib import CoreLib
lib = CoreLib()
lib = SqlLib()
os.system("cls")

fields = [ "f1", "f2", "f3", "f4" ]
types  = [ "integer", "decimal", "text", "datetime" ]
message = "create table tb (id integer, id_parent integer, recon text, rule text, f1 integer, f2 real, f3 text, f4 text)"
x = lib.get_create_table_definition("tb", fields, types)
print(x == message)
