import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")
from src.utillib import UtilLib
from src.fslib import FsLib


fslib = FsLib()
utillib = UtilLib()


class FsLibTest(unittest.TestCase):

    def setUp(self):
        pass

    def is_dir(self):
        v = fslib.is_dir("c:\\temp\\rpt")
        #self.assertEqual(v, True)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()