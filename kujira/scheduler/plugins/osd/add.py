# -*- coding: utf-8 -*-
"""This plugin describes task of adding an OSD to cluster"""

from kujira.scheduler.plugins.plugin import Plugin

class Add(Plugin):
    """Add an OSD to cluster"""
    salt_module_name = 'kujira.osd.add'

    def is_valid(self):
        if 'host' not in self.params:
            return (False, "'host' param is required!")

        if 'device' not in self.params:
            return (False, "'device' param is required!")

        return (True, None)

    def can_run(self):
        if not self.check_if_exists():
            return (False, "Adding an OSD on device {0} on host {1} " \
            "is already in queue!".format(self.params['device'],
                                          self.params['host']))

        return (True, None)

    def title(self):
        return "Add OSD on device {device} on node {node}".format(
            device=self.params['device'],
            node=self.params['host'])

    def subtasks(self):
        subtasks = super(Add, self).subtasks()
        subtasks[0]['device'] = self.params['device']
        return subtasks

