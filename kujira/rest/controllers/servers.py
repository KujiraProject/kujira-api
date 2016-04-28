from kujira.blueprints import server_bp
from kujira.rest.lib.request_methods import send_get


@server_bp.route("/<fsid>")
def all_servers(fsid):
    return send_get('cluster/' + fsid + '/server')


@server_bp.route("/<fsid>/<fqdn>")
def server(fsid, fqdn):
    return send_get('cluster/' + fsid + '/server/' + fqdn)


@server_bp.route("/<fqdn>")
def server_fqdn(fqdn):
    return send_get('server/' + fqdn)
