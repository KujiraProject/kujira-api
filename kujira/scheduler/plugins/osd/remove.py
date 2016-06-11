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
            return (False, "Removing OSD {0} from {1} is already in queue!" \
            .format(self.params['osd_id'], self.params['host']))

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
