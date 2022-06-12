import sys
sys.path.append("..")

import unittest
from src.utillib import UtilLib

class UtilLibTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_xyz(self):
        self.assertEqual(1, 1)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()