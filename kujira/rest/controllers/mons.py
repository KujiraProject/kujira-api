"""API Controller for monitor objects.
Methods mapped:
- api/v2/clusters/fsid/mon
- api/v2/clusters/fsid/mon/name
- api/v2/clusters/fsid/mon/name/status"""

from kujira.blueprints import MON_BP
from kujira.rest.lib.request_methods import check_fsid


@MON_BP.route("")
def all_monitors():
    """Request for getting all monitors"""
    response = check_fsid('cluster/', '/mon', parse_mons)
    return response


@MON_BP.route("/<name>")
def monitor(name):
    """Request for getting monitor of particular name"""
    response = check_fsid('cluster/', '/mon/'+name, parse_mons)
    return response


def parse_mons(mons):
    """Function which parses mons list or dict into JSON API format"""
    result = {
        'data': []
    }
    if isinstance(mons, list):
        for mon_dict in mons:
            current_mon = parse_mon(mon_dict)
    else:
        current_mon = parse_mon(mons)
    result['data'].append(current_mon)
    return result


def parse_mon(mon_dict):
    """Function which restructures mon's dict entries into appropriate categories"""
    result = {
        'type': 'mons'
    }
    attributes = {}
    for key, value in mon_dict.iteritems():
        key = key.replace('_', '-')
        if str(key) == 'name':
            result['id'] = str(value)
        attributes[str(key)] = value
    result['attributes'] = attributes
    return result
