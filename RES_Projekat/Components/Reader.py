import os
import sqlite3
import threading
from datetime import datetime

from inquirer2 import prompt

from Components.Worker import Worker
from Constants.Codes import CODES, Code


class Reader:
    @staticmethod
    def ShowLastValueByCode():
        code = Reader.__SelectCode()
        w = Worker(1)
        value = w.GetLatestValue(code)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'Latest value for {code} is {value}')
        input()

    @staticmethod
    def ShowValuesByTimeInterval():
        code = Reader.__SelectCode()
        data = Reader.__GetValues(code)

        start_date = Reader.__GetDate('Start date')
        end_date = Reader.__GetDate('End date')

        date_data = []
        for result in data:
            date = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
            date_data.append((date, result[1], result[2]))

        for data_point in date_data:
            if start_date <= data_point[0] <= end_date:
                print(f'{data_point[1]}\t{data_point[2]}')
        input()

    @staticmethod
    def __GetValues(code):
        w = Worker(1)
        dataset_id = w.IdentifyDatasetByCode(code)

        lock = threading.Lock()
        lock.acquire()
        con = sqlite3.connect('db.db')
        cur = con.cursor()
        query = f"""SELECT FORMATION_DATE, CODE, VALUE FROM DATASET{dataset_id} WHERE CODE = '{code.name}'"""
        cur.execute(query)
        results = cur.fetchall()
        con.close()
        lock.release()

        if results is None:
            return []
        return results

    @staticmethod
    def __GetDate(text):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(text)
        questions = [
            {
                'type': 'input',
                'name': 'date',
                'message': 'Enter a date in format YYYY-MM-DD-HH-MM-SS',
                'validate': lambda x: True if Reader.__ValidateDate(x) else 'Invalid date'
            }
        ]
        answers = prompt.prompt(questions)
        date = datetime.strptime(answers['date'], '%Y-%m-%d-%H-%M-%S')
        return date

    @staticmethod
    def __ValidateDate(value):
        try:
            date = datetime.strptime(value, '%Y-%m-%d-%H-%M-%S')
            return True
        except:
            return False

    @staticmethod
    def __SelectCode():
        questions = [
            {
                'type': 'list',
                'name': 'code',
                'message': 'Code',
                'choices': CODES
            }
        ]
        answers = prompt.prompt(questions)
        code = Code[answers['code']]
        return code
