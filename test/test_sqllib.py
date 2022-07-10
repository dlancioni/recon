import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")

from src.sqllib import SqlLib
lib = SqlLib()

recon = {
    "Id": 1,
    "Name": "Saldo x Extrato",
    "Description": "1:M reconciliation",
    "Datasources":
    [
        {
            "Side": 1,
            "Name": "Saldo",
            "Path": "",
            "File": "saldo.txt",
            "Separator": ";",
            "Fields":
            [
                {"Id":1, "Name":"Data do Movimento", "Type":"Datetime", "Value":"20221231", "Mask":""},
                {"Id":2, "Name":"Codigo da Agencia", "Type":"Integer", "Value":"1010", "Mask":""},
                {"Id":3, "Name":"Numero da Conta", "Type":"Text", "Value":"10001-1", "Mask":""},
                {"Id":4, "Name":"Saldo na Data", "Type":"Decimal", "Value":"1.99", "Mask":""}
            ]
        }
        ,
        {
            "Side": 2,
            "Name": "Extrato",
            "Path": "",            
            "File": "extrato.txt",
            "Separator": ";",
            "Fields": 
            [
                {"Id":1, "Name":"Data do Movimento", "Type":"Datetime", "Value":"20221231", "Mask":""},
                {"Id":2, "Name":"Codigo da Agencia", "Type":"Integer", "Value":"1010", "Mask":""},
                {"Id":3, "Name":"Numero da Conta", "Type":"Text", "Value":"10001-1", "Mask":""},
                {"Id":4, "Name":"Saldo na Data", "Type":"Decimal", "Value":"1.99", "Mask":""}
            ]
        }
    ],
    "Recons":
    [
        {
            "Rule": "Agencia/Conta",
            "Fields":
            [
                {"Type":"Key", "Name":"Codigo da Agencia"},
                {"Type":"Key", "Name":"Numero da Conta"},
                {"Type":"Compare", "Name":"Saldo na Data", "Function":"Sum"},
                {"Type":"Compare", "Name":"Data do Movimento"}
            ]
        }
    ]
}

field_def = recon["Datasources"][0]["Fields"]
recon_def = recon["Recons"][0]["Fields"]

class CoreLibTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_get_field_type(self):
        self.assertEqual("", lib.get_field_type(""))
        self.assertEqual("Real", lib.get_field_type("decimal"))
        self.assertEqual("Text", lib.get_field_type("datetime"))
        self.assertEqual("Integer", lib.get_field_type("integer"))
        self.assertEqual("Text", lib.get_field_type("datetime"))
        
    def test_get_field_list(self):
        self.assertEqual("", lib.get_field_list(""))
        self.assertEqual("[Data do Movimento], [Codigo da Agencia], [Numero da Conta], [Saldo na Data]", lib.get_field_list(field_def))
        
    def test_get_value_list(self):
        self.assertEqual("", lib.get_value_list(""))
        self.assertEqual("'20221231', 1010, '10001-1', 1.99", lib.get_value_list(field_def))
        
    def test_get_create_table_definition(self):
        self.assertEqual("", lib.get_create_table_definition("", "", ""))
        message = "create table tb (Id integer primary key, Id_Parent integer default 0, Recon text default '', Rule text default '', Status text default 'Orphan', [Data do Movimento] Text, [Codigo da Agencia] Integer, [Numero da Conta] Text, [Saldo na Data] Real)"
        fields = ['Data do Movimento', 'Codigo da Agencia', 'Numero da Conta', 'Saldo na Data']
        types = ['Datetime', 'Integer', 'Text', 'Decimal']
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
        
    def test_get_sql_key(self):
        self.assertEqual("", lib.get_sql_key("", "", ""))
        message = "and tb1.[Codigo da Agencia] = tb2.[Codigo da Agencia] and tb1.[Numero da Conta] = tb2.[Numero da Conta]"
        self.assertEqual(message, lib.get_sql_key("tb1", "tb2", recon_def))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
