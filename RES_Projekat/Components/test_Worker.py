from sys import path
from os import getcwd
import unittest
from unittest.mock import patch, Mock
path.append(getcwd()[1:-17])
from RES_Projekat.Components.Worker import Worker
from RES_Projekat.Constants import DataSets


class TestWorker(unittest.TestCase):
    def setUp(self) -> None:
        self.worker = Worker(1)

    @patch("Components.Worker.sqlite3")
    def test_GetData(self, var):
        var.connect().cursor().fetchall.return_value = None
        self.assertEqual(Worker.GetData(1), [], msg="Return value should be empty list!")

        var.connect().cursor().fetchall.return_value = [[1, 2], ["one", "two"]]
        self.assertEqual(Worker.GetData(2)[0].code, 1, msg="Code of first WorkerPropery should be 1!")

    def test_IdentifyDatasetIndex(self):
        with patch("Components.Worker.DATASETS", [1, 2, 3]):
            data = Mock()
            data.dataset = 10
            self.assertEqual(Worker.IdentifyDatasetIndex(data), None, msg="Return value should be None!")

        with patch("Components.Worker.DATASETS", [1, 2, 10]):
            data = Mock()
            data.dataset = 10
            self.assertEqual(Worker.IdentifyDatasetIndex(data), 2, msg="Return value should be None!")

    @patch("Components.Worker.sqlite3")
    def test_GetLatestValue(self, var):
        code = Mock()
        code.name = ""
        var.connect().cursor().fetchone.return_value = None
        self.assertEqual(self.worker.GetLatestValue(code), None, msg="Return value should be None!")

    def test_ValidateDeadband(self):
        wp = Mock()
        wp.code = ""
        wp.worker_value = 2
        with patch("Components.Worker.Worker.GetLatestValue", return_value=None):
            self.assertEqual(self.worker.ValidateDeadband(wp), True, msg="Return value should be None!")

        with patch("Components.Worker.Worker.GetLatestValue", return_value=3):
            with patch("builtins.abs", return_value=1):
                self.assertEqual(self.worker.ValidateDeadband(wp), True, msg="Return value should be None!")

    def test_IdentifyDatasetByCode(self):
        data = Mock()
        data.dataset.value = [0, 1]
        with patch.object(self.worker, "buffer", [[data, data]]):
            self.assertEqual(self.worker.IdentifyDatasetByCode(0), 1, msg="Return value should be None!")

if __name__ == '__main__':
    unittest.main()