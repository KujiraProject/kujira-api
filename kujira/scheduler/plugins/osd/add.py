# -*- coding: utf-8 -*-
"""This plugin describes task of adding an OSD to cluster"""

from kujira.scheduler.plugins.plugin import Plugin

class Add(Plugin):
    """Add an OSD to cluster"""
    name = 'kujira.osd.add'

    def is_valid(self):
        if 'host' not in self.params:
            return (False, "'host' param is required!")

        if 'device' not in self.params:
            return (False, "'device' param is required!")

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
                'arg': self.params['device'],
                'jid': None,
                'status': None,
            },
        ]

