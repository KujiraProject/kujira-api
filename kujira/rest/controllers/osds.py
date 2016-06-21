"""API Controller for osd objects.
Methods mapped:
- api/v2/clusters/fsid/osd
- api/v2/clusters/fsid/osd/osd_id"""

from kujira.blueprints import OSD_BP
from kujira.rest.lib.request_methods import check_fsid


@OSD_BP.route("")
def all_osds():
    """Request for getting all osds"""
    response = check_fsid('cluster/', '/osd', parse_osds)
    return response


@OSD_BP.route("/<osd_id>")
def osd(osd_id):
    """Request for getting monitor of particular id"""
    response = check_fsid('cluster/', '/osd/'+osd_id, parse_osds)
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
            for index in range(len(value)):
                if isinstance(value[index], dict):
                    lst.append(parse_osd(value[index]))
                else:
                    lst.append(value[index])
            attributes[key] = lst
        else:
            attributes[key] = value
    result['attributes'] = attributes
    return result
