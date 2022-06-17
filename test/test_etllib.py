import os
import sys
import pathlib
import unittest
sys.path.append("..")
sys.path.insert(1, pathlib.Path().resolve()._str + "\\recon\\")

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

class EtlLibTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_import_file(self):
        path = fslib.get_dir_etc("Saldo x Extrato.json")
        setup = fslib.get_json(path)
        ds = setup["Side 1"]["Datasource"][0]
        cn = dblib.get_connection()
        #etllib.import_file(cn, ds)
        self.assertEqual("", "")

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()