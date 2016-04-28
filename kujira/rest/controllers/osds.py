from kujira.blueprints import osd_bp
from kujira.rest.lib.request_methods import send_get


@osd_bp.route("/<fsid>")
def all_osds(fsid):
    return send_get('cluster/' + fsid + '/osd')


@osd_bp.route("/<fsid>/<int:osd_id>")
def osd(fsid, osd_id):
    return send_get('cluster/' + fsid + '/osd/' + str(osd_id))
