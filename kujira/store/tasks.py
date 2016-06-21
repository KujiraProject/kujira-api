"""library to acces Mongo database allowing to insert and get tasks."""

import datetime
from pymongo import MongoClient
from pymongo import errors

class Mongodb(object):
    """contains managing of tasks in Kujira"""

    def __init__(self):
        """init"""
        self.client = MongoClient()
        self.connection = None
        self.tasks_collection = None
        self.tasks_audit_collection = None

    def connect(self, data_base_name, collection_name, history_collection_name):
        """sets connection
        :param data_base_name: name of the database
        :param collection_name: name of the main task collection
        :param history_collection_name: name of the history collection
        """
        self.connection = self.client[data_base_name]
        self.tasks_collection = self.connection[collection_name]
        self.tasks_audit_collection = self.connection[history_collection_name]

    def insert_task(self, param_dict):
        """insert task as json file into MongoDB with "PENDING" state
        :param param_dict: dictionary of task parameters
        """
        try:
            post = param_dict
            post['task_state'] = "PENDING"
            post['date'] = datetime.datetime.utcnow()
            self.tasks_collection.insert_one(post).inserted_id
        except errors.ConnectionFailure:
            raise exceptions.ConnectionError('Cannot connect to database!')
        except IndexError:
            raise exceptions.CursorError('Cursor empty, problem with database!')

    def get_task(self):
        """gets oldest task from task collection
        :returns dictionary with single task
        """
        try:
            temporary_cursor = (self.tasks_collection.find().sort("date", 1).limit(1))
            return self.tasks_collection.find_one({"_id": temporary_cursor[0]['_id']})
        except errors.ConnectionFailure:
            raise exceptions.ConnectionError('Cannot connect to database!')
        except IndexError:
            raise exceptions.CursorError('Cursor empty, problem with database!')

    def get_all_tasks(self):
        """gets all tasks from task collection
        :returns dictionary with all tasks
        """
        try:
            temporary_cursor = self.tasks_collection.find()
            tasks = []
            for doc in temporary_cursor:
                tasks.append(doc)
            return tasks
        except errors.ConnectionFailure:
            raise exceptions.ConnectionError('Cannot connect to database!')
        except IndexError:
            raise exceptions.CursorError('Cursor empty, problem with database!')

    def close_task(self, task_id):
        """moves task from main collection to historical one
        :param task_id: id of task to close
        """
        try:
            self.tasks_audit_collection.insert_one(self.tasks_collection.find_one({"_id": task_id}))
            self.tasks_collection.delete_one({"_id": task_id})
        except errors.ConnectionFailure:
            raise exceptions.TransactionError('Coulnt finish transaction')

    def update_tasks(self, task):
        """changes task state in main collection
        :param task_id: id of task to update
        :param new_state: new task state as string
        """
        return self.tasks_collection.update(
            {"date": task["date"]},
            {"$set": {"subtask": task["subtask"]}}
        )