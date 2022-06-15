import os
import sys
import json
import pathlib
from src.dblib import Db
from src.fslib import FsLib
from src.etllib import EtlLib
from src.sqllib import SqlLib
from src.utillib import UtilLib
from src.corelib import CoreLib

dblib = Db()
fslib = FsLib()
sqllib = SqlLib()
etllib = EtlLib()
corelib = CoreLib()
utillib = UtilLib()

path = fslib.get_dir_etc("Saldo x Extrato.json")
setup = fslib.get_json(path)
ds = setup["Side 1"]["Datasource"][0]
cn = dblib.get_connection()

os.system("cls")
etllib.import_file(cn, ds)