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
                        {"Posição":"3",  "Tamanho":"8", "Nome":"Campo 2", "Tipo":"DataHora"},
                        {"Posição":"12", "Tamanho":"6", "Nome":"Campo 3", "Tipo":"Texto"},
                        {"Posição":"19", "Tamanho":"7", "Nome":"Campo 4", "Tipo":"Decimal"}
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
                    "Arquivo": "cc.xlsx",
                    "Planilha": "Saldo",
                    "Inicio": "2",
                    "Campos":
                    [
                        {"Posição":"1", "Nome":"Agencia", "Tipo":"Texto"},
                        {"Posição":"2", "Nome":"Conta", "Tipo":"Texto"},
                        {"Posição":"3", "Nome":"Saldo", "Tipo":"Decimal", "Mask":","}
                    ]
                }
            ]
        }
        
        cn = self.get_connection()        
        AreaLib(1, "").process(cn, config)
        EtlLib(1, "").process(cn, config)
        rs = dblib.query(cn, "select * from tb11")
        self.assertEqual(len(rs), 3)
        
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
                    "Consulta": "select * from public.tb1",
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
        self.assertEqual(len(rs), 3)
        
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
                    "Consulta": "select * from tb1",
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
        self.assertEqual(len(rs), 2)

if __name__ == '__main__':
    unittest.main()
