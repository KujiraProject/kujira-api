'''
library to acces Mongo database allowing to insert and get tasks.
'''

import datetime
from pymongo import MongoClient

class Mongodb(object):
    '''contains connecting, inserting and geting tasks from database'''

    def __init__(self):
        self.client = MongoClient()
        self.database_connection = None
        self.database_collection = None
        self.database_collection_history = None
        self.post = None
        self.document = None

    def connect(self, data_base_name, collection_name, history_collection_name):
        '''method setting up the connection to database'''
        self.database_connection = self.client[data_base_name]
        self.database_collection = self.database_connection[collection_name]
        self.database_collection_history = self.database_connection[history_collection_name]


    def insert_task(self, name):
        '''method inserting task(actually just a name) as record into specified
         collections in database, auto generated date, to allow getting oldest event'''
        self.post = {"name": name, "date": datetime.datetime.utcnow()}
        return self.database_collection.insert_one(self.post).inserted_id


    def get_task(self):
        '''gets the newest task from database, deletes it and then inserts into
        historical collection with beginning state "doing"'''
        temporary_cursor = (self.database_collection.find().sort("date", 1).limit(1))
        self.document = self.database_collection.find_one({"_id": temporary_cursor[0]['_id']})
        self.post = {"_id":self.document['_id'],
                     "name":self.document['name'],
                     "date": datetime.datetime.utcnow(), "state": "doing"}
        self.database_collection_history.insert_one(self.post)
        self.database_collection.delete_one({"_id": self.document['_id']})
        return self.document

    def update_evaluated_task(self, task_id, new_state):
        '''can change state in historical collection'''
        return self.database_collection_history.update_one(
            {"_id": task_id},
            {"$set": {"state": new_state}}
        )

