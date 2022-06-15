import sys
sys.path.append("..")

import unittest
from src.etllib import EtlLib
from src.utillib import UtilLib
from src.dblib import Db

import os
import json

class EtlLibTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_import_file(self, cn, ds):
        db = Db()
        cn = db.get_connection()
        util = UtilLib()
        path = os.path.abspath(util.get_dir_parent(".") + "\\tmp\\setup.json")
        
        self.assertEqual(1, 1)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()