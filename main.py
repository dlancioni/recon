import os
import sys
import csv
import logging
import argparse
from src.fslib import FsLib
from src.fslib import FsLib
from src.msglib import MsgLib
from datetime import timedelta
from src.utillib import UtilLib
from src.corelib import CoreLib
from src.reportlib import ReportLib
from timeit import default_timer as timer
fslib = FsLib()
msglib = MsgLib()
utillib = UtilLib()
reportlib = ReportLib()
""" control the user input """
utillib.cls()
parser = argparse.ArgumentParser()
parser.add_argument("--f", help="File with conciliation configuration")
parser.add_argument("--t", nargs='?', const=1, type=int, help="Time elapsed")
parser.add_argument("--r", nargs='?', const=0, type=int, help="Results on console: [0] Sinthetic, [1] Side 1 [2] Side 2 [12] Side 1 and 2")
args = parser.parse_args()
""" append file extension if not provided """
filename = "recon [en_us].cfg" if args.f == None else args.f
""" start processing """
start = timer()
msglib.print(msglib.get_value(msglib.console, "M1"))
corelib = CoreLib()
status, error, reports = corelib.process(filename)
end = timer()
""" finish processing """
msglib.print(msglib.get_value(msglib.console, "M2"))
""" print console information """
if status == False:
    msglib.print(f"{filename}")
    msg = msglib.set_time(error)
    CRED = '\033[91m'
    CEND = '\033[0m'    
    print(CRED + msg + CEND)
else:
    if args.r != None:
        index = int(args.r)
        reportlib.print_report(reports, index)
""" time elapsed """
if args.t != None:
    msg = msglib.get_value(msglib.console, "M3")
    msglib.print(f"{msg}: {timedelta(seconds=end-start)}")