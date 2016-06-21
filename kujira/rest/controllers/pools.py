"""API Controller for pool objects.
Methods mapped:
- api/v2/clusters/fsid/pool
- api/v2/clusters/fsid/pool/pool_id"""

from kujira.blueprints import POOL_BP
from kujira.rest.lib.parsing_methods import parse_cluster_pool
from kujira.rest.lib.request_methods import check_fsid


@POOL_BP.route("")
def all_pools():
    """Request for getting all pools"""
    response = check_fsid('cluster/', '/pool', parse_pools)
    return response


@POOL_BP.route("/<pool_id>")
def pool(pool_id):
    """Request for pools monitor of particular id"""
    response = check_fsid('cluster/', '/pool/' + str(pool_id), parse_pools)
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
