# -*- coding: utf-8 -*-
"""This plugin describes task of adding a monitor to cluster"""

from kujira.scheduler.plugins.plugin import Plugin

class Add(Plugin):
    """Add a monitor to cluster"""
    salt_module_name = 'kujira.mon.add'

    def is_valid(self):
        if 'host' not in self.params:
            return (False, "'host' param is required!")

        return (True, None)

    def can_run(self):
        if not self.check_if_exists():
            return (False, "Adding a monitor on {0} " \
            "is already in queue!".format(self.params['host']))

        return (True, None)

    def title(self):
        return "Add MON on node {node}".format(node=self.params['host'])

