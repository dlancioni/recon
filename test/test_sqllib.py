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
    def get_field_list(self):
        # no data
        self.assertEqual("", lib.get_field_list(""))
        # all
        fields = ["integer", "decimal", "text", "datetime"]
        self.assertEqual("integer, decimal, text, datetime", lib.get_field_list(fields))
        # aggregate
        fields = ["integer", "decimal", "text", "datetime"]
        types  = ["integer", "decimal", "text", "datetime"]
        aggregs  = ["", "sum", "", "max"]
        self.assertEqual("integer, sum(decimal) decimal, text, max(datetime) datetime", lib.get_field_list(fields, types, aggregs))        
        
    # value list to generate insert
    def test_get_value_list(self):       
        # no data
        self.assertEqual("", lib.get_value_list([], [], [], []))        
        # regular
        fields = [ "integer", "decimal", "text", "datetime" ]
        types  = [ "integer", "decimal", "text", "datetime" ]
        masks  = [ "", "", "", "" ]        
        values = [ 1, "1.99", "text 1", "20221231" ]
        message = "1, 1.99, 'text 1', '20221231'"
        self.assertEqual(message, lib.get_value_list(fields, types, values, masks))        
        # mask decimal (,)
        fields = [ "integer", "decimal", "text", "datetime" ]
        types  = [ "integer", "decimal", "text", "datetime" ]
        values = [ 1, "1,99", "text 1", "20221231" ]
        masks  = [ "", ",", "", "" ]
        message = "1, 1.99, 'text 1', '20221231'"
        self.assertEqual(message, lib.get_value_list(fields, types, values, masks))

    # generate script to create table
    def test_get_create_table_definition(self):
        # empty
        self.assertEqual("", lib.get_create_table_definition("", "", ""))
        # complete
        fields = [ "integer", "decimal", "text", "datetime" ]
        types  = [ "integer", "decimal", "text", "datetime" ]
        message = "create table tb (integer integer, decimal real, text text, datetime text)"
        self.assertEqual(message, lib.get_create_table_definition("tb", fields, types))

    # generate script to create index
    def test_get_create_index_definition(self):
        # empty
        self.assertEqual("", lib.get_create_index_definition("", ""))
        # complete
        fields = [ "integer", "decimal", "text", "datetime" ]
        message = "create index idx_tb on tb (integer, decimal, text, datetime)"
        self.assertEqual(message, lib.get_create_index_definition("tb", fields))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()