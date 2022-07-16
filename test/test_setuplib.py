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

msglib = MsgLib()
corelib = CoreLib()
fslib = FsLib()

class UtilLibTest(unittest.TestCase):
    
    def open_recon(self):
        path = fslib.get_path_recon("", "recon [en_us].cfg")
        recon_en = fslib.open_json(path)
        path = fslib.get_path_recon("", "recon [pt_br].cfg")
        recon_pt = fslib.open_json(path)            
        return recon_en, recon_pt

    def setUp(self):
        pass

    def test_validate_info(self):
        recon_en, recon_pt = self.open_recon()
        fields = ["Id", "Name", "Description"]
        for field in fields:
            us = f"Mandatory field: {field}"
            pt = f"Campo obrigatório: {field}"            
            recon = copy.copy(recon_en)
            recon[field] = ""
            status, message, reports = corelib.process(recon)
            if message in [us, pt]: message = True
            self.assertEqual(status, False)
            self.assertEqual(message, True)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()