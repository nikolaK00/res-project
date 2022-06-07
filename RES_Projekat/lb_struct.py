import time
from random import  randint
from load_balancer import LoadBalancer

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
        
class Writer:
    @staticmethod
    def RunDataSending():
        while True:
            time.sleep(2)
            code = randint(0, 7)
            value = randint(1, 10000)
            new_item = Item(code, value)
            LoadBalanser.LB_Receiver(code,value)
            
