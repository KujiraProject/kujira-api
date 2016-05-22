"""API Controller for cluster objects.
Methods mapped:
- api/v2/clusters"""

from flask import Response

from kujira.blueprints import CLUSTER_BP
from kujira.rest.lib.parsing_methods import parse_and_return, parse_cluster_pool
from kujira.rest.lib.request_methods import send_get


@CLUSTER_BP.route("")
def cluster():
    """Request for getting all clusters"""
    response = send_get('cluster')
    if not isinstance(response, Response):
        response = parse_and_return(parse_clusters, response)
    return response


def parse_clusters(clusters):
    """Function which parses clusters list or dict into JSON API format"""
    result = {
        'data': []
    }
    for cluster_dict in clusters:
        current_cluster = parse_cluster_pool('clusters', cluster_dict)
    result['data'].append(current_cluster)
    return result

