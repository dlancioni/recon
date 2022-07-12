import os
import sys
import json
import logging
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")

from src.fslib import FsLib
from src.utillib import UtilLib
from src.msglib import MsgLib
from src.cfglib import ConfigLib
from src.corelib import CoreLib

msglib = MsgLib()
corelib = CoreLib()

class UtilLibTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_validate_info(self):
        i = 0
        values = []
        values.append({"Id":"", "Name":"Saldo x Extrato", "Description":"1:M reconciliation"})
        values.append({"Id":"1", "Name":"", "Description":"1:M reconciliation"})
        values.append({"Id":"1", "Name":"Saldo x Extrato", "Description":""})
        session = ""
        fields = ["Id", "Name", "Description"]
        for field in fields:
            message = msglib.get_value(msglib.validation, "M2", [field])
            status, error = corelib.process(values[i])
            self.assertEqual(False, status)
            self.assertEqual(message, error)
            i += 1

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()