# -*- coding: utf-8 -*- 

from kujira.scheduler.plugins.plugin import Plugin

class Remove(Plugin):
    name = 'osd.remove'

    def is_valid(self):
        return (True, None)

    def can_run(self):
        if not self.check_if_exists():
            return (False, "Mongo check failed.")
        return (True, None)

    def ceph_query(self):
        pass
        
    def check_if_exists(self):
        tasks = self.mongo.get_all_tasks()
        
        for task in tasks:
            if (task["title"] == self.name and
               task["arg"] == self.params["arg"]):
                return False

        return True
