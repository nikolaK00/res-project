from sys import path
from os import getcwd
import unittest
from unittest.mock import patch, Mock, MagicMock

from Components.Reader import Reader

path.append(getcwd()[1:-17])


class TestReader(unittest.TestCase):

    @patch("Components.Reader.sqlite3")
    def test_GetValues(self, var):
        code = Mock()
        code.name = ""
        var.connect().cursor().fetchall.return_value = None
        self.assertEqual(Reader.GetValues(code), [], msg="Return value should be None!")

        var.connect().cursor().fetchall.return_value = [1, 2, 3]
        self.assertEqual(Reader.GetValues(code), [1, 2, 3], msg="Return value should be None!")

    @patch("os.system", return_value=None)
    @patch("builtins.print", return_value=None)
    @patch("inquirer2.prompt.prompt", return_value={'date':1})
    @patch("Components.Reader.datetime")
    def test_GetDate(self, datetime, var1, var2, var3):
        datetime.strptime.return_value = 1
        self.assertEqual(Reader.GetDate(""), 1, msg="Return value should be one!")

    @patch("Components.Reader.datetime", autospec=True)
    def test_ValidateDate(self, datetime):
        datetime.strptime.return_value = 1
        self.assertEqual(Reader.ValidateDate(1), True, msg="Return value should be True!")

    @patch("inquirer2.prompt.prompt", return_value={'code':1})
    @patch("Components.Reader.Code", {1:1})
    def test_SelectCode(self, var):
        self.assertEqual(Reader.SelectCode(), 1, msg="Return value should be None!")


if __name__ == '__main__':
    unittest.main()