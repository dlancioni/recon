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

class Validation(unittest.TestCase):

    def open_recon(self, language):
        filename = "recon [en_us].cfg" if language == "en-us" else "recon [pt_br].cfg"
        path = fslib.get_path_recon("", filename)
        recon = fslib.open_json(path)
        return recon

    def assert_field(self, recon):
        status, message, reports = corelib.process(recon)
        self.assertEqual(status, False)

    def validate_header(self, language):
        if language == "en-us":
            fields = ["Id", "Name", "Description"]
        else:
            fields = ["Id", "Nome", "Descrição"]
        for field in fields:
            recon = self.open_recon(language)
            del recon[field]
            self.assert_field(recon)            
            recon = self.open_recon(language)
            recon[field] = ""
            self.assert_field(recon)
            
    def validate_datasource(self, language):        
        if language == "en-us":
            fields_ds = ["Side", "Name", "File", "Separator", "Fields"]
            fields_fd = ["Id", "Name", "Type"]
            session_ds = "Datasources"
            session_fd = "Fields"
        else:
            fields_ds = ["Lado", "Nome", "Arquivo", "Separador", "Campos"]
            fields_fd = ["Id", "Nome", "Tipo"]
            session_ds = "Dados"
            session_fd = "Campos"
        for field in fields_ds:
            recon = self.open_recon(language)
            del recon[session_ds][0][field]
            self.assert_field(recon)
            recon = self.open_recon(language)
            recon[session_ds][0][field] = ""
            self.assert_field(recon)
            if field == session_fd:
                for field in fields_fd:
                    recon = self.open_recon(language)
                    del recon[session_ds][0][session_fd][0][field]
                    self.assert_field(recon)
                    recon = self.open_recon(language)
                    recon[session_ds][0][session_fd][0][field] = ""
                    self.assert_field(recon)