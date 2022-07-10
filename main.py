import os
import sys
import logging
import argparse
from src.fslib import FsLib
from src.fslib import FsLib
from datetime import timedelta
from src.utillib import UtilLib
from src.corelib import CoreLib
from src.msglib import MsgLib
from timeit import default_timer as timer
utillib = UtilLib()
fslib = FsLib()
msglib = MsgLib()

""" control the user input """
parser = argparse.ArgumentParser()
parser.add_argument("--g", help="json file that groups the recons")
parser.add_argument("--r", help="json file with single recon")
args = parser.parse_args()
recons = []
if args.g:
    print("Importing a group of recons...", args.g)
if args.r:
    arr = str(args.r).split(".")
    arr = arr[0]
    filename = arr +".json"
    recons.append(filename)
""" start processing """
if len(recons) == 0:
    recons = ["recon.json"]
os.system("cls||clear")
start = timer()
msglib.print(msglib.get_value(msglib.console, "M1"))
corelib = CoreLib()
for recon in recons:
    status, error = corelib.process(recon)
    if not status:
        msglib.print(error)
end = timer()
""" finish processing """
msglib.print(msglib.get_value(msglib.console, "M2"))
msg = msglib.get_value(msglib.console, "M3")
msglib.print(f"{msg}: {timedelta(seconds=end-start)}")