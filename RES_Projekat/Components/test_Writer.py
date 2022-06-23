from sys import path
from os import getcwd
import unittest
from unittest import mock
path.append(getcwd()[1:-17])
from RES_Projekat.Components.Writer import Writer


class TestWriter(unittest.TestCase):
    def test_ValidateNumber(self):
        self.assertEqual(Writer.ValidateNumber(-7), False, msg="Number is less than 0!")
        self.assertEqual(Writer.ValidateNumber(0), True, msg="Should return True!")
        self.assertEqual(Writer.ValidateNumber(1), True, msg="Should return True!")


if __name__ == '__main__':
    unittest.main()