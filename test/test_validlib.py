import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")
from src.etllib import EtlLib
from src.validlib import ValidationLib
from src.msglib import MsgLib
from src.setuplib import SetupLib
from src.constlib import const

msglib = MsgLib()
validlib = ValidationLib()
setuplib = SetupLib()

class EtlLibTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_validate_datasource_file_delimited(self):
        datasource = {
            "Lado": "1",
            "Nome": "Lado 1",
            "Tipo": "Delimitado",
            "Delimitador": ";",
            "Caminho": "c:\\temp\\",
            "Arquivo": "File.txt",
            "Inicio": "2",
            "Campos":
            [
                {"Posição":"1", "Nome":"Campo 1", "Tipo":"Inteiro"},
                {"Posição":"2", "Nome":"Campo 2", "Tipo":"Datahora"},
                {"Posição":"3", "Nome":"Campo 3", "Tipo":"Texto"},
                {"Posição":"4", "Nome":"Campo 4", "Tipo":"Decimal", "Mascara":","}
            ]
        }

        validlib.validate_datasource_file_delimited(datasource)

    def test_validate_datasource_file_positional(self):
        datasource = {
            "Side": "2",
            "Name": "Side 2",
            "Type": "Posicional",
            "Path": "c:\\temp\\",
            "File": "File.txt",
            "Start": "2",
            "Fields":
            [
                {"Position":"1", "Size":"1", "Name":"Campo 1", "Type":"Integer"},
                {"Position":"3", "Size":"8", "Name":"Campo 2", "Type":"Datetime"},
                {"Posição":"12", "Size":"6", "Name":"Campo 3", "Type":"Text"},
                {"Posição":"19", "Size":"7", "Name":"Campo 4", "Type":"Decimal"}
            ]
        }
        
        validlib.validate_datasource_file_positional(datasource)
        
    def test_validate_datasource_file_excel(self):
        datasource = {
            "Lado": "1",
            "Nome": "Lado 1",
            "Tipo": "Excel",
            "Arquivo": "File.xlsx",
            "Sheet": "Plan1",
            "Caminho": "c:\\temp\\",
            "Inicio": "1",
            "Fields":
            [
                {"Posição":"1", "Nome":"Campo 1", "Tipo":"Inteiro"},
                {"Posição":"2", "Nome":"Campo 2", "Tipo":"Datahora"},
                {"Posição":"3", "Nome":"Campo 3", "Tipo":"Texto"},
                {"Posição":"4", "Nome":"Campo 4", "Tipo":"Decimal", "Mascara":","}
            ]
        }

        validlib.validate_datasource_file_excel(datasource)
        
    def test_validate_datasource_db(self):
        datasource = {
            "Lado": "2",
            "Nome": "Side 2",
            "Tipo": "Db",
            "Conector": "connector_pgsql.cfg",
            "Consulta": "select * from public.tb1",
            "Campos":
            [
                {"Posição":"1", "Nome":"Campo 1", "Tipo":"Inteiro"},
                {"Posição":"2", "Nome":"Campo 2", "Tipo":"Datahora"},
                {"Posição":"3", "Nome":"Campo 3", "Tipo":"Texto"},
                {"Posição":"4", "Nome":"Campo 4", "Tipo":"Decimal", "Mascara":","}
            ]
        }

        validlib.validate_datasource_db(datasource)
        
    def test_validate(self):
        config = {
            "Datasources":
            [
                {
                    "Lado": "1",
                    "Nome": "Lado 1",
                    "Tipo": "Delimitado",
                    "Delimitador": ";",
                    "Caminho": "c:\\temp\\",
                    "Arquivo": "File.txt",
                    "Inicio": "2",
                    "Campos":
                    [
                        {"Posição":"1", "Nome":"Campo 1", "Tipo":"Inteiro"},
                    ]
                },
                {
                    "Side": "1",
                    "Name": "Side 2",
                    "Type": "Posicional",
                    "Path": "c:\\temp\\",
                    "File": "File.txt",
                    "Start": "2",
                    "Fields":
                    [
                        {"Position":"1", "Size":"1", "Name":"Campo 1", "Type":"Integer"},
                    ]
                },
                {
                    "Lado": "2",
                    "Nome": "Lado 1",
                    "Tipo": "Excel",
                    "Arquivo": "File.xlsx",
                    "Sheet": "Plan1",
                    "Caminho": "c:\\temp\\",
                    "Inicio": "1",
                    "Fields":
                    [
                        {"Posição":"1", "Nome":"Campo 1", "Tipo":"Inteiro"},
                    ]
                },
                {
                    "Lado": "2",
                    "Nome": "Side 2",
                    "Tipo": "Db",
                    "Conector": "connector_pgsql.cfg",
                    "Consulta": "select * from public.tb1",
                    "Campos":
                    [
                        {"Posição":"1", "Nome":"Campo 1", "Tipo":"Inteiro"},
                    ]
                }
            ]
        }

        validlib.validate_datasources(config)
        validlib.validate_datasources_sides(config)
        

if __name__ == '__main__':
    unittest.main()
