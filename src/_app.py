import sys
import os
from sqllib import SqlLib
lib = SqlLib()
os.system("cls")

fields = [ "integer", "decimal", "text", "datetime" ]
types =  [ "integer", "decimal", "text", "datetime" ]
values = [ 1, 1.99, "text 1", "20221231" ]
x = lib.get_value_list(fields, types, values)
print(x)