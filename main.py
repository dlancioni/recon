import os
import sys
import logging
import argparse
from src.fslib import FsLib
from src.fslib import FsLib
from datetime import timedelta
from src.utillib import UtilLib
from src.corelib import CoreLib
from timeit import default_timer as timer
""" General declaration """
recons = []
utillib = UtilLib()
fslib = FsLib()
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
    recons = [
        #"Volume 10k.json"
        "saldo x extrato.json"
    ]
os.system("cls||clear")
start = timer()
utillib.log(f"Start processing...")
corelib = CoreLib()
for recon in recons:
    corelib.process(recon)
utillib.log(f"Finish processing the recons")
end = timer()
print(f"Elapsed time: {timedelta(seconds=end-start)}")