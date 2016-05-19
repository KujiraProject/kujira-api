"""API Controller for monitor objects.
Methods mapped:
- api/v2/clusters/fsid/mon
- api/v2/clusters/fsid/mon/name
- api/v2/clusters/fsid/mon/name/status"""

from flask import Response

from kujira.blueprints import MON_BP
from kujira.rest.lib.parsing_methods import parse_and_return
from kujira.rest.lib.request_methods import send_get


@MON_BP.route("/<fsid>")
def all_monitors(fsid):
    """Request for getting all monitors"""
    response = send_get('cluster/' + fsid + '/mon')
    if not isinstance(response, Response):
        response = parse_and_return(parse_mons, response)
    return response


@MON_BP.route("/<fsid>/<name>")
def monitor(fsid, name):
    """Request for getting monitor of particular name"""
    response = send_get('cluster/' + fsid + '/mon/' + name)
    if not isinstance(parse_mons, Response):
        response = parse_and_return(parse_mons, response)
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
