from kujira.blueprints import osd_bp
from kujira.rest.lib.request_methods import send_get, send_get_alt
from kujira.rest.lib.parsing_methods import parse_and_return


@osd_bp.route("/<fsid>")
def all_osds(fsid):
    response = send_get_alt('cluster/' + fsid + '/osd')
    return parse_and_return(osds_parse, response)


@osd_bp.route("/<fsid>/<osd_id>")
def osd(fsid, osd_id):
    response = send_get_alt('cluster/' + fsid + '/osd/' + osd_id)
    return parse_and_return(osds_parse, response)


def osds_parse(json_dict):
    try:
        new_dict = json_dict[0]
    except Exception as e:
        new_dict = json_dict
        print e.message
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