from kujira.blueprints import pool_bp
from kujira.rest.lib.request_methods import send_get


@pool_bp.route("/<fsid>")
def all_pools(fsid):
    return send_get('cluster/' + fsid + '/pool')


@pool_bp.route("/<fsid>/<int:pool_id>")
def pool(fsid, pool_id):
    return send_get('cluster/' + fsid + '/pool/' + str(pool_id))

