import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")
from src.expirelib import ExpireLib

expirelib = ExpireLib()

class ExpireLibTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_expired(self):
        expired = expirelib.expired()
        self.assertEqual(expired, False)

if __name__ == '__main__':
    unittest.main()