import os
import sys
import json
import logging
import copy
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")
from validate_en import ValidateEn
from validate_pt import ValidatePt

class UtilLibTest(unittest.TestCase):
                  
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
                    
    def test_validate_en(self):
        en = ValidateEn()
        en.validate_header()
        
    def test_validate_pt(self):
        pt = ValidatePt()
        pt.validate_header()

if __name__ == '__main__':
    unittest.main()