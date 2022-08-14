import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")
from src.utillib import UtilLib

class UtilLibTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_abc(self):
        with self.assertRaises(Exception):
            100 / 1

if __name__ == '__main__':
    unittest.main()