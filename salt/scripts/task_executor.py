# -*- coding: utf-8 -*-
# Import python libs
from __future__ import absolute_import
import time
import logging

# Import salt libs
import salt.utils.event
import salt.client

logger = logging.getLogger('task_execute')
handler = logging.FileHandler('/var/tmp/task_execute.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler) 

try:
	import TaskStorage
except ImportError:
	logger.error('No connection with mongoDB')
	class TaskStorage(object):
		def __init__(self):
			self.listTask=[{"host":"mng","module":'cmd.run', "arg":"date","jid" : "", "status":""},{"host":"node1","module":'test.sleep', 
			"arg":"1","jid" : "", "status":""},{"host":"mng","module":'cmd.run', "arg":"ls","jid" : "", "status":""}]
		def get_task(self):
			return self.listTask[0]
		def update_task(self, task):
			self.listTask[0] = task
			if(self.listTask[0]['status'] != ''):
				del self.listTask[0]		
	
	
def execute(task):
	"""Function which execute tasks"""
	client_salt = salt.client.LocalClient()
	job_id = client_salt.cmd_async(task["host"], task["module"], [task["arg"]])
	return job_id
	
	
def wait_for_finish(task):
	"""Function which wait for task status"""
	client_salt = salt.client.LocalClient()
	while True:	
		try:
			ret_temp = client_salt.get_cli_returns(task['jid'], task['host'])
			ret=[x for x in ret_temp]
			if not ret:
				logger.info('Task still running jid: %s' task['jid'])
				time.sleep(1)
				continue
			logger.info('Task is finished jid: %s' task['jid'])
			if(ret[0]['mng']['ret'] == True):
				return True
			else:
				return False
		except KeyError as ex:
			logger.error('Catch exception KeyError %s', ex)
			continue
	
	
def start():
	"""Main function where take and execute tasks """
	connection=TaskStorage()
	while True:
		task=connection.get_task()
		
		if not task:
			time.sleep(60) # sleep asking for next task
			continue
			
		jid=execute(task)
		task['jid']= jid
		connection.update_task(task)
		if jid==0:
			task['status'] = 'failure'
			connection.update_task(task)
			break;
		if(wait_for_finish(task)):
			task['status'] = 'finished'
		else:
			task['status'] = 'failure'	
		connection.update_task(task)

start()