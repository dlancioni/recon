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
    
    def assert_mandatory(self, fn, config, field):
        try:
            if fn == "validate_info":
                msg = msglib.get("V2", [field])
                validlib.validate_info(config)
        except BaseException as err:
            self.assertEqual(msg, str(err))

    def test_validate_info(self):
        self.assert_mandatory("validate_info", {"Id":"", "Nome": "abc", "Descrição": "abc"}, "Id")

if __name__ == '__main__':
    unittest.main()
