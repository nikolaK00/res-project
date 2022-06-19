import sqlite3
import threading

import config
from Constants.Codes import Code
from Constants.DataSets import DataSet, DATASETS
from Models.CollectionDescription import CollectionDescription
from Models.WorkerProperty import WorkerProperty


class Worker:
    def __init__(self, id, status=False, is_free=True):
        self.buffer = {
            0: [CollectionDescription(0, DataSet.DataSet_1, []), False],
            1: [CollectionDescription(1, DataSet.DataSet_2, []), False],
            2: [CollectionDescription(2, DataSet.DataSet_3, []), False],
            3: [CollectionDescription(3, DataSet.DataSet_4, []), False]
        }
        self.id = id
        self.status = status
        self.is_free = is_free

    @staticmethod
    def GetData(dataset_id):
        lock = threading.Lock()
        lock.acquire()
        con = sqlite3.connect('db.db')
        cur = con.cursor()
        query = f"""SELECT CODE, VALUE FROM DATASET{dataset_id}"""
        cur.execute(query)
        results = cur.fetchall()
        con.close()
        lock.release()

        data = []
        if results is not None:
            for result in results:
                data.append(WorkerProperty(result[0], result[1]))
        return data

    def ProcessData(self, data):
        self.is_free = False
        self.__LoadData(data)
        self.__CheckForReadyData()
        #self.__ProcessData()
        self.is_free = True

    def __LoadData(self, data):
        dataset_id = Worker.__IdentifyDatasetIndex(data)
        for item in data.items:
            wp = WorkerProperty(item.code, item.value)
            self.buffer[dataset_id][0].historical_collection.append(wp)

    @staticmethod
    def __IdentifyDatasetIndex(data):
        dataset_id = 0
        for dataset in DATASETS:
            if data.dataset == dataset:
                return dataset_id
            dataset_id += 1

    def __CheckForReadyData(self):
        for buffer_item in self.buffer.values():
            first_code = False
            second_code = False
            for wp in buffer_item[0].historical_collection:
                if wp.code == buffer_item[0].dataset.value[0]:
                    first_code = True
                elif wp.code == buffer_item[0].dataset.value[1]:
                    second_code = True

            if first_code and second_code:
                buffer_item[1] = True
            else:
                buffer_item[1] = False

    def __ProcessingData(self):
        for buffer_item in self.buffer.values():
            if buffer_item[1]:
                for wp in buffer_item[0].historical_collection:
                    if self.__ValidateDeadband(wp):
                        Worker.__StoreDataInDatabase(wp, buffer_item[0].id + 1)
                buffer_item[0].historical_collection.clear()

    @staticmethod
    def __StoreDataInDatabase(wp, dataset_id):
        lock = threading.Lock()
        lock.acquire()
        con = sqlite3.connect('db.db')
        cur = con.cursor()
        query = f"""INSERT INTO DATASET{dataset_id} (CODE, VALUE) values ('{wp.code.name}', {wp.worker_value})"""
        cur.execute(query)
        con.commit()
        con.close()
        lock.release()
        
    @staticmethod
    def __CreateTables():
        lock = threading.Lock()
        lock.acquire()
        con = sqlite3.connect('db.db')
        cur = con.cursor()
        for dataset_id in range(1, 5):
            query = f"""CREATE TABLE DATASET{dataset_id} (CODE TEXT NOT NULL,
                                                          VALUE INT NOT NULL,
                                                          FORMATION_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                          CONSTRAINT DATASET{dataset_id}_CH CHECK (DATASET{dataset_id}.VALUE>=0))"""
            cur.execute(query)
        con.close()
        lock.release()

    def GetLatestValue(self, code):
        while True:
            try:
                lock = threading.Lock()
                lock.acquire()
                con = sqlite3.connect('db.db')
                cur = con.cursor()
                dataset_id = self.IdentifyDatasetByCode(code)
                query = f"""SELECT VALUE FROM DATASET{dataset_id} WHERE FORMATION_DATE = (SELECT MAX(FORMATION_DATE) FROM DATASET{dataset_id} WHERE CODE='{code.name}') AND CODE='{code.name}'"""
                cur.execute(query)
                result = cur.fetchone()
                con.close()
                lock.release()

                if result is None:
                    return None
                return result[0]
            except:
                self.__CreateTables()

    def __ValidateDeadband(self, wp):
        if wp.code == Code.CODE_DIGITAL:
            return True
        latest_value = self.GetLatestValue(wp.code)
        if latest_value is not None:
            if abs(latest_value - wp.worker_value) <= (latest_value * 0.02):
                return False
        return True

    def IdentifyDatasetByCode(self, code):
            for id in range(0, 4):
                if code in self.buffer[id][0].dataset.value:
                    return id + 1

    def __str__(self):
        return f'Worker {self.id}'
