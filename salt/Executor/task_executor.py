# -*- coding: utf-8 -*-
# Import python libs
from __future__ import absolute_import
import json
import time
import logging
import json
import Queue

# Import salt libs
import salt.utils.event
import salt.client
import salt.config

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
			self.listTask=[{"host":"mng","module":'cmd.run', "arg":"date","jid" : "", "status":""},{"host":"node1","module":'test.sleep', "arg":"1","jid" : "", "status":""},{"host":"mng","module":'cmd.run', "arg":"ls","jid" : "", "status":""}]
		def get_task(self, a):
			return self.listTask[0]
		def update(self, task):
			self.listTask[0] = task
			if(self.listTask[0]['status'] != ''):
				del self.listTask[0]		
	
def execute(task):
	"""Function which execute tasks"""
	client_salt = salt.client.LocalClient()
	job_id = client_salt.cmd_async(task["host"], task["module"], [task["arg"]])
	return job_id
	
def check(task):
	client_salt = salt.client.LocalClient()
	while True:	
		try:
			ret_temp = client_salt.get_cli_returns(task['jid'], task['host'])
			ret=[x for x in ret_temp]
			if ret:
				logger.info('Task is finished jid: %s' % task['jid'])
				if(ret[0]['mng']['ret'] == True):
					return True
				else:
					return False
			else:
				logger.info('Task still running jid: %s' % task['jid'])
			time.sleep(2)
		except KeyError as ex:
			logger.error('Catch exception KeyError %s' % ex)
			continue
		except:
			logger.error('Catch unexcepted error')
			continue
	
	
def start():
	connection=TaskStorage()
	while True:
		task=connection.get_task(1)
		if task:
			jid=execute(task)
			task['jid']= jid
			connection.update(task)
			if jid==0:
				task['status'] = 'failure'
				connection.update(task)
				break;
			if(check(task)):
				task['status'] = 'finished'
			else:
				task['status'] = 'failure'	
			connection.update(task)
		else:
			time.sleep(60) # sleep asking for next task

start()
