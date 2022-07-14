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
parser.add_argument("--r", help="json file with single recon")
parser.add_argument("--c", help="output info on console [tb, tb1, tb2]")
args = parser.parse_args()

""" append file extension if not provided """
filename = "recon.cfg" if str(args.r).strip() == "" else args.r

""" start processing """
start = timer()
msglib.print(msglib.get_value(msglib.console, "M1"))
corelib = CoreLib()
status, error, tb1, tb2 = corelib.process(filename)
end = timer()

""" finish processing """
msglib.print(msglib.get_value(msglib.console, "M2"))
msg = msglib.get_value(msglib.console, "M3")
msglib.print(f"{msg}: {timedelta(seconds=end-start)}")

""" print console information """
if status == False:
    utillib.cls()    
    msg = f"Error processing {filename}"
    msglib.print(msg)
    msglib.print(error)
else:    
    if args.c in ["tb", "tb1"]:
        print(tb1)
    if args.c in ["tb", "tb2"]:    
        print(tb2)