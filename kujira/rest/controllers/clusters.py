from kujira.blueprints import cluster_bp
from kujira.rest.lib.request_methods import send_get


@cluster_bp.route("")
def cluster():
    return send_get('cluster')

