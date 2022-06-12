import sys
sys.path.append("..")

import unittest
from src.corelib import CoreLib
lib = CoreLib()

class CoreLibTest(unittest.TestCase):
    def setUp(self):
        pass
    
    # merge table structure
    def test_get_table_structure(self):
        # one side only
        f1  = []
        t1   = []
        f2  = ["name", "age", "salary"]
        t2   = ["text", "integer", "decimal"]
        f,t = lib.get_table_structure(f1, t1, f2, t2)
        self.assertEqual(3, len(f))
        self.assertEqual(3, len(t))
        # merge and remove duplicates
        f1  = ["name", "age"]
        t1   = ["text", "integer"]
        f2  = ["name", "age", "salary"]
        t2   = ["text", "integer", "decimal"]
        f,t = lib.get_table_structure(f1, t1, f2, t2)
        self.assertEqual(3, len(f))
        self.assertEqual(3, len(t))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()