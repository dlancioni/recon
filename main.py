import sys
import logging
from src.etllib import EtlLib

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "c:\\temp\\log.txt",
                    filemode = "w",
                    format = Log_Format,
                    level=logging.DEBUG)

logger = logging.getLogger()
logger.info("Hello from main")





etl = EtlLib()
etl.import_file()



