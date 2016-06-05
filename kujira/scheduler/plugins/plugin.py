# -*- coding: utf-8 -*-

from kujira.store.tasks import Mongodb

class Plugin(object):
    
    def __init__(self, **params):
        self.params = params
        self.mongo = Mongodb()
        self.mongo.connect("mydb", "tasks", "oldTasks")

    def is_valid(self):
        raise NotImplementedError("Plugin.is_valid must be implemented!")

    def can_run(self):
        raise NotImplementedError("Plugin.can_run must be implemented!")
