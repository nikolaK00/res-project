class LbStruct:
    def __init__(self, item, description, listadescr):
        self.item = item
        self.description = description
        self.listadescr = listadescr

class Item:
    def __init__(self, code, value):
        self.code = code
        self.value = value

class Description:
    def __init__(self, id, listait, dataset):
        self.id = id
        self.listait = listait
        self.dataset=dataset


class ListaDescriptiona:
    def __init__(self, descriptions):
        self.descriptions = descriptions
