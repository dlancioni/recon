import sys
sys.path.append("..")

import unittest
from src.sqllib import SqlLib
lib = SqlLib()

class CoreLibTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_field_type(self):
        self.assertEqual("", lib.get_field_type(""))
        self.assertEqual("real", lib.get_field_type("decimal"))
        self.assertEqual("text", lib.get_field_type("datetime"))

    def test_get_field_type(self):
        self.assertEqual("", lib.get_field_list(""))
        self.assertEqual("text, decimal", lib.get_field_list(["text","decimal"]))
        self.assertEqual("text, sum(decimal) decimal", lib.get_field_list(["text","decimal"], ["text", "decimal"], ["", "sum"]))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()