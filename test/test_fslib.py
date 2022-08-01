import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")

from src.fslib import FsLib

fslib = FsLib()

class FsLibTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_is_dir(self):
        v = fslib.is_dir("c:\\temp\\rpt")
        #self.assertEqual(v, True)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()