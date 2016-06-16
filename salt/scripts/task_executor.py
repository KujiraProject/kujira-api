# -*- coding: utf-8 -*-
# Import python libs
from __future__ import absolute_import
import time
import logging
# Import salt libs
import salt.utils.event
import salt.client
import salt.config
import os

LOG = logging.getLogger('executor')
HANDLER = logging.FileHandler('/var/log/executor.log')
FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
HANDLER.setFormatter(FORMATTER)
LOG.addHandler(HANDLER)

FETCH_TIME = 10# interval to fetch next task
pwd = os.getcwd()
print(pwd)
number = (len(pwd)-12)
pwd = pwd[:number]+"kujira/store/"
print(pwd)
import sys
sys.path.append(pwd)
import tasks

def execute(subtask):
    """Function which execute tasks"""
    LOG.info("Executing subtask: %s", subtask)
    client_salt = salt.client.LocalClient()
    job_id = client_salt.cmd_async(subtask["host"], subtask["module"], [subtask["arg"]])
    return job_id

def finish(subtask):
    """Function which wait for task status"""
    client_salt = salt.client.LocalClient()
    while True:
        try:
            ret_temp = client_salt.get_cli_returns(subtask['jid'], subtask['host'])
            ret = [x for x in ret_temp]
            if ret:
                if ret[0][subtask['host']]['ret'] == True:
                    LOG.info('Subtask finished. JID: %s', subtask['jid'])
                    subtask['status'] = 'Finished'
                    return subtask
                else:
                    LOG.info('Subtask failed. JID: %s', subtask['jid'])
                    subtask['status'] = 'Failed'
                    return subtask
            else:
                LOG.info('Subtask still running. JID: %s', subtask['jid'])
                return False
        except KeyError:
            continue # Check it

def execute_parallel(connection, task):
    """Function which execute parallel task"""
    jids = []
    #Executions 
    list_subtasks=task['subtask'] #take list of subtask from task
    for i in range(0, len(list_subtasks)):
        subtask = list_subtasks[i]
        jid = execute(subtask)
        if jid == 0:
            list_subtasks[i]['status'] = 'Error'
            continue
        subtask['jid'] = jid
        subtask['status'] = 'Executing'
        jids.append(jid)
        list_subtasks[i] = subtask
    task['subtask'] = list_subtasks
    connection.update_tasks(task)
    
    #Check
    while jids:
        for subtask in list_subtasks:
            if not subtask['jid'] in jids:
                continue
            if finish(subtask):
                jids.remove(subtask['jid'])
    connection.update_tasks(task)
    
def execute_sequential(connection, task):
    """Function which execute sequential task"""
    list_subtasks=task['subtask'] #take list of subtask from task
    for i in range(0, len(list_subtasks)):
        jid = execute(list_subtasks[i])
        if jid == 0:
            list_subtasks[i]['status'] = 'Error'
            connection.update_tasks(task)
            continue
        list_subtasks[i]['jid'] = jid
        list_subtasks[i]['status'] = 'Executing'
        task['subtask'] = list_subtasks
        connection.update_tasks(task)
        while True:
            tmp = finish(list_subtasks[i])
            if tmp:
                list_subtasks[i] = tmp
                break
        task['subtask']=list_subtasks
        connection.update_tasks(task)

def start():
    """Main function where take and execute tasks """
    #connect = Configurate_task()
    connection = tasks.Mongodb()
    connection.connect("mydb2", "tasks2", "oldTasks2")
                             
    while True:
        task = connection.get_task()
        if not task:
            LOG.debug("Waiting %d seconds to ask for next task...", FETCH_TIME)
            time.sleep(FETCH_TIME)  # sleep asking for next task
            continue
        LOG.info("Fetching task: {0}\nParallel: {1}\nSubtask:{2}".format(task["title"],task["parallel"],task["subtask"]))
        if(task['parallel']==True):
            execute_parallel(connection,task)
        else:
            execute_sequential(connection, task)
start()
