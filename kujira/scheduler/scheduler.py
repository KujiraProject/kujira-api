# -*- coding: utf-8 -*-
import Queue
from threading import Lock

from plugins.config import PLUGINS

class Scheduler(object):
    instance = None

    def __init__(self):
        # Mongo
        self.lock = Lock()

    def instance(self):
        if not Scheduler.instance:
            Scheduler.instance = Scheduler()

        return Scheduler.instance
    
    def add_task(self, name, **params): # name = 'osd.add'
        try:
            self.lock.acquire()
            if not name in PLUGINS:
                return (False, "Could not find plugin: {}".format(name))

            plugin = PLUGINS[name](**params)
            
            is_valid_result = plugin.is_valid()
            if not is_valid_result[0]:
                return is_valid_result

            can_run_result = plugin.can_run()
            if not can_run_result[0]:
                return can_run_result

            # Mongo
        except:
            pass
        finally:
            self.lock.release()
            
