import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")

from src.corelib import CoreLib
lib = CoreLib()

class CoreLibTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()