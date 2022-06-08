import os
import time
from random import randint

from Components.LoadBalancer import LoadBalancer
from Constants.Codes import CODES
from Models.Item import Item


class Writer:
    @staticmethod
    def RunDataSending():
        while True:
            time.sleep(2)
            code = CODES[randint(0, 7)]
            value = randint(1, 10000)
            new_item = Item(code, value)
            LoadBalancer.ReceiveData(new_item)
