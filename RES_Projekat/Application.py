import os
import threading

from inquirer2 import prompt

import config
from Components.Reader import Reader
from Components.LoadBalancer import LoadBalancer
from Components.Writer import Writer


class Application:
    @staticmethod
    def Start():
        automatic_data_sending_thread = threading.Thread(target=Writer.RunDataSending, args=())
        automatic_data_forwarding_thread = threading.Thread(target=LoadBalancer.ForwardData, args=())

        automatic_data_sending_thread.start()
        automatic_data_forwarding_thread.start()

        Application.__Prompt()

    @staticmethod
    def __Prompt():
        while config.RUN_THREADS:
            os.system('cls' if os.name == 'nt' else 'clear')
            questions = [
                {
                    'type': 'list',
                    'name': 'input',
                    'message': 'Select action',
                    'choices': ['Show worker statues', 'Show last value by Code', 'Show code values in a time interval',
                                'Turn on new workers', 'Turn off existing workers', 'Track logger', 'Exit']
                }
            ]
            answers = prompt.prompt(questions)
            if answers['input'] == 'Show worker statues':
                Writer.ShowWorkerStatuses()
            elif answers['input'] == 'Show last value by Code':
                Reader.ShowLastValueByCode()
            elif answers['input'] == 'Show code values in a time interval':
                Reader.ShowValuesByTimeInterval()
            elif answers['input'] == 'Turn on new workers':
                Writer.TurnOnWorkersPrompt()
            elif answers['input'] == 'Turn off existing workers':
                Writer.TurnOffWorkersPrompt()
            elif answers['input'] == 'Track logger':
                Application.__Log()
            elif answers['input'] == 'Exit':
                os.system('cls' if os.name == 'nt' else 'clear')
                config.RUN_THREADS = False

    @staticmethod
    def __Log():
        os.system('cls' if os.name == 'nt' else 'clear')
        config.LOGGER_ACTIVE = True
        input()
        config.LOGGER_ACTIVE = False
        os.system('cls' if os.name == 'nt' else 'clear')
