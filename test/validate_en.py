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

class ValidateEn(unittest.TestCase):

    def open_recon(self):
        path = fslib.get_path_recon("", "recon [en_us].cfg")
        recon = fslib.open_json(path)
        return recon

    def validate_tag(self, field):
        recon = self.open_recon()
        del recon[field]
        status, message, reports = corelib.process(recon)
        self.assertEqual(status, False)

    def validate_value(self, field):
        recon = self.open_recon()
        del recon[field]
        status, message, reports = corelib.process(recon)
        self.assertEqual(status, False)

    def validate_header(self):
        for field in ["Id", "Name", "Description"]:
            self.validate_tag(field)
            self.validate_value(field)