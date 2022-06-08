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

    @staticmethod
    def Prompt():
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            questions = [
                {
                'type': 'list',
                'name': 'input',
                'message': 'Select action',
                'choices': ['Turn on new workers', 'Turn off existing workers']
                }
            ]
            answers = prompt.prompt(questions)
            if answers['input'] == 'Turn on new workers':
                Writer.__TurnOnWorkersPrompt()
            elif answers['input'] == 'Turn off existing workers':
                Writer.__TurnOffWorkersPrompt()

    @staticmethod
    def __TurnOnWorkersPrompt():
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
    def __TurnOffWorkersPrompt():
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
