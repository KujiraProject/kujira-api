"""API Controller for tasks"""

from kujira.blueprints import TASKS_BP
from kujira.store.tasks import Mongodb
from kujira.rest.lib.parsing_methods import create_error_422, parse_and_return
from kujira.store.exceptions import ConnectionError

MONGO = Mongodb()
MONGO.connect("mydb", "tasks", "oldTasks")

@TASKS_BP.route("")
def all_tasks():
    """Request for all tasks"""
    tasks = []
    try:
        tasks = MONGO.get_all_tasks()
    except ConnectionError err:
        response = create_error_422("kujira.store.tasks", str(err))
            
    return parse_and_return(parse_tasks, tasks)

def parse_tasks(tasks):
    """Parse tasks"""
    result = {}
    result["data"] = []
    for task in tasks:
        result["data"].append({
            "attributes": task,
            "id": task["_id"],
            "type": "tasks"
        })
    
    return result
   