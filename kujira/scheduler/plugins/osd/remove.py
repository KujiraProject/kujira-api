# -*- coding: utf-8 -*- 

from kujira.scheduler.plugins.plugin import Plugin

class Remove(Plugin):
    
    def is_valid(self):
        return (True, None)

    def can_run(self):
        if not self.mongo_check():
            return (False, "Mongo check failed.")
        return (True, None)

    def ceph_query(self):
        pass
        
    def mongo_check(self):
        tasks = self.mongo.get_all_tasks()
        
        for task in tasks:
            if task["title"] == "osd.remove" and task["arg"] == self.params["arg"]:
                return False
        return True
