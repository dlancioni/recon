import os
import sys
import pathlib
import unittest
sys.path.append("..")
sys.path.insert(1, pathlib.Path().resolve()._str + "\\recon\\")

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