import os
import sys
import logging
import argparse
from src.fslib import FsLib
from src.fslib import FsLib
from src.msglib import MsgLib
from datetime import timedelta
from src.utillib import UtilLib
from src.corelib import CoreLib
from timeit import default_timer as timer
fslib = FsLib()
msglib = MsgLib()
utillib = UtilLib()
""" control the user input """
utillib.cls()
parser = argparse.ArgumentParser()
parser.add_argument("--f", help="File with conciliation configuration")
parser.add_argument("--c", help="Conciliation results per side: [1, 2, 12]")
args = parser.parse_args()
""" append file extension if not provided """
filename = "recon.cfg" if args.f == None else args.f
""" start processing """
start = timer()
msglib.print(msglib.get_value(msglib.console, "M1"))
corelib = CoreLib()
status, error, result, console = corelib.process(filename)
end = timer()
""" finish processing """
msglib.print(msglib.get_value(msglib.console, "M2"))
msg = msglib.get_value(msglib.console, "M3")
msglib.print(f"{msg}: {timedelta(seconds=end-start)}")
""" print console information """
if status == False:
    utillib.cls()
    msglib.print(f"{filename}")
    msglib.print(error)
else:
    if str(args.c).isnumeric():
        utillib.cls()        
        print(f"{filename}")
        if int(args.c) == 1:
            print(console[1])
        if int(args.c) == 2:
            print(console[2])
        if int(args.c) == 12:
            print(console[1])
            print(console[2])