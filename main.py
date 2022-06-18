import os
import sys
import logging
from src.corelib import CoreLib
from src.fslib import FsLib

fslib = FsLib()

setup = fslib.get_json(os.path.dirname(os.path.realpath(__file__)) + "\\setup.json")

Log_Format = " %(asctime)s - %(levelname)s %(message)s"
logging.basicConfig(filename = setup["log"],
                    filemode = "w",
                    format = Log_Format,
                    level=logging.DEBUG)

logger = logging.getLogger()
logger.info("Hello from main")

print("Start processing the recons")
corelib = CoreLib()
corelib.process()
print("End processing the recons")


