"""File with Blueprints registration"""

from flask import Blueprint

OSD_BP = Blueprint('osd', __name__, url_prefix="/kujira/api/v1/osds")
POOL_BP = Blueprint('pool', __name__, url_prefix="/kujira/api/v1/pools")
SERVER_BP = Blueprint('server', __name__, url_prefix="/kujira/api/v1/servers")
MON_BP = Blueprint('mon', __name__, url_prefix="/kujira/api/v1/mons")
CLUSTER_BP = Blueprint('cluster', __name__, url_prefix="/kujira/api/v1/clusters")
