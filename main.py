import os
import sys
import logging
from src.corelib import CoreLib
from src.fslib import FsLib

fslib = FsLib()
setup = fslib.get_json(os.path.dirname(os.path.realpath(__file__)) + "\\setup.json")
log_path = setup["log"] + "\\log.txt"
log_format = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename = log_path,
                    filemode = "w",
                    datefmt='%Y-%m-%d %H:%M:%S',
                    format = log_format,
                    level=logging.DEBUG)

logger = logging.getLogger()
logger.info("Start processing the recons")
corelib = CoreLib()
corelib.process()
logger.info("Finish processing the recons")