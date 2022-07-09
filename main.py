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
""" General declaration """
recons = []
utillib = UtilLib()
fslib = FsLib()
msglib = MsgLib()
""" Control the user input """
parser = argparse.ArgumentParser()
parser.add_argument("--g", help="json file that groups the recons")
parser.add_argument("--r", help="json file with single recon")
args = parser.parse_args()
if args.g:
    print("Importing a group of recons...", args.g)
if args.r:
    recons.append(args.r)
""" Start processing """
if len(recons) == 0:
    recons = ["recon.json"]
os.system("cls||clear")
start = timer()
msglib.print("message", 1)
corelib = CoreLib()
for recon in recons:
    corelib.process(recon)
end = timer()
msglib.print("message", 2)
msg = msglib.get_value("message", 3)
print(f"{msg}: {timedelta(seconds=end-start)}")