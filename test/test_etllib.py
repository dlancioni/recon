import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")

from src.dblib import DbLib
from src.fslib import FsLib
from src.etllib import EtlLib

dblib = DbLib()
fslib = FsLib()
etllib = EtlLib(0, "Test")        

class EtlLibTest(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_import_file(self):
        path = fslib.get_path_recon("", "saldo x extrato.json")
        recon = fslib.open_json(path)
        ds = recon["Datasources"][0]
        cn = dblib.get_connection()
        cursor = cn.cursor()
        cursor.execute("drop table if exists tb11")
        cursor.execute("create table tb11 (Id integer primary key, Id_Parent integer default 0, Recon text default '', Rule text default '', Status text default 'Orphan', [Data do Movimento] Text, [Codigo da Agencia] Integer, [Numero da Conta] Text, [Saldo na Data] Real)")
        id = recon["Id"]
        name = recon["Name"]
        etllib = EtlLib(id, name)
        etllib.import_file(cn, ds)
        cursor.execute("select * from tb11")
        rows = cursor.fetchall()
        self.assertEqual(4, len(rows))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()