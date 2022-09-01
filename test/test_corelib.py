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

    def check_synthetic(self, side, data, matched, divergent, orphan):
        SIDE, STATUS, TOTAL = 0, 1, 2
        
        if matched > 0 and divergent > 0 and orphan > 0:
            line = 1 if side == 1 else 4
        if matched > 0 and divergent == 0 and orphan > 0:
            line = 1 if side == 1 else 3

        if matched > 0:
            self.assertEqual(data[line][SIDE], str(side))
            self.assertEqual(data[line][STATUS] in ["Matched", "Batido"], True)
            self.assertEqual(data[line][TOTAL], str(matched))
        if divergent > 0:
            line += 1
            self.assertEqual(data[line][SIDE], str(side))
            self.assertEqual(data[line][STATUS] in ["Divergent", "Divergente"], True)
            self.assertEqual(data[line][TOTAL], str(divergent))
        if orphan > 0:
            line += 1
            self.assertEqual(data[line][SIDE], str(side))
            self.assertEqual(data[line][STATUS] in ["Orphan", "Órfão"], True)
            self.assertEqual(data[line][TOTAL], str(orphan))

    def setUp(self):
        pass        
    
    def tearDown(self):
        pass
    
    """ Test basic recon status [Matched, Divergent and Orphan] """
    def test_recon_text(self):
        recon = "test_text.cfg"
        status, message, reports = corelib.process(recon)
        self.assertEqual(status, True)
        self.assertEqual(message, "")
        self.assertEqual(len(reports), 2)
        data = fslib.get_csv_as_list(reports[0])
        self.check_synthetic(1, data, 1, 1, 1)
        self.check_synthetic(2, data, 2, 1, 1)
        
    """ Test aggregate function [Sum, Max, Min, Avg] """ 
    def test_recon_aggregation(self):        
        recon = "test_aggreg.cfg"
        status, message, reports = corelib.process(recon)
        self.assertEqual(status, True)
        self.assertEqual(message, "")
        self.assertEqual(len(reports), 2)
        data = fslib.get_csv_as_list(reports[0])
        self.check_synthetic(1, data, 4, 1, 1)
        self.check_synthetic(2, data, 2, 1, 1)
            
    """ Test operators on compare [=, !=, >, >=, <, <=] """ 
    def test_recon_operators(self):        
        recon = "test_operator.cfg"
        status, message, reports = corelib.process(recon)
        self.assertEqual(status, True)
        self.assertEqual(message, "")
        self.assertEqual(len(reports), 2)
        data = fslib.get_csv_as_list(reports[0])
        self.check_synthetic(1, data, 1, 1, 1)
        self.check_synthetic(2, data, 1, 1, 1)
            
    """ Test multiple rules """ 
    def test_recon_multiple_rules(self):
        recon = "test_rules.cfg"
        status, message, reports = corelib.process(recon)
        self.assertEqual(status, True)
        self.assertEqual(message, "")
        self.assertEqual(len(reports), 2)
        data = fslib.get_csv_as_list(reports[0])
        self.check_synthetic(1, data, 3, 0, 1)
        self.check_synthetic(2, data, 3, 0, 1)

if __name__ == '__main__':
    unittest.main()