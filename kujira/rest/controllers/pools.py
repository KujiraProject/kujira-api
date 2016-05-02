from kujira.blueprints import pool_bp
from kujira.rest.lib.request_methods import send_get_alt
from kujira.rest.lib.parsing_methods import parse_and_return


@pool_bp.route("/<fsid>")
def all_pools(fsid):
    response = send_get_alt('cluster/' + fsid + '/pool')
    return parse_and_return(pools_parse, response)


@pool_bp.route("/<fsid>/<int:pool_id>")
def pool(fsid, pool_id):
    response = send_get_alt('cluster/' + fsid + '/pool/' + str(pool_id))
    return parse_and_return(pools_parse, response)


def pools_parse(json_dict):
    try:
        new_dict = json_dict[0]
    except Exception as e:
        new_dict = json_dict
        print e.message
    data = {'data': {'type' : 'pool'}}
    attributes = {}
    if new_dict:
        for key, value in new_dict.iteritems():
            if str(key) == 'id':
                data['data']['id'] = str(value)
                attributes[key] = value
            else:
                attributes[key] = value
        data['data']['attributes'] = attributes
    return data

