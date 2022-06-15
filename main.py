import sys
import logging
from src.etllib import EtlLib

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "c:\\temp\\log.txt",
                    filemode = "w",
                    format = Log_Format)

logger = logging.getLogger()
logger.error("Hello from main")


etl = EtlLib()
etl.import_file()



