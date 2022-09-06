import os
import sys
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")
from src.maillib import MailLib
from src.utillib import UtilLib

mailib = MailLib()

class MailLibTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_send_mail(self):       
        sent = mailib.send(["david.lancioni@live.com"], "Subject", "Body")
        self.assertEqual(sent, False) # remember password is commited as blank!!

if __name__ == '__main__':
    unittest.main()