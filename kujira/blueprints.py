from flask import Blueprint

osd_bp = Blueprint('osd', __name__, url_prefix="/osds")
pool_bp = Blueprint('pool', __name__, url_prefix="/pools")