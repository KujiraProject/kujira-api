from flask import Blueprint

osd_bp = Blueprint('osd', __name__, url_prefix="/osds")
pool_bp = Blueprint('pool', __name__, url_prefix="/pools")
server_bp = Blueprint('server', __name__, url_prefix="/servers")
mon_bp = Blueprint('mon', __name__, url_prefix="/mons")
cluster_bp = Blueprint('cluster', __name__, url_prefix="/clusters")
