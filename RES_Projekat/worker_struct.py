#Task 6: Struktura workera
class CollectionDescription:
    def __init__(self, id , dataset, historical_collection):
        self.id = id
        self.dataset= dataset
        self.historical_collection = historical_collection

class HistoricalCollection:
    def __init__(self, array_worker_property):
        self.array_worker_property= array_worker_property

class WorkerProperty:
    def __init__(self, code, worker_value):
        self.code=code
        self.workerValue=worker_value
