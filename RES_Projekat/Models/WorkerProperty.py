class WorkerProperty:
    def __init__(self, code, worker_value):
        self.code = code
        self.worker_value = worker_value

    def __str__(self):
        return f'{self.code.name}\t{self.worker_value}'