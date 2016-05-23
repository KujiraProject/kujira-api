"""API Controller for osd objects.
Methods mapped:
- api/v2/clusters/fsid/osd
- api/v2/clusters/fsid/osd/osd_id"""

from flask import Response

from kujira.blueprints import OSD_BP
from kujira.rest.lib.parsing_methods import parse_and_return
from kujira.rest.lib.request_methods import send_get


@OSD_BP.route("/<fsid>")
def all_osds(fsid):
    """Request for getting all osds"""
    response = send_get('cluster/' + fsid + '/osd')
    if not isinstance(response, Response):
        response = parse_and_return(parse_osds, response)
    return response


@OSD_BP.route("/<fsid>/<osd_id>")
def osd(fsid, osd_id):
    """Request for getting monitor of particular id"""
    response = send_get('cluster/' + fsid + '/osd/' + osd_id)
    if not isinstance(response, Response):
        response = parse_and_return(parse_osds, response)
    return response


def parse_osds(osds):
    """Function which parses osds' list or dict into JSON API format"""
    result = {
        'data': []
    }
    if isinstance(osds, list):
        for osd_dict in osds:
            current_osd = parse_osd(osd_dict)
    else:
        current_osd = parse_osd(osds)
    result['data'].append(current_osd)
    return result


def parse_osd(osd_dict):
    """Function which restructures osd's dict entries into appropriate categories"""
    result = {
        'type': 'osds'
    }
    attributes = {}
    for key, value in osd_dict.iteritems():
        key = key.replace('_', '-')
        if str(key) == 'id':
            result['id'] = str(value)
            attributes[key] = value
        elif isinstance(value, list):
            lst = []
            for index in enumerate(value):
                if isinstance(value[index], dict):
                    lst.append(parse_osd(value[index]))
                else:
                    lst.append(value[index])
            attributes[key] = lst
        else:
            attributes[key] = value
    result['attributes'] = attributes
    return result