# -*- coding: utf-8 -*-

"""A simple test engine, not intended for real use but as an example"""

# Import python libs
from __future__ import absolute_import
import json
import logging

# Import salt libs
import salt.utils.event
import salt.client
#Global variables


def functionTakeTasks():
	"""Take task from list"""
	listTasks=[{"host":"mng","cmd":"uname"},{"host":"node1","cmd":"whoami"},{"host":"mng","cmd":"ls"}]
	return listTasks

def functionDoTasks(listTasksToDo):
	"""Function which execute tasks"""
	listTasksDone=[]
	client_salt = salt.client.LocalClient()
	
	while len(listTasksToDo)!=0:
		tmp=listTasksToDo.pop();
		res = client_salt.cmd(tmp["host"], 'cmd.run_all', [tmp["cmd"]])[tmp["host"]]['retcode']
		if(res==0):
			listTasksDone.append(str(tmp["host"]+' '+tmp["cmd"])+" done\n")
		else:
			listTasksToDo.append(tmp)
	return listTasksDone
	
def start():

	listTasksDone=[]
	while True:
		listTasksToDo=functionTakeTasks()
		listTasksDone=listTasksDone+functionDoTasks(listTasksToDo)
		break	
		
start()