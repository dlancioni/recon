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
    
    """ Test basic recon status [Matched, Divergent and Orphan] """
    def recon_status(self):

        recon_en = "test datatype (en-us)"
        recon_pt = "test datatype (pt-br)"

        status, message, reports = corelib.process(recon_en)
        self.assertEqual(status, True)
        self.assertEqual(message, "")
        self.assertEqual(len(reports), 2)
        data = fslib.get_csv_as_list(reports[0])
        self.check_synthetic(1, data, 1, 1, 1)
        self.check_synthetic(2, data, 2, 1, 1)

        status, message, reports = corelib.process(recon_pt)
        self.assertEqual(status, True)
        self.assertEqual(message, "")
        self.assertEqual(len(reports), 2)
        data = fslib.get_csv_as_list(reports[0])
        self.check_synthetic(1, data, 1, 1, 1)
        self.check_synthetic(2, data, 2, 1, 1)

    """ Trigger all tests """
    def test_run(self):
        self.recon_status()
        utillib.cls()

if __name__ == '__main__':
    unittest.main()