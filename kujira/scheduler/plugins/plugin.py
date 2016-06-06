# -*- coding: utf-8 -*-

from kujira.store.tasks import Mongodb
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

    def data(self):
        return {
            'name': self.name,
            'date': self.create_date.strftime('%c'),
            'params': self.params,
        }
