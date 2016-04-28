from kujira.blueprints import mon_bp
from kujira.rest.lib.request_methods import send_get


@mon_bp.route("/<fsid>")
def all_monitors(fsid):
    return send_get('cluster/' + fsid + '/mon')


@mon_bp.route("/<fsid>/<name>")
def monitor(fsid, name):
    return send_get('cluster/' + fsid + '/mon/' + name)


@mon_bp.route("/<fsid>/<name>/status")
def monitor_status(fsid, name):
    return send_get('cluster/' + fsid + '/mon/' + name + '/status')
