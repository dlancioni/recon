import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")

from src.sqllib import SqlLib
lib = SqlLib()

recon = {
    "Id": 1,
    "Name": "Recon 1",
    "Description": "1:1 where both sides have the same file",
    "Datasources":
    [
        {
            "Side": 1,
            "Name": "One",
            "File": "etc:recon_11.txt",
            "Separator": ";",
            "Fields": 
            [
                {"name":"Agencia", "type":"integer", "value":"1010"},
                {"name":"Saldo", "type":"decimal", "function":"sum", "mask":",", "value":"1,99"},
                {"name":"Conta", "type":"text", "value":"10001-1"},
                {"name":"Data", "type":"datetime", "function":"max", "value":"20221231"}
            ]
        }
    ]
}

field_def = recon["Datasources"][0]["Fields"]

class CoreLibTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_get_field_type(self):
        self.assertEqual("", lib.get_field_type(""))
        self.assertEqual("real", lib.get_field_type("decimal"))
        self.assertEqual("text", lib.get_field_type("datetime"))
        
    def test_get_field_list(self):
        self.assertEqual("", lib.get_field_list(""))
        self.assertEqual("agencia, sum(saldo) saldo, conta, max(data) data", lib.get_field_list(field_def))
        
    def test_get_value_list(self):
        self.assertEqual("", lib.get_value_list(""))
        self.assertEqual("1010, 1.99, '10001-1', '20221231'", lib.get_value_list(field_def))
        
    def test_get_create_table_definition(self):
        self.assertEqual("", lib.get_create_table_definition("", ""))
        message = "create table tb "
        message += "("
        message += "id integer primary key, "
        message += "id_parent integer default 0, "
        message += "recon text default '', "
        message += "rule text default '', "
        message += "status text default 'orphan', "
        message += "agencia integer, "
        message += "saldo real, "
        message += "conta text, "
        message += "date text"
        message += ")"        
        self.assertEqual(len(message), len(lib.get_create_table_definition("tb", field_def)))
        
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
        
    def test_get_grouping_list(self):
        self.assertEqual("", lib.get_grouping_list(""))
        self.assertEqual("agencia, conta", lib.get_grouping_list(field_def))
        
    def test_get_sql_key(self):
        self.assertEqual("", lib.get_sql_key("", "", ""))
        fields = [ "name", "date" ]
        message = "and tb1.name = tb2.name and tb1.date = tb2.date"
        self.assertEqual(message, lib.get_sql_key("tb1", "tb2", fields))        

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
