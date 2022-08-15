import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")
from src.etllib import EtlLib
from src.validlib import ValidationLib
from src.msglib import MsgLib

msglib = MsgLib()
validlib = ValidationLib()

class EtlLibTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
