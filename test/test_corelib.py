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
    
    def confere(self, data, recon, rule, matched, divergent, orphan):
        for side in range(1, 3):
            i = 1 if side == 1 else 4
            total_match = matched[0] if side == 1 else matched[1]
            total_divergent = divergent[0] if side == 1 else divergent[1]
            total_orphan = orphan[0] if side == 1 else orphan[1]
            
            self.assertEqual(data[i][0], str(side))
            self.assertEqual(data[i][1], "")
            self.assertEqual(data[i][2], "")
            self.assertEqual(data[1][3] in ["Orphan", "Órfão"], True)
            self.assertEqual(data[i][4], str(total_orphan))
            i+=1
            self.assertEqual(data[i][0], str(side))
            self.assertEqual(data[i][1], recon)
            self.assertEqual(data[i][2], rule)
            self.assertEqual(data[i][3] in ["Matched", "Batido"], True)
            self.assertEqual(data[i][4], str(total_match))
            i+=1
            self.assertEqual(data[i][0], str(side))
            self.assertEqual(data[i][1], recon)
            self.assertEqual(data[i][2], rule)
            self.assertEqual(data[i][3] in ["Divergent", "Divergente"], True)
            self.assertEqual(data[i][4], str(total_divergent))
    
    def basic(self):
        
        status, message, reports = corelib.process("recon [en-us]")
        self.assertEqual(status, True)
        self.assertEqual(message, "")
        self.assertEqual(len(reports), 3)
        data = fslib.get_csv_as_list(reports[0])
        self.confere(data, "Recon 1", "Rule 1", [1,2], [1,1], [1,1])

        status, message, reports = corelib.process("recon [pt-br]")
        self.assertEqual(status, True)
        self.assertEqual(message, "")
        self.assertEqual(len(reports), 3)
        data = fslib.get_csv_as_list(reports[0])
        self.confere(data, "Conciliação 1", "Regra 1", [1,2], [1,1], [1,1])
        
    def test_run(self):
        utillib.cls()
        self.basic()

if __name__ == '__main__':
    unittest.main()