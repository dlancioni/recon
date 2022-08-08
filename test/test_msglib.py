import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")
from src.msglib import MsgLib
from src.cfglib import ConfigLib
from src.utillib import UtilLib

msglib = MsgLib()
cfglib = ConfigLib()
utillib = UtilLib()

class UtilLibTest(unittest.TestCase):

    def setUp(self):
        pass
    
    def open_config(self):
        language = cfglib.get(7)
        if language.lower() in ["en-us", "pt-br"]:
            validated = True
        else:
            validated = False
        self.assertEqual(validated, True)

    def get_value(self):
        # No parameters
        x = "Start processing"
        y = msglib.get("M1", [], "en-us")
        self.assertEqual(x, y)
        x = "Iniciando o processamento"
        y = msglib.get("M1", [], "pt-br")
        self.assertEqual(x, y)
        # within parameters
        x = "Field Id is mandatory"
        y = msglib.get("V2", ["Id"], "en-us")
        self.assertEqual(x, y)
        x = "Campo Id é obrigatório"
        y = msglib.get("V2", ["Id"], "pt-br")
        self.assertEqual(x, y)

    def tearDown(self):
        pass
    
    """ Trigger all tests """
    def test_run(self):
        self.open_config()
        self.get_value()
        utillib.cls()    

if __name__ == '__main__':
    unittest.main()