"""API Controller for pool objects.
Methods mapped:
- api/v2/clusters/fsid/pool
- api/v2/clusters/fsid/pool/pool_id"""

import logging

from kujira.blueprints import POOL_BP
from kujira.rest.lib.request_methods import send_get
from kujira.rest.lib.parsing_methods import parse_and_return


@POOL_BP.route("/<fsid>")
def all_pools(fsid):
    """Request for getting all pools"""
    response = send_get('cluster/' + fsid + '/pool')
    if response.status_code != 422:
        response = parse_and_return(pools_parse, response)
    return response


@POOL_BP.route("/<fsid>/<int:pool_id>")
def pool(fsid, pool_id):
    """Request for pools monitor of particular id"""
    response = send_get('cluster/' + fsid + '/pool/' + str(pool_id))
    if response.status_code != 422:
        response = parse_and_return(pools_parse, response)
    return response


def pools_parse(json_dict):
    """Pools parser to JSON API format"""
    try:
        new_dict = json_dict[0]
    except KeyError as err:
        new_dict = json_dict
        logging.warning(str(err))
    root = {'data': []}
    attributes = {}
    if new_dict:
        data = {'type': 'pools'}
        for key, value in new_dict.iteritems():
            key = key.replace('_', '-')
            if str(key) == 'id':
                data['id'] = str(value)
                attributes[key] = value
            else:
                attributes[key] = value
        data['attributes'] = attributes
    root['data'].append(data)
    return root

