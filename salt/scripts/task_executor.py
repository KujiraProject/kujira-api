# -*- coding: utf-8 -*-
# Import python libs
from __future__ import absolute_import
import time
import logging
# Import salt libs
import salt.utils.event
import salt.client
import salt.config

LOG = logging.getLogger('executor')
HANDLER = logging.FileHandler('/var/log/executor.log')
FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
HANDLER.setFormatter(FORMATTER)
LOG.addHandler(HANDLER)

FETCH_TIME = 5 # interval to fetch next task
CHECK_TIME = 2 # interval to check if task finished

try:
    import TaskStorage
except ImportError:
    LOG.error('No connection with mongoDB, using testing tasks...')

    class TaskStorage(object):
        def __init__(self):
            self.nt = 0
            self.tasks = [[{"host": "mng",   "module": 'test.sleep', "arg": "3",   "jid": "", "status": ""}],
                          [{}],  # It means that there isnt any task at the moment
                          [{}],  # It means that there isnt any task at the moment
                          [{"host": "node1",   "module": 'cmd.run',    "arg": "pepe", "jid": "", "status": ""},
                          {"host": "node1", "module": 'test.sleep', "arg": "1",    "jid": "", "status": ""}],
                          [{}],  # It means that there isnt any task at the moment
                          [{"host": "mng",   "module": 'cmd.run',    "arg": "ls",   "jid": "", "status": ""}]]

        def get_task(self):
            if self.nt >= len(self.tasks):
                self.nt = 0

            task = self.tasks[self.nt]
            self.nt = self.nt + 1
            return task

        def update(self, task):
            return

class get_task(object):
    """Class connect to database and take list with tasks to execute and return task"""
    def __init__(self):
        self.tasks = TaskStorage().get_task()
        self.connection = TaskStorage()
        
    def get_task(self):
        """Function which return task to execute"""
        if len(self.tasks)==0:
            self.tasks = self.connection.get_task()
        if len(self.tasks)!=0:
            return self.tasks.pop()
        return

def execute(task):
    """Function which execute tasks"""
    LOG.info("Executing task: %s", task)
    client_salt = salt.client.LocalClient()
    job_id = client_salt.cmd_async(task["host"], task["module"], [task["arg"]])
    return job_id

def wait_for_finish(task):
    """Function which wait for task status"""
    client_salt = salt.client.LocalClient()
    while True:
        try:
            ret_temp = client_salt.get_cli_returns(task['jid'], task['host'])
            ret = [x for x in ret_temp]
            if ret:
                if ret[0][task['host']]['ret'] == True:
                    LOG.info('Task finished. JID: %s', task['jid'])
                    return True
                else:
                    LOG.info('Task failed. JID: %s', task['jid'])
                    return False
            else:
                LOG.info('Task still running. JID: %s', task['jid'])
            time.sleep(CHECK_TIME)
        except KeyError:
            continue # Check it

def start():
    """Main function where take and execute tasks """
    connect = get_task()
    connection = TaskStorage()
    while True:
        task = connect.get_task()
        if not task:
            LOG.debug("Waiting %d seconds to ask for next task...", FETCH_TIME)
            time.sleep(FETCH_TIME)  # sleep asking for next task
            continue
        jid = execute(task)
        task['jid'] = jid
        task['status'] = 'Executing'
        connection.update(task)
        if jid == 0:
            task['status'] = 'Error'
            connection.update(task)
            continue
        if wait_for_finish(task):
            task['status'] = 'Finished'
        else:
            task['status'] = 'Failed'
        connection.update(task)
        
start()
