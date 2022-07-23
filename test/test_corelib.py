import os
import sys
import csv
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")
from src.corelib import CoreLib
from src.fslib import FsLib
from src.utillib import UtilLib
corelib = CoreLib()
fslib = FsLib()
utillib = UtilLib()

class CoreLibTest(unittest.TestCase):

    def setUp(self):
        pass        
    
    def tearDown(self):
        pass
    
    def check_synthetic(self, side, data, matched, divergent, orphan):
        SIDE, STATUS, TOTAL = 0, 1, 2
        line = 1 if side == 1 else 4
        self.assertEqual(data[line][SIDE], str(side))
        self.assertEqual(data[line][STATUS] in ["Matched", "Batido"], True)
        self.assertEqual(data[line][TOTAL], str(matched))
        line += 1
        self.assertEqual(data[line][SIDE], str(side))
        self.assertEqual(data[line][STATUS] in ["Divergent", "Divergente"], True)
        self.assertEqual(data[line][TOTAL], str(divergent))            
        line += 1            
        self.assertEqual(data[line][SIDE], str(side))
        self.assertEqual(data[line][STATUS] in ["Orphan", "Órfão"], True)
        self.assertEqual(data[line][TOTAL], str(orphan))
    
    def basic(self):

        status, message, reports = corelib.process("recon [en-us]")
        self.assertEqual(status, True)
        self.assertEqual(message, "")
        self.assertEqual(len(reports), 3)
        data = fslib.get_csv_as_list(reports[0])
        self.check_synthetic(1, data, 1, 1, 1)
        self.check_synthetic(2, data, 2, 1, 1)

        status, message, reports = corelib.process("recon [pt-br]")
        self.assertEqual(status, True)
        self.assertEqual(message, "")
        self.assertEqual(len(reports), 3)
        data = fslib.get_csv_as_list(reports[0])
        self.check_synthetic(1, data, 1, 1, 1)
        self.check_synthetic(2, data, 2, 1, 1)
        
    def test_run(self):
        utillib.cls()
        self.basic()

if __name__ == '__main__':
    unittest.main()