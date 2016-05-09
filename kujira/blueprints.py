from flask import Blueprint

OSD_BP = Blueprint('osd', __name__, url_prefix="/osds")
POOL_BP = Blueprint('pool', __name__, url_prefix="/pools")
SERVER_BP = Blueprint('server', __name__, url_prefix="/servers")
MON_BP = Blueprint('mon', __name__, url_prefix="/mons")
CLUSTER_BP = Blueprint('cluster', __name__, url_prefix="/clusters")
