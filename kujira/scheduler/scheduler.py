# -*- coding: utf-8 -*-
import Queue
from threading import Lock
from plugins.config import PLUGINS
from kujira.store.tasks import Mongodb

import logging

log = logging.getLogger(__name__)

class Scheduler(object):
    instance = None

    def __init__(self):
        self.lock = Lock()
        self.mongo = Mongodb()
        self.mongo.connect("mydb", "tasks", "oldTasks")

    def instance(self):
        if not Scheduler.instance:
            Scheduler.instance = Scheduler()

        return Scheduler.instance
    
    def add_task(self, name, **params): # name = 'osd.add'
        try:
            self.lock.acquire()
            log.info("Adding new task to queue...")

            if not name in PLUGINS.keys():
                return (False, "Could not find plugin: {}".format(name))

            plugin = PLUGINS[name](**params)

            plugin.set_db_instance(self.mongo)

            is_valid_result = plugin.is_valid()
            if not is_valid_result[0]:
                return is_valid_result

            can_run_result = plugin.can_run()
            if not can_run_result[0]:
                return can_run_result

            print self.mongo.insert_task({"title":name,
                                    "arg":params["arg"]})

            return (True, None)
        except NotImplementedError as e:
            log.error("Some function in plugin is not implemented: " + str(e))
        except:
            log.error("An unknown error occurred!")
        finally:
            self.lock.release()
            
