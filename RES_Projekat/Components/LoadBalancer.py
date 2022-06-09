import threading
import time

from Components.Worker import Worker
from Constants.DataSets import DATASETS
from Models.Description import Description


class LoadBalancer:
    buffer = [
        Description(id=0, items=[], dataset=DATASETS[0]),
        Description(id=1, items=[], dataset=DATASETS[1]),
        Description(id=2, items=[], dataset=DATASETS[2]),
        Description(id=3, items=[], dataset=DATASETS[3])
    ]
    workers = {}
    worker_statuses = {}
    last_used_worker_id = 0

    @staticmethod
    def ReceiveData(item):
        dataset_id = LoadBalancer.__IdentifyDataset(item)
        LoadBalancer.buffer[dataset_id].items.append(item)

    @staticmethod
    def __IdentifyDataset(data):
        dataset_id = 0
        for dataset in DATASETS:
            if data.code in dataset:
                return dataset_id
            dataset_id += 1

    @staticmethod
    def __GenerateWorkerId():
        new_worker_id = 1
        for worker in LoadBalancer.workers.values():
            if worker.id >= new_worker_id:
                new_worker_id = worker.id + 1

        return new_worker_id

    @staticmethod
    def TurnOnNewWorker(amount):
        for _ in range(amount):
            new_worker_id = LoadBalancer.__GenerateWorkerId()
            LoadBalancer.workers[new_worker_id] = Worker(new_worker_id)
            LoadBalancer.worker_statuses[new_worker_id] = 'On'

    @staticmethod
    def TurnOffExistingWorker(worker_name):
        wanted_worker_id = None
        for worker in LoadBalancer.workers.values():
            if worker.__str__() == worker_name:
                wanted_worker_id = worker.id

        LoadBalancer.worker_statuses[wanted_worker_id] = 'Off'