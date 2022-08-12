import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")
from src.dblib import DbLib

dblib = DbLib()

class UtilLibTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_connection_mysql(self):
        cn = dblib.get_connection_mysql("connector_mysql.cfg")
        self.assertEqual(cn.warning_count, 0)

    def test_connection_pgsql(self):
        cn = dblib.get_connection_pgsql("connector_pgsql.cfg")
        self.assertEqual(cn.status, 1)

if __name__ == '__main__':
    unittest.main()