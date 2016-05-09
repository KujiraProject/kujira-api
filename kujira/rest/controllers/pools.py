import logging

from kujira.blueprints import POOL_BP
from kujira.rest.lib.request_methods import send_get
from kujira.rest.lib.parsing_methods import parse_and_return


"""API Controller for pool objects.
Methods mapped:
- api/v2/clusters/fsid/pool
- api/v2/clusters/fsid/pool/pool_id
"""


@POOL_BP.route("/<fsid>")
def all_pools(fsid):
    response = send_get('cluster/' + fsid + '/pool')
    return parse_and_return(pools_parse, response)


@POOL_BP.route("/<fsid>/<int:pool_id>")
def pool(fsid, pool_id):
    response = send_get('cluster/' + fsid + '/pool/' + str(pool_id))
    return parse_and_return(pools_parse, response)


def pools_parse(json_dict):
    try:
        new_dict = json_dict[0]
    except Exception as e:
        new_dict = json_dict
        logging.warning(e.message)
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

