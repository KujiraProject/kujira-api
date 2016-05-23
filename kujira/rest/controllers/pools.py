"""API Controller for pool objects.
Methods mapped:
- api/v2/clusters/fsid/pool
- api/v2/clusters/fsid/pool/pool_id"""

from flask import Response

from kujira.blueprints import POOL_BP
from kujira.rest.lib.parsing_methods import parse_and_return, parse_cluster_pool
from kujira.rest.lib.request_methods import send_get


@POOL_BP.route("/<fsid>")
def all_pools(fsid):
    """Request for getting all pools"""
    response = send_get('cluster/' + fsid + '/pool')
    if not isinstance(response, Response):
        response = parse_and_return(parse_pools, response)
    return response


@POOL_BP.route("/<fsid>/<int:pool_id>")
def pool(fsid, pool_id):
    """Request for pools monitor of particular id"""
    response = send_get('cluster/' + fsid + '/pool/' + str(pool_id))
    if not isinstance(response, Response):
        response = parse_and_return(parse_pools, response)
    return response


def parse_pools(pools):
    """Function which parses pools list or dict into JSON API format"""
    result = {
        'data': []
    }
    if isinstance(pools, list):
        for pool_dict in pools:
            current_pool = parse_cluster_pool('pools', pool_dict)
    else:
        current_pool = parse_cluster_pool('pools', pools)
    result['data'].append(current_pool)
    return result