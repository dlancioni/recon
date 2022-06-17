import os
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

database_path = os.path.join('..', 'path', 'to', 'db')

print(os.path.join('.'))
print(os.path.join('..', 'path', 'to', 'db'))
print(os.path.join( 'to', 'db'))
print(os.path.join('db'))
os.path.abspath(".")


etl = EtlLib()
etl.import_file()



