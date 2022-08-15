import os
import sys
import json
import logging
import copy
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")
from src.fslib import FsLib
from src.utillib import UtilLib
from src.msglib import MsgLib
from src.cfglib import ConfigLib
from src.corelib import CoreLib
from src.setuplib import SetupLib

msglib = MsgLib()
corelib = CoreLib()
fslib = FsLib()
setuplib = SetupLib()
utillib = UtilLib()

class SetupLibTest(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()