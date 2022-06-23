from sys import path
from os import getcwd
path.append(getcwd()[1:-17])

import unittest
from unittest.mock import patch, Mock
from RES_Projekat.Components.LoadBalancer import LoadBalancer
from RES_Projekat.Models.Description import Description


class TestLoadBalancer(unittest.TestCase):

    def test_IdentifyDataset(self):
        data = Mock()
        data.code = 2
        with patch("Components.LoadBalancer.DATASETS", [[1], [2], [3]]):
            self.assertEqual(LoadBalancer.IdentifyDataset(data), 1, msg="Return value should be one!")

    def test_PackageData(self):
        description = Mock()
        description.id = 1
        description.items = [1, 2, 3]
        description.dataset = "dataset"
        self.assertIsInstance(LoadBalancer.PackageData(description), Description, msg="Return value should be None!")

    def test_GenerateWorkerId(self):
        worker_1 = Mock()
        worker_2 = Mock()
        worker_1.id = 1
        worker_2.id = 2
        with patch.object(LoadBalancer, "workers", {1:worker_1, 2:worker_2}):
            self.assertEqual(LoadBalancer.GenerateWorkerId(), 3, msg="Return value should be 4!")


if __name__ == '__main__':
    unittest.main()