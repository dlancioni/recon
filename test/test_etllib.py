import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")
from src.etllib import EtlLib
from src.validlib import ValidationLib
from src.msglib import MsgLib

msglib = MsgLib()
validlib = ValidationLib()
etllib = EtlLib(1, "test")

class EtlLibTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_validate_info(self):
        config = {
            "Id": "",
            "Nome": "",
            "Descrição": ""
        }
        #self.assertRaises(ValueError(msglib.get("V2", ["Id"])), validlib.validate_info(config))
        msg = msglib.get("V2", ["Id"])
        with self.assertRaises(Exception):
            validlib.validate_info(config)

if __name__ == '__main__':
    unittest.main()