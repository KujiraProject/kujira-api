# -*- coding: utf-8 -*-
"""This plugin describes task of removing an OSD from cluster"""

from kujira.scheduler.plugins.plugin import Plugin

class Remove(Plugin):
    """Remove an OSD from cluster"""
    name = 'kujira.osd.remove'

    def is_valid(self):
        if 'host' not in self.params:
            return (False, "'host' param is required!")

        if 'osd_id' not in self.params:
            return (False, "'osd_id' param is required!")

        return (True, None)

    def can_run(self):
        if not self.check_if_exists():
            return (False, "Task already exists!")

        return (True, None)

    def subtasks(self):
        return [
            {
                'host': self.params['host'],
                'module': self.name,
                'arg': self.params['osd_id'],
                'jid': None,
                'status': None,
            },
        ]
        
    def check_if_exists(self):
        tasks = self.db.get_all_tasks()
        
        for task in tasks:
            for subtask in task['subtasks']:
                if (subtask['module'] == self.name and
                   subtask['arg'] == self.params['device']):
                    return False

        return True
