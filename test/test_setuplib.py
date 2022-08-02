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

class SetupLibTest(unittest.TestCase):
    
    def open_recon(self, language):
        filename = "test (en-us).cfg" if language == "en-us" else "test (pt-br).cfg"
        path = fslib.get_path_config(filename)
        recon = setuplib.open_recon(path)
        return recon

    def assert_validate_tag(self, recon):
        status, message, reports = corelib.process(recon)
        self.assertEqual(status, False)
        self.assertNotEqual(message, "")
        
    def assert_validate_msg(self, recon, field=""):
        status, message, reports = corelib.process(recon)
        self.assertEqual(status, False)
        br = msglib.get("E4", [field], "en-us") + " " + msglib.get("V2", [field], "en-us")
        us = msglib.get("E4", [field], "pt-br") + " " + msglib.get("V2", [field], "pt-br")
        self.assertEqual(message in [us, br], True)

    def validate_header(self, language):
        if language == "en-us":
            fields = ["Id", "Name", "Description"]
        else:
            fields = ["Id", "Nome", "Descrição"]
        for field in fields:            
            recon = self.open_recon(language)
            del recon[field]
            self.assert_validate_tag(recon)            
            recon = self.open_recon(language)
            recon[field] = ""
            self.assert_validate_msg(recon, field)
            
    def validate_datasource(self, language):        
        if language == "en-us":
            fields_ds = ["Side", "Name", "File", "Separator", "Start", "Fields"]
            fields_fd = ["Id", "Name", "Type"]
            session_ds = "Datasources"
            session_fd = "Fields"
        else:
            fields_ds = ["Lado", "Nome", "Arquivo", "Separador", "Inicio", "Campos"]
            fields_fd = ["Id", "Nome", "Tipo"]
            session_ds = "Dados"
            session_fd = "Campos"
        for field in fields_ds:
            if field != session_fd:
                recon = self.open_recon(language)
                del recon[session_ds][0][field]
                self.assert_validate_tag(recon)
                recon = self.open_recon(language)
                recon[session_ds][0][field] = ""
                self.assert_validate_msg(recon, field)
            else:
                for field in fields_fd:
                    recon = self.open_recon(language)
                    del recon[session_ds][0][session_fd][0][field]
                    self.assert_validate_tag(recon)
                    recon = self.open_recon(language)
                    recon[session_ds][0][session_fd][0][field] = ""
                    self.assert_validate_msg(recon, field)
                    
    def validate_recon(self, language):
        if language == "en-us":
            fields_rc = ["Rule", "Fields"]
            fields_fd = ["Type", "Name"]
            session_rc = "Recon"
            session_fd = "Fields"
        else:
            fields_rc = ["Regra", "Campos"]
            fields_fd = ["Tipo", "Nome"]
            session_rc = "Conciliação"
            session_fd = "Campos"
        for field in fields_rc:
            if field != session_fd:
                recon = self.open_recon(language)
                del recon[session_rc][0][field]
                self.assert_validate_tag(recon)
                recon = self.open_recon(language)
                recon[session_rc][0][field] = ""
                self.assert_validate_msg(recon, field)
            else:
                for field in fields_fd:
                    recon = self.open_recon(language)
                    del recon[session_rc][0][session_fd][0][field]
                    self.assert_validate_tag(recon)
                    recon = self.open_recon(language)
                    recon[session_rc][0][session_fd][0][field] = ""
                    self.assert_validate_msg(recon, field)    
                    
    def open_bad_recon(self):
        message = ""
        try:
            filename = "test [bad json].cfg"
            path = fslib.get_path_config(filename)
            recon = setuplib.open_recon(path)
        except BaseException as err:
            message = str(err)
        self.assertNotEqual(message, "")
                  
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_recon(self):
        self.open_bad_recon()
        for language in ["en-us", "pt-br"]:
            self.validate_header(language)
            self.validate_datasource(language)
            self.validate_recon(language)

if __name__ == '__main__':
    unittest.main()