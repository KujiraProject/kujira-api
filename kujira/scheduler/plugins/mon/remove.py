# -*- coding: utf-8 -*-
"""This plugin describes task of removing a monitor from cluster"""

from kujira.scheduler.plugins.plugin import Plugin

class Remove(Plugin):
    """Remove a monitor from cluster"""
    salt_module_name = 'kujira.mon.remove'

    def is_valid(self):
        if 'host' not in self.params:
            return (False, "'host' param is required!")

        return (True, None)

    def can_run(self):
        if not self.check_if_exists():
            return (False, "Removing monitor from {0} is already in queue!" \
            .format(self.params['host']))

        return (True, None)

    def title(self):
        return "Remove MON from node {node}".format(node=self.params['host'])
