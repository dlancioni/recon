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

    def process(self, filename):
        status, message, reports = corelib.process(filename)
        rpt1 = reports[0]
        data = fslib.get_csv_as_list(rpt1)
        self.assertEqual(status, True)
        for side in range(1, 3):
            if filename == "recon [en-us]":
                recon = "Recon 1"
                rule = "Rule 1"
            else:
                recon = "Conciliação 2"
                rule = "Regra 1"
            i = 1 if side == 1 else 4
            self.assertEqual(data[i][0], str(side))
            self.assertEqual(data[i][1], "")
            self.assertEqual(data[i][2], "")
            self.assertEqual(data[1][3] in ["Orphan", "Órfão"], True)
            self.assertEqual(data[i][4], "1")
            i+=1
            self.assertEqual(data[i][0], str(side))
            self.assertEqual(data[i][1], recon)
            self.assertEqual(data[i][2], rule)
            self.assertEqual(data[i][3] in ["Matched", "Batido"], True)
            self.assertEqual(data[i][4], "1")
            i+=1
            self.assertEqual(data[i][0], str(side))
            self.assertEqual(data[i][1], recon)
            self.assertEqual(data[i][2], rule)
            self.assertEqual(data[i][3] in ["Divergent", "Divergente"], True)
            self.assertEqual(data[i][4], "1")

    def test_process(self):
        utillib.cls()
        self.process("recon [en-us]")
        self.process("recon [pt-br]")

if __name__ == '__main__':
    unittest.main()