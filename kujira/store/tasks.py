'''
library to acces Mongo database allowing to insert and get tasks.
'''

import datetime
from pymongo import MongoClient

class Mongodb(object):
    '''contains connecting, inserting and geting tasks from store'''

    def __init__(self):
        self.client = MongoClient()
        self.connection = None
        self.tasks_collection = None
        self.tasks_audit_collection = None
        self.post = None
        self.document = None

    def connect(self, data_base_name, collection_name, history_collection_name):
        '''method setting up the connection to store'''
        self.connection = self.client[data_base_name]
        self.tasks_collection = self.connection[collection_name]
        self.tasks_audit_collection = self.connection[history_collection_name]

    def insert_task(self, param_dict):
        '''method inserting task(actually just a name) as record into specified
         collections in store, auto generated date, to allow getting oldest event'''
        post = param_dict
        post['task_state'] = "pending"
        post['date'] = datetime.datetime.utcnow()
        return self.tasks_collection.insert_one(post).inserted_id

    def get_task(self):
        '''gets the newest task from store, deletes it and then inserts into
        historical collection with beginning state "doing"'''
        temporary_cursor = (self.tasks_collection.find().sort("date", 1).limit(1))
        self.document = self.tasks_collection.find_one({"_id": temporary_cursor[0]['_id']})
        self.tasks_collection.update_one(
            {"_id": self.document["_id"]},
            {"$set": {"task_state": "doing"}}
        )
        return self.document

    def close_task(self, task_id):
        '''Closes task, removes from collection and inserts into audit collection'''
        self.tasks_collection.update_one(
            {"_id": task_id},
            {"$set": {"task_state": "done"}}
        )
        self.tasks_audit_collection.insert_one(self.tasks_collection.find_one({"_id": task_id}))
        self.tasks_collection.delete_one({"_id": task_id})

    def update_task_status(self, task_id, new_state):
        '''can change state in historical collection'''
        return self.tasks_collection.update_one(
            {"_id": task_id},
            {"$set": {"task_state": new_state}}
        )

