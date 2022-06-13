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
    last_used_worker_id = 1

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

        return dataset_id - 1

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

        @staticmethod
        def ForwardData():

            for description in LoadBalancer.buffer:
                if len(description.items) <= 0:
                    continue

                worker = LoadBalancer.__GetAvailableWorker()
                worker_processing_thread = threading.Thread(target=worker.ProcessData, args=(description,))
                worker_processing_thread.start()

        @staticmethod
        def __GetAvailableWorker():
            while True:
                active_workers = [worker for worker in LoadBalancer.workers.values() if
                                  LoadBalancer.worker_statuses[worker.id] == 'On']

                # If there is only one available worker, return it
                if len(active_workers) == 1:
                    if active_workers[0].is_available:
                        return active_workers[0]

                # Get next worker once it is available
                wanted_worker_id = LoadBalancer.__GetNextWorkerId()
                for worker in active_workers:
                    if worker.id == wanted_worker_id and worker.is_available:
                        LoadBalancer.last_used_worker_id = worker.id
                        return worker

                time.sleep(0.5)

        @staticmethod
        def __GetNextWorkerId():
            index = 0
            active_workers_ids = [worker.id for worker in LoadBalancer.workers.values() if
                                  LoadBalancer.worker_statuses[worker.id] == 'On']
            for worker_id in active_workers_ids:
                if worker_id == LoadBalancer.last_used_worker_id:
                    return active_workers_ids[index + 1]
                index += 1