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
utillib = UtilLib()

class SetupLibTest(unittest.TestCase):
       
    def open_recon(self):
        filename = "test_basic.cfg"
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
        us = msglib.get("E4", [field], "en-us") + " " + msglib.get("V2", [field], "en-us")
        br = msglib.get("E4", [field], "pt-br") + " " + msglib.get("V2", [field], "pt-br")
        self.assertEqual(message in [us, br], True)

    def validate_header(self):
        fields = ["Id", "Name", "Description"]
        for field in fields:            
            recon = self.open_recon()
            tagname = setuplib.tag_name(recon, field)
            del recon[tagname]
            self.assert_validate_tag(recon)
            recon = self.open_recon()
            tagname = setuplib.tag_name(recon, field)
            recon[tagname] = ""
            self.assert_validate_msg(recon, tagname)

    def validate_datasource(self):        
        fields_ds = ["Side", "Name", "Type", "Delimiter", "File", "Start", "Fields"]
        fields_fd = ["Position", "Name", "Type"]
        for field in fields_ds:
            if field != "Fields":
                recon = self.open_recon()
                tag_ds = setuplib.tag_name(recon, "Datasources")
                tag_field = setuplib.tag_name(recon[tag_ds][0], field)
                del recon[tag_ds][0][tag_field]
                self.assert_validate_tag(recon)
                recon = self.open_recon()
                tag_ds = setuplib.tag_name(recon, "Datasources")
                tag_field = setuplib.tag_name(recon[tag_ds][0], field)
                recon[tag_ds][0][tag_field] = ""
                self.assert_validate_msg(recon, tag_field)
            else:
                for field in fields_fd:
                    recon = self.open_recon()                    
                    tag_ds = setuplib.tag_name(recon, "Datasources")
                    tag_fd = setuplib.tag_name(recon[tag_ds][0], "Fields")
                    tag_field = setuplib.tag_name(recon[tag_ds][0][tag_fd][0], field)                    
                    del recon[tag_ds][0][tag_fd][0][tag_field]
                    self.assert_validate_tag(recon)                    
                    recon = self.open_recon()                    
                    tag_ds = setuplib.tag_name(recon, "Datasources")
                    tag_fd = setuplib.tag_name(recon[tag_ds][0], "Fields")
                    tag_field = setuplib.tag_name(recon[tag_ds][0][tag_fd][0], field)                    
                    recon[tag_ds][0][tag_fd][0][tag_field] = ""
                    self.assert_validate_msg(recon, tag_field)
                    
    def validate_recon(self):        
        fields_rc = ["Rule", "Fields"]
        fields_fd = ["Type", "Name"]
        for field in fields_rc:
            if field != "Fields":               
                recon = self.open_recon()
                tag_rc = setuplib.tag_name(recon, "Recon")
                tag_field = setuplib.tag_name(recon[tag_rc][0], field)
                del recon[tag_rc][0][tag_field]
                self.assert_validate_tag(recon)
                recon = self.open_recon()
                tag_rc = setuplib.tag_name(recon, "Recon")
                tag_field = setuplib.tag_name(recon[tag_rc][0], field)
                recon[tag_rc][0][tag_field] = ""
                self.assert_validate_msg(recon, tag_field)
            else:
                for field in fields_fd:
                    recon = self.open_recon()
                    tag_rc = setuplib.tag_name(recon, "Recon")
                    tag_fd = setuplib.tag_name(recon[tag_rc][0], "Fields")
                    tag_field = setuplib.tag_name(recon[tag_rc][0][tag_fd][0], field)
                    del recon[tag_rc][0][tag_fd][0][tag_field]
                    self.assert_validate_tag(recon)                    
                    recon = self.open_recon()
                    tag_rc = setuplib.tag_name(recon, "Recon")
                    tag_fd = setuplib.tag_name(recon[tag_rc][0], "Fields")
                    tag_field = setuplib.tag_name(recon[tag_rc][0][tag_fd][0], field)
                    recon[tag_rc][0][tag_fd][0][tag_field] = ""
                    self.assert_validate_msg(recon, tag_field)
                    
    def open_bad_recon(self):
        message = ""
        try:
            filename = "test_bad_json"
            path = fslib.get_path_config(filename)
            recon = setuplib.open_recon(path)
        except BaseException as err:
            message = str(err)
        self.assertNotEqual(message, "")
                  
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    """ Malformed configuration file """
    def bad_configuration(self):       
        self.open_bad_recon()

    """ Tag names and mandatory fields """
    def validation(self):       
        self.validate_header()
        self.validate_datasource()
        self.validate_recon()

    """ Trigger all tests """
    def test_run(self):
        self.bad_configuration()
        self.validation()
        utillib.cls()

if __name__ == '__main__':
    unittest.main()