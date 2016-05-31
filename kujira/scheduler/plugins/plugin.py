# -*- coding: utf-8 -*-

class Plugin(object):
    
    def __init__(self, **params):
        self.params = params

    def is_valid(self):
        raise NotImplementedError("Plugin.is_valid must be implemented!")

    def can_run(self):
        raise NotImplementedError("Plugin.can_run must be implemented!")
