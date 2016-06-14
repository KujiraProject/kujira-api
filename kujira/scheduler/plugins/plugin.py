# -*- coding: utf-8 -*-
"""Abstaction for scheduler's plugins (tasks)"""

from datetime import datetime

class Plugin(object):
    """Plugin class is an abstraction for task"""
    salt_module_name = None

    def __init__(self, **params):
        self.create_date = datetime.now()
        self.params = params
        self.database = None

        if 'parallel' not in self.params:
            self.params['parallel'] = True

    def set_db_instance(self, database):
        """Set instance of mongo database connection

        :param database: mongo db connection"""
        self.database = database

    def is_valid(self):
        """Check if task is valid

        Check if task has all params and if they are valid"""
        raise NotImplementedError("Plugin.is_valid must be implemented!")

    def can_run(self):
        """Check if task can be run

        It should return False if task is duplicate of another one"""
        raise NotImplementedError("Plugin.can_run must be implemented!")

    def check_if_exists(self):
        """Check if task exists in database"""
        tasks = self.database.get_all_tasks()

        for task in tasks:
            for existing_subtask in task['subtasks']:
                for current_subtask in self.subtasks():
                    if existing_subtask == current_subtask:
                        return False

        return True

    def subtasks(self):
        """Get subtasks

        This function returns subtasks which must be executed
        to complete this task"""
        return [
            {
                'host': self.params['host'],
                'module': self.salt_module_name,
                'arg': None,
                'jid': None,
                'status': None,
            },
        ]

    def title(self):
        """Human friendly name of task"""
        raise NotImplementedError("Plugin.title must be implemented!")

    def data(self):
        """Get dictionary containing all information about task"""
        return {
            'title': self.title(),
            'subtasks': self.subtasks(),
            'parallel': self.params['parallel']}
