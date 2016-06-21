"""File with Blueprints registration"""

from flask import Blueprint

OSD_BP = Blueprint('osd', __name__, url_prefix="/kujira/api/v1/calamari/osds")
POOL_BP = Blueprint('pool', __name__, url_prefix="/kujira/api/v1/calamari/pools")
SERVER_BP = Blueprint('server', __name__, url_prefix="/kujira/api/v1/calamari/servers")
MON_BP = Blueprint('mon', __name__, url_prefix="/kujira/api/v1/calamari/mons")
CLUSTER_BP = Blueprint('cluster', __name__, url_prefix="/kujira/api/v1/calamari/clusters")
DISK_BP = Blueprint('disk', __name__, url_prefix="/kujira/api/v1/disks")
TASKS_BP = Blueprint('tasks', __name__, url_prefix="/kujira/api/v1/tasks")