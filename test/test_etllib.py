import os
import sys
import pathlib
import unittest
sys.path.append("..")
sys.path.insert(1, pathlib.Path().resolve()._str + "\\recon\\")

from src.etllib import EtlLib
from src.utillib import UtilLib
from src.dblib import Db

class EtlLibTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_import_file(self):       
        self.assertEqual(1, 1)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()