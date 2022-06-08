class Worker:
    def __init__(self, id):
        self.id = id
        self.is_available = True

    def ProcessData(self, description_list):
        pass

    def SaveData(self):
        pass

    def __str__(self):
        return f'Worker {self.id}'
