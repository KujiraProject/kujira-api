# -*- coding: utf-8 -*-

from datetime import datetime

class Plugin(object):

    def __init__(self, **params):
        self.create_date = datetime.now()
        self.params = params

    def set_db_instance(self, db):
        self.database = db

    def is_valid(self):
        raise NotImplementedError("Plugin.is_valid must be implemented!")

    def can_run(self):
        raise NotImplementedError("Plugin.can_run must be implemented!")

    def subtasks(self):
        raise NotImplementedError("Plugin.subtasks must be implemented!")

    def data(self):
        return {
            'title': self.name,
            'subtasks': self.subtasks(),
            'parallel': self.params['parallel']
       }
