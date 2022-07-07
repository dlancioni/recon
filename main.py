# python -m unittest discover -stest -v

import os
import sys
import logging
from src.corelib import CoreLib
from src.fslib import FsLib
from src.utillib import UtilLib
from timeit import default_timer as timer
from datetime import timedelta

start = timer()
utillib = UtilLib()
# general configuration file
fslib = FsLib()
app_path = fslib.get_dir_parent(fslib.get_dir())
setup = fslib.get_json(app_path + "\\setup.json")
# log file
log_path = setup["log"] 
if log_path.find("etc:") > -1:
    log_path = fslib.get_dir_etc()
log_path += "\\log.txt"
log_format = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename = log_path,
                    filemode = "w",
                    datefmt='%Y-%m-%d %H:%M:%S',
                    format = log_format,
                    level=logging.DEBUG)
# core program
logger = logging.getLogger()
logger.info("Start processing the recons")
recons = []
recons = [
    #"Volume 1M.json"
    #"Volume 100k.json"
    "saldo x extrato.json"    
]
os.system("cls||clear")
utillib.log(f"Start processing...")
corelib = CoreLib()
for recon in recons:
    utillib.log(f"Running recon {recon}")
    corelib.process(recon)
utillib.log(f"Finish processing the recons")
end = timer()
print(f"Elapsed time: {timedelta(seconds=end-start)}")