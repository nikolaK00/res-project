class Item:
    def __init__(self, code, value):
        self.code = code
        self.value = value

    def __str__(self):
        return f'{self.code.name}\t{self.value}'