import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")
from src.msglib import MsgLib

msglib = MsgLib()

class UtilLibTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_value(self):
        # No parameters
        x = "Start processing"
        y = msglib.get_value("console", "M1", [], "en-us")
        self.assertEqual(x, y)
        x = "Iniciando processamento"
        y = msglib.get_value("console", "M1", [], "pt-br")
        self.assertEqual(x, y)
        # within parameters
        x = "Mandatory field: {1}".replace("{1}", "Id")
        y = msglib.get_value("validation", "M2", ["Id"], "en-us")
        self.assertEqual(x, y)
        x = "Campo obrigatório: {1}".replace("{1}", "Id")
        y = msglib.get_value("validation", "M2", ["Id"], "pt-br")
        self.assertEqual(x, y)        
        
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()