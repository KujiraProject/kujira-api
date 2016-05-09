from kujira.blueprints import OSD_BP
from kujira.rest.lib.parsing_methods import parse_and_return
from kujira.rest.lib.request_methods import send_get


"""API Controller for osd objects.
Methods mapped:
- api/v2/clusters/fsid/osd
- api/v2/clusters/fsid/osd/osd_id
"""


@OSD_BP.route("/<fsid>")
def all_osds(fsid):
    response = send_get('cluster/' + fsid + '/osd')
    return parse_and_return(osds_parse, response)


@OSD_BP.route("/<fsid>/<osd_id>")
def osd(fsid, osd_id):
    response = send_get('cluster/' + fsid + '/osd/' + osd_id)
    return parse_and_return(osds_parse, response)


def osds_parse(json_dict):
    try:
        new_dict = json_dict[0]
    except Exception as e:
        new_dict = json_dict
    data = {'data': {'type' : 'osd'}}
    attributes = {}
    if new_dict:
        for key, value in new_dict.iteritems():
            if str(key) == 'id':
                data['data']['id'] = str(value)
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
        data['data']['attributes'] = attributes
    return data