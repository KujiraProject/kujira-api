from flask import Blueprint

cluster_bp = Blueprint('clusters', __name__, url_prefix="/clusters")
osd_bp = Blueprint('osds', __name__, url_prefix="/osds")
server_bp = Blueprint('servers', __name__, url_prefix="/servers")
pool_bp = Blueprint('pools', __name__, url_prefix="/pools")
mon_bp = Blueprint('mons', __name__, url_prefix="/mons")
