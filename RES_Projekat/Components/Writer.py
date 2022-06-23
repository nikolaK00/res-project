import os
import time
from random import randint

from inquirer2 import prompt

import RES_Projekat.config
from RES_Projekat.Components.LoadBalancer import LoadBalancer
from RES_Projekat.Constants.Codes import Code
from RES_Projekat.Models.Item import Item


class Writer:
    @staticmethod
    def RunDataSending():
        while config.RUN_THREADS:
            time.sleep(2)
            code = Code(randint(1, 8))
            value = randint(1, 10000)
            new_item = Item(code, value)
            LoadBalancer.ReceiveData(new_item)
            if config.LOGGER_ACTIVE:
                print(f'[WRITER]:\t Send package\t{new_item}')

    @staticmethod
    def TurnOnWorkersPrompt():
        os.system('cls' if os.name == 'nt' else 'clear')
        questions = [
            {
                'type': 'input',
                'name': 'amount',
                'message': 'How many workers do you want to turn on',
                'validate': lambda x: True if Writer.__ValidateNumber(x) else 'Invalid'
            }
        ]
        answers = prompt.prompt(questions)
        LoadBalancer.TurnOnNewWorker(int(answers['amount']))

    @staticmethod
    def TurnOffWorkersPrompt():
        os.system('cls' if os.name == 'nt' else 'clear')
        choices = [{'name': worker.__str__()} for worker in LoadBalancer.workers.values() if
                   LoadBalancer.worker_statuses[worker.id] == 'On']
        if not choices:
            print('There are no turned on workers to turn off')
            input()
            return

        questions = [
            {
                'type': 'checkbox',
                'name': 'workers_to_turn_off',
                'message': 'Select workers to turn off',
                'choices': choices
            }
        ]
        answers = prompt.prompt(questions)

        for worker_name in answers['workers_to_turn_off']:
            LoadBalancer.TurnOffExistingWorker(worker_name)

    @staticmethod
    def ShowWorkerStatuses():
        for worker in LoadBalancer.workers.values():
            print(f'{worker}   {LoadBalancer.worker_statuses[worker.id]}')
        input()

    @staticmethod
    def __ValidateNumber(value):
        try:
            if int(value) < 0:
                return False
        except:
            return False
        return True
