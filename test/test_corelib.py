import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")
from src.corelib import CoreLib
from src.fslib import FsLib
from src.utillib import UtilLib
corelib = CoreLib()
fslib = FsLib()
utillib = UtilLib()

class CoreLibTest(unittest.TestCase):

    def validate_cfg(self):
        status, error, reports = corelib.process("recon [en_us]")
        self.assertEqual(status, True)
        status, error, reports = corelib.process("recon [pt_br]")
        self.assertEqual(status, True)
        
    def setUp(self):
        pass        
    
    def tearDown(self):
        pass
    
    def test_validation(self):
        utillib.cls()        
        self.validate_cfg()    

if __name__ == '__main__':
    unittest.main()