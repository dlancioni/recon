# python -m unittest discover -stest -v

import os
import sys
import logging
from src.corelib import CoreLib
from src.fslib import FsLib
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
corelib = CoreLib()
corelib.process()
logger.info("Finish processing the recons")