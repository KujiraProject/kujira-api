import os
pwd = os.getcwd()
print(pwd)
number = (len(pwd)-12)
pwd = pwd[:number]+"kujira/store/"
print(pwd)
import sys
sys.path.append(pwd)
import tasks
    
connection = tasks.Mongodb()
connection.connect("mydb2", "tasks2", "oldTasks2")
connection.insert_task({
                            "date":"",
                            "task_state":"",
                            "parallel": False,
                            "title": "Add node5 to Ceph",
                            "subtask":[{"host": "node2",   "module": 'test.sleep', "arg": "5",   "jid": "", "status": ""},
                                {"host": "mng",   "module": 'test.sleeprt2', "arg": "20",   "jid": "", "status": ""},
                                {"host": "mng",   "module": 'test.sleep', "arg": "5",   "jid": "", "status": ""}
                            ],
                        })
                        
connection.insert_task({
                            "task_state":"",
                            "date":"",
                            "parallel": True,
                            "title": "Add node5 to Ceph",
                            "subtask":[{"host": "mng",   "module": 'test.sleep', "arg": "23",   "jid": "", "status": ""},
                                {"host": "mng",   "module": 'test.sleep', "arg": "23",   "jid": "", "status": ""},
                                {"host": "mng",   "module": 'test.sleep', "arg": "23",   "jid": "", "status": ""}
                            ]
                        })
                        
 