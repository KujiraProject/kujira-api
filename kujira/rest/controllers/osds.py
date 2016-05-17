"""API Controller for osd objects.
Methods mapped:
- api/v2/clusters/fsid/osd
- api/v2/clusters/fsid/osd/osd_id"""

import logging

from kujira.blueprints import OSD_BP
from kujira.rest.lib.parsing_methods import parse_and_return
from kujira.rest.lib.request_methods import send_get


@OSD_BP.route("/<fsid>")
def all_osds(fsid):
    """Request for getting all osds"""
    response = send_get('cluster/' + fsid + '/osd')
    if response.status_code != 422:
        response = parse_and_return(osds_parse, response)
    return response


@OSD_BP.route("/<fsid>/<osd_id>")
def osd(fsid, osd_id):
    """Request for getting monitor of particular id"""
    response = send_get('cluster/' + fsid + '/osd/' + osd_id)
    if response.status_code != 422:
        response = parse_and_return(osds_parse, response)
    return response


def osds_parse(json_dict):
    """Osds parser to JSON API format"""
    try:
        new_dict = json_dict[0]
    except Exception as e:
        new_dict = json_dict
        logging.warning(e.message)
    root = {'data': []}
    attributes = {}
    if new_dict:
        data = {'type' : 'osds'}
        for key, value in new_dict.iteritems():
            key = key.replace('_', '-')
            if str(key) == 'id':
                data['id'] = str(value)
                attributes[key] = value
            elif isinstance(value, list):
                lst = []
                for index in range(len(value)):
                    if isinstance(value[index], dict):
                        lst.append(osds_parse(value[index]))
                    else:
                        lst.append(value[index])
                attributes[key] = lst
            else:
                attributes[key] = value
        data['attributes'] = attributes
    root['data'].append(data)
    return root