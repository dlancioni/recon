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
    
    def test_get_file(self):
        path1 = "c:\\temp\\abc.txt"
        path2 = etllib.get_file("c:\\temp\\abc.txt")
        self.assertEqual(path1, path2)
        path1 = "C:\\Users\\david\\Developer\\recon\\etc\\recon_01.txt"
        path2 = etllib.get_file("etc:recon_01.txt")
        self.assertEqual(path1, path2)        

    def test_import_file(self):
        path = fslib.get_dir_etc("recon_01.json")
        setup = fslib.get_json(path)
        ds = setup["Datasources"][0]
        cn = dblib.get_connection()
        cursor = cn.cursor()
        cursor.execute("create table if not exists tb11 (Integer integer, Decimal decimal, Text text, Datetime datetime)")
        id = setup["Id"]
        name = setup["Name"]
        etllib = EtlLib(id, name)
        etllib.import_file(cn, ds)
        cursor.execute("select * from tb11")
        rows = cursor.fetchall()
        self.assertEqual(3, len(rows))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()