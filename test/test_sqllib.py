import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")

from src.sqllib import SqlLib
lib = SqlLib()

class CoreLibTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_get_field_type(self):
        self.assertEqual("", lib.get_field_type(""))
        self.assertEqual("real", lib.get_field_type("decimal"))
        self.assertEqual("text", lib.get_field_type("datetime"))
        
    def get_field_list(self):
        self.assertEqual("", lib.get_field_list(""))
        fields = ["integer", "decimal", "text", "datetime"]
        self.assertEqual("integer, decimal, text, datetime", lib.get_field_list(fields))
        fields = ["integer", "decimal", "text", "datetime"]
        types  = ["integer", "decimal", "text", "datetime"]
        aggregs  = ["", "sum", "", "max"]
        self.assertEqual("integer, sum(decimal) decimal, text, max(datetime) datetime", lib.get_field_list(fields, types, aggregs))
        
    def get_grouping_list(self):
        self.assertEqual("", lib.get_grouping_list("", ""))
        fields = ["integer", "decimal", "text", "datetime"]
        funcs  = ["", "sum", "", "max"]
        self.assertEqual("integer, text, datetime", lib.get_grouping_list(fields, funcs))
        
    def test_get_value_list(self):       
        self.assertEqual("", lib.get_value_list([], [], [], []))        
        fields = [ "age", "salary", "name", "birthdate" ]
        types  = [ "integer", "decimal", "text", "datetime" ]
        masks  = [ "", "", "", "" ]
        values = [ 1, "1.99", "text 1", "20221231" ]
        message = "1, 1.99, 'text 1', '20221231'"
        self.assertEqual(message, lib.get_value_list(fields, types, values, masks))
        fields = [ "age", "salary", "name", "birthdate" ]
        types  = [ "integer", "decimal", "text", "datetime" ]
        values = [ 1, "1,99", "text 1", "20221231" ]
        masks  = [ "", ",", "", "" ]
        message = "1, 1.99, 'text 1', '20221231'"
        self.assertEqual(message, lib.get_value_list(fields, types, values, masks))
        
    def test_get_create_table_definition(self):
        self.assertEqual("", lib.get_create_table_definition("", "", ""))
        fields = [ "age", "salary", "name", "birthdate" ]
        types  = [ "integer", "decimal", "text", "datetime" ]
        message = "create table tb (id integer primary key, id_parent integer default 0, recon text default '', rule text default '', age integer, salary real, name text, birthdate text)"
        self.assertEqual(message, lib.get_create_table_definition("tb", fields, types))
        
    def test_get_create_index_definition(self):
        self.assertEqual("", lib.get_create_index_definition("", ""))
        fields = [ "name", "date" ]
        message = "create index idx_tb on tb (name, date)"
        self.assertEqual(message, lib.get_create_index_definition("tb", fields))
        
    def test_get_sql_insert(self):
        self.assertEqual("", lib.get_sql_insert("", "", ""))
        tablename = "tb"
        fields = "id, name"
        values = "1, 'nome 1'"
        message = "insert into tb (id, name) values (1, 'nome 1')"
        self.assertEqual(message, lib.get_sql_insert(tablename, fields, values))
        
    def test_get_table_structure(self):
        f,t = lib.get_table_structure(["name", "age"], ["text", "integer"], ["name", "age", "salary", "bonus"], ["text", "integer", "decimal", "decimal"])
        self.assertEqual(4, len(f))
        self.assertEqual(4, len(t))        
        f,t = lib.get_table_structure(["name"], ["text", "integer"], ["name", "age", "salary"], ["text", "integer", "decimal"])
        self.assertEqual([], f)
        self.assertEqual([], t)
        f,t = lib.get_table_structure(["name", "age"], ["text", "integer"], ["name", "age", "salary"], [])
        self.assertEqual([], f)
        self.assertEqual([], t)
        f,t = lib.get_table_structure([], [], ["name", "age", "salary"], ["text", "integer", "decimal"])
        self.assertEqual(3, len(f))
        self.assertEqual(3, len(t))
        f,t = lib.get_table_structure(["name", "age"], ["text", "integer"], ["name", "age", "salary"], ["text", "integer", "decimal"])
        self.assertEqual(3, len(f))
        self.assertEqual(3, len(t))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()