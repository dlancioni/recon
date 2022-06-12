import sys
sys.path.append("..")

import unittest
from src.sqllib import SqlLib
lib = SqlLib()

class CoreLibTest(unittest.TestCase):

    def setUp(self):
        pass

    # field type used to create table
    def test_get_field_type(self):
        self.assertEqual("", lib.get_field_type(""))
        self.assertEqual("real", lib.get_field_type("decimal"))
        self.assertEqual("text", lib.get_field_type("datetime"))

    # field list to generate select, group by, order by
    def test_get_field_type(self):
        self.assertEqual("", lib.get_field_list(""))
        self.assertEqual("text, decimal", lib.get_field_list(["text","decimal"]))
        self.assertEqual("text, sum(decimal) decimal", lib.get_field_list(["text","decimal"], ["text", "decimal"], ["", "sum"]))
        
    # value list to generate insert
    def test_get_value_list(self):
        
        message = ""
        fields = []
        types =  []
        values = []
        self.assertEqual(message, lib.get_value_list(fields, types, values))
        
        message = "1, 1.99, 'text 1', '20221231'"
        fields = ["integer", "decimal", "text", "datetime"]
        types =  ["integer", "decimal", "text", "datetime"]
        values = [1, 1.99, "text 1", "20221231"]
        self.assertEqual(message, lib.get_value_list(fields, types, values))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()