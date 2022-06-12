import sys
sys.path.append("..")

import unittest
from src.corelib import CoreLib
lib = CoreLib()

class CoreLibTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_get_table_structure(self):
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