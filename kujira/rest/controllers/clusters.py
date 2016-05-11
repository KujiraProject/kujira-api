"""API Controller for cluster objects.
Methods mapped:
- api/v2/clusters"""

import logging

from kujira.blueprints import CLUSTER_BP
from kujira.rest.lib.request_methods import send_get
from kujira.rest.lib.parsing_methods import parse_and_return


@CLUSTER_BP.route("")
def cluster():
    response = send_get('cluster')
    if response.status_code != 422:
        response = parse_and_return(clusters_parse, response)
    return response


def clusters_parse(json_dict):
    try:
        new_dict = json_dict[0]
    except Exception as e:
        new_dict = json_dict
        logging.warning(e.message)
    root = {'data': []}
    attributes = {}
    if new_dict:
        data = {'type': 'clusters'}
        for key, value in new_dict.iteritems():
            key = key.replace('_', '-')
            if str(key) == 'name':
                data['id'] = str(value)
                attributes[key] = value
            else:
                attributes[key] = value
        data['attributes'] = attributes
    root['data'].append(data)
    return root