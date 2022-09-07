import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")
from src.etllib import EtlLib
from src.validlib import ValidationLib
from src.msglib import MsgLib
from src.dblib import DbLib
from src.cfglib import ConfigLib
from src.fslib import FsLib        
from src.arealib import AreaLib

fslib = FsLib()        
cfglib = ConfigLib()
dblib = DbLib()
msglib = MsgLib()
validlib = ValidationLib()

class EtlLibTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def get_connection(self):
        path_temp = fslib.get_path_log(cfglib.get(1))
        debug = int(cfglib.get(6))
        cn = dblib.get_connection(path_temp, debug)
        cn = dblib.begin_tran(cn, debug)
        return cn

    def test_import_delimited(self):
        config = {
            "Id": "1",
            "Dados":
            [
                {
                    "Lado": "1",
                    "Nome": "Test 1",
                    "Tipo": "Delimitado",
                    "Delimitador": ";",
                    "Caminho": "",
                    "Arquivo": "text_delimited.txt",
                    "Inicio": "2",
                    "Campos":
                    [
                        {"Posição":"1", "Nome":"Inteiro", "Tipo":"Inteiro"},
                        {"Posição":"2", "Nome":"DataHora", "Tipo":"DataHora", "Mascara":"dd/MM/yyyy"},
                        {"Posição":"3", "Nome":"Texto", "Tipo":"Texto"},
                        {"Posição":"4", "Nome":"Decimal", "Tipo":"Decimal", "Mask":","},
                        {"Posição":"5", "Nome":"Default", "Tipo":"Texto", "Valor Padrão":"xyz"}
                    ]
                }
            ]
        }

        cn = self.get_connection()        
        AreaLib(1, "").process(cn, config)      
        EtlLib(1, "").process(cn, config)
        rs = dblib.query(cn, "select * from tb11")
        self.assertEqual(len(rs), 3)
        
    def test_import_positional(self):
        config = {
            "Id": "1",
            "Dados":
            [
                {
                    "Lado": "1",
                    "Nome": "Test",
                    "Tipo": "Positional",
                    "Caminho": "",
                    "Arquivo": "text_positional.txt",
                    "Inicio": "2",
                    "Campos":
                    [
                        {"Posição":"1",  "Tamanho":"1", "Nome":"Campo 1", "Tipo":"Inteiro"},
                        {"Posição":"3",  "Tamanho":"8", "Nome":"Campo 2", "Tipo":"DataHora", "Mascara":"yyyymmdd"},
                        {"Posição":"12", "Tamanho":"6", "Nome":"Campo 3", "Tipo":"Texto"},
                        {"Posição":"19", "Tamanho":"7", "Nome":"Campo 4", "Tipo":"Decimal", "Mascara":"."}
                    ]
                }
            ]
        }

        cn = self.get_connection()        
        AreaLib(1, "").process(cn, config)
        EtlLib(1, "").process(cn, config)
        rs = dblib.query(cn, "select * from tb11")
        self.assertEqual(len(rs), 4)
        
    def test_import_excel(self):
        config = {
            "Id": "1",
            "Dados":
            [
                {
                    "Lado": "1",
                    "Nome": "Test 1",
                    "Tipo": "Excel",
                    "Caminho": "",
                    "Arquivo": "excel.xlsx",
                    "Planilha": "Text",
                    "Inicio": "2",
                    "Campos":
                    [
                        {"Posição":"1", "Nome":"Ids", "Tipo":"Inteiro"},
                        {"Posição":"2", "Nome":"Dt", "Tipo":"DataHora", "Mascara":"dd/mm/yyyy"},
                        {"Posição":"3", "Nome":"Hr", "Tipo":"DataHora", "Mascara":"hh:mm:ss"},
                        {"Posição":"4", "Nome":"Dh", "Tipo":"DataHora", "Mascara":"dd/mm/yyyy hh:mm:ss"},
                        {"Posição":"5", "Nome":"D4", "Tipo":"Decimal", "Mascara":","},
                        {"Posição":"6", "Nome":"D8", "Tipo":"Decimal", "Mascara":","},
                        {"Posição":"7", "Nome":"M1", "Tipo":"Decimal", "Mascara":","}
                    ]
                }
            ]
        }
        
        cn = self.get_connection()        
        AreaLib(1, "").process(cn, config)
        EtlLib(1, "").process(cn, config)
        rs = dblib.query(cn, "select * from tb11")
        self.assertEqual(len(rs), 1)
        
    def test_import_db_pgsql(self):
        config = {
            "Id": "1",
            "Dados":
            [
                {
                    "Lado": "1",
                    "Nome": "Test Db",
                    "Tipo": "Db",
                    "Conector": "connector_pgsql.cfg",
                    "Consulta": "select 1 Id, 'Description 1' Description",
                    "Campos":
                    [
                        {"Posição":"1", "Nome":"Field 1", "Tipo":"Integer"},
                        {"Posição":"2",  "Nome":"Field 2", "Tipo":"Text"}
                    ]
                }
            ]
        }

        cn = self.get_connection()
        AreaLib(1, "").process(cn, config)
        EtlLib(1, "").process(cn, config)
        rs = dblib.query(cn, "select * from tb11")
        self.assertEqual(len(rs), 1)
        
    def test_import_db_mysql(self):
        config = {
            "Id": "1",
            "Dados":
            [
                {
                    "Lado": "1",
                    "Nome": "Test Db",
                    "Tipo": "Db",
                    "Conector": "connector_mysql.cfg",
                    "Consulta": "select 1 Id, 'Description 1' Description",
                    "Campos":
                    [
                        {"Posição":"1", "Nome":"Field 1", "Tipo":"Integer"},
                        {"Posição":"2",  "Nome":"Field 2", "Tipo":"Text"}
                    ]
                }
            ]
        }

        cn = self.get_connection()
        AreaLib(1, "").process(cn, config)
        EtlLib(1, "").process(cn, config)
        rs = dblib.query(cn, "select * from tb11")
        self.assertEqual(len(rs), 1)
        
    def test_import_db_mssql(self):
        config = {
            "Id": "1",
            "Dados":
            [
                {
                    "Lado": "1",
                    "Nome": "Test Db",
                    "Tipo": "Db",
                    "Conector": "connector_mssql.cfg",
                    "Consulta": "select 1 'Id', 'Name 1' 'Name'",
                    "Campos":
                    [
                        {"Posição":"1", "Nome":"Field 1", "Tipo":"Inteiro"},
                        {"Posição":"2",  "Nome":"Field 2", "Tipo":"Texto"}
                    ]
                }
            ]
        }

        cn = self.get_connection()
        AreaLib(1, "").process(cn, config)
        EtlLib(1, "").process(cn, config)
        rs = dblib.query(cn, "select * from tb11")
        self.assertEqual(len(rs), 1)

if __name__ == '__main__':
    unittest.main()
