from kujira.blueprints import mon_bp
from kujira.rest.lib.request_methods import send_get_alt
from kujira.rest.lib.parsing_methods import parse_and_return


@mon_bp.route("/<fsid>")
def all_monitors(fsid):
    response = send_get_alt('cluster/' + fsid + '/mon')
    return parse_and_return(mons_parse, response)


@mon_bp.route("/<fsid>/<name>")
def monitor(fsid, name):
    response = send_get_alt('cluster/' + fsid + '/mon/' + name)
    return parse_and_return(mons_parse, response)


@mon_bp.route("/<fsid>/<name>/status")
def monitor_status(fsid, name):
    response = send_get_alt('cluster/' + fsid + '/mon/' + name + 'status')
    return parse_and_return(mons_parse, response)


def mons_parse(json_dict):
    try:
        new_dict = json_dict[0]
    except Exception as e:
        new_dict = json_dict
        print e.message
    data = {'data': {'type' : 'mon'}}
    attributes = {}
    if new_dict:
        for key, value in new_dict.iteritems():
            if str(key) == 'name':
                data['data']['id'] = str(value)
                attributes[key] = value
            else:
                attributes[key] = value
        data['data']['attributes'] = attributes
    return data