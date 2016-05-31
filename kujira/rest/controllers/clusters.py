"""API Controller for cluster objects.
Methods mapped:
- api/v2/clusters"""

from flask import Response

from kujira.blueprints import CLUSTER_BP
from kujira.rest.lib.parsing_methods import parse_and_return
from kujira.rest.lib.request_methods import send_get


@CLUSTER_BP.route("")
def get_cluster():
    """Request for getting all clusters"""
    response = send_get('cluster')
    if isinstance(response, Response):
        return response

    for cluster_dict in response:
        fsid = cluster_dict["id"]
        response = send_get('cluster/{fsid}/sync_object/health'.format(fsid=fsid))
        response["fsid"] = fsid
        response["name"] = cluster_dict["name"]
        response["update-time"] = cluster_dict["update_time"]
        return parse_and_return(parse_cluster, response)


def parse_cluster(cluster):
    """Function which parses clusters list or dict into JSON API format"""
    return {
        "data": {
            "type": "clusters",
            "id": cluster["fsid"],
            "attributes": {
                "id": cluster["fsid"],
                "name": cluster["name"],
                "epoch": cluster["timechecks"]["epoch"],
                "health": cluster["overall_status"]
            }
        }
    }
