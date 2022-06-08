import threading
import time

from Components.Worker import Worker
from Constants.DataSets import DATASETS
from Models.Description import Description


class LoadBalancer:
    workers = {}
    worker_statuses = {}
    last_used_worker_id = 0

    @staticmethod
    def ReceiveData(item):
        dataset_id = LoadBalancer.__IdentifyDataset(item)

    @staticmethod
    def __IdentifyDataset(data):
        dataset_id = 0
        for dataset in DATASETS:
            if data.code in dataset:
                return dataset_id
            dataset_id += 1
