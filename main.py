import os
import sys
import csv
import logging
import argparse
from datetime import timedelta
from timeit import default_timer as timer
from termcolor import colored, cprint
from src.fslib import FsLib
from src.msglib import MsgLib
from src.utillib import UtilLib
from src.corelib import CoreLib
from src.reportlib import ReportLib

""" general declaration """
fslib = FsLib()
msglib = MsgLib()
utillib = UtilLib()
corelib = CoreLib()
reportlib = ReportLib()

""" control the user input """
utillib.cls()
parser = argparse.ArgumentParser()
parser.add_argument("--f", help="File with conciliation configuration")
parser.add_argument("--c", nargs='?', const=1, type=int, help="Clear screen before show results")
parser.add_argument("--t", nargs='?', const=1, type=int, help="Time elapsed")
parser.add_argument("--r", nargs='?', const=0, type=int, help="Results on console: [0] Sinthetic, [1] Side 1 [2] Side 2 [12] Side 1 and 2")
args = parser.parse_args()

""" set default configuration if not provided """
filename = "recon [en-us].cfg" if args.f == None else args.f

""" start processing """
start = timer()
msglib.print(msglib.get("M1"))
status, error, reports = corelib.process(filename)
end = timer()

""" time elapsed """
if args.t != None:
    msg = msglib.get("M3")
    msg = msglib.set_time(f"{msg}: {timedelta(seconds=end-start)}")
    msg = colored(msg, "yellow")
    print(msg)

""" finish processing """
if status == True:
    print(colored(msglib.set_time(msglib.get("M10", [filename])), "green"))
else:
    print(colored(msglib.set_time(msglib.get("M11", [filename])), "red"))
    print(colored(msglib.set_time(error), "red"))
    
""" all done """
msglib.print(msglib.get("M2"))

""" generate reports """    
if status == True:
    if args.r != None:
        if args.c != None:
            utillib.cls()
        index = int(args.r)
        reportlib.print_report(reports, index)