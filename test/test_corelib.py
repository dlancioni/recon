import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")
from src.corelib import CoreLib
from src.fslib import FsLib
corelib = CoreLib()
fslib = FsLib()

class CoreLibTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_tag_english_portuguese(self):
        """
        Test case: Validate ALL tags in configuration file
        Comment: As we can configure the recon using portuguese or english fields,
        we need to make sure the code will touch all possible labels.
        """
        status, error, reports = corelib.process("recon [en_us].cfg")
        rpt0 = fslib.get_csv_as_list(reports[0])
        rpt1 = fslib.get_csv_as_list(reports[1])
        rpt2 = fslib.get_csv_as_list(reports[2])
        print(rpt0)

        status, error, reports = corelib.process("recon [pt_br].cfg")
        rpt0 = fslib.get_csv_as_list(reports[0])
        rpt1 = fslib.get_csv_as_list(reports[1])
        rpt2 = fslib.get_csv_as_list(reports[2])
        print(rpt0)
        
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()