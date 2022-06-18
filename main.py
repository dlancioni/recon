import os
import sys
import logging
from src.corelib import CoreLib

Log_Format = " %(asctime)s - %(levelname)s %(message)s"
logging.basicConfig(filename = "c:\\temp\\log.txt",
                    filemode = "w",
                    format = Log_Format,
                    level=logging.DEBUG)

logger = logging.getLogger()
logger.info("Hello from main")

print("Start processing the recons")
corelib = CoreLib()
corelib.process()
print("End processing the recons")


