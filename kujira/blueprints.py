from flask import Blueprint

server_bp = Blueprint('server', __name__, url_prefix="/servers")
mon_bp = Blueprint('mon', __name__, url_prefix="/mons")
cluster_bp = Blueprint('cluster', __name__, url_prefix="/clusters")
