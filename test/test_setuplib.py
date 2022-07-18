import os
import sys
import json
import logging
import copy
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")
from validation import Validation

class SetupLibTest(unittest.TestCase):
                  
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_mandatory(self):
        validation = Validation()
        for language in ["en-us", "pt-br"]:
            validation.validate_header(language)
            validation.validate_datasource(language)
            validation.validate_recon(language)

if __name__ == '__main__':
    unittest.main()