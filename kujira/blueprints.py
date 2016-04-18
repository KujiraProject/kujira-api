from flask import Blueprint

osd_bp = Blueprint('osd', __name__, url_prefix="/osd")
server_bp = Blueprint('server', __name__, url_prefix="/server")
pool_bp = Blueprint('pool', __name__, url_prefix="/pool")
crush_bp = Blueprint('crush', __name__, url_prefix="/crush")
mon_bp = Blueprint('mon', __name__, url_prefix="/mon")
