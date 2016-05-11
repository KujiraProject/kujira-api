"""API Controller for server objects.
Methods mapped:
- api/v2/clusters/fsid/server
- api/v2/clusters/fsid/server/fqdn
- api/v2/server/fqdn"""

import logging

from kujira.blueprints import SERVER_BP
from kujira.rest.lib.request_methods import send_get
from kujira.rest.lib.parsing_methods import parse_and_return


@SERVER_BP.route("/<fsid>")
def all_servers(fsid):
    response = send_get('cluster/' + fsid + '/server')
    if response.status_code != 422:
        response = parse_and_return(servers_parse, response)
    return response


@SERVER_BP.route("/<fsid>/<fqdn>")
def server(fsid, fqdn):
    response = send_get('cluster/' + fsid + '/server/' + fqdn)
    if response.status_code != 422:
        response = parse_and_return(servers_parse, response)
    return response


@SERVER_BP.route("/<fqdn>")
def server_fqdn(fqdn):
    response = send_get('/server/' + fqdn)
    if response.status_code != 422:
        response = parse_and_return(servers_parse, response)
    return response


def servers_parse(json_dict):
    print json_dict
    try:
        new_dict = json_dict[0]
    except Exception as e:
        new_dict = json_dict
        logging.warning(e.message)
    root = {'data': []}
    attributes = {}
    if new_dict:
        data = {'type': 'servers'}
        for key, value in new_dict.iteritems():
            key = key.replace('_', '-')
            if str(key) == 'fqdn':
                data['id'] = str(value)
                attributes[key] = value
            elif str(key) == 'type':
                data['type'] = str(value) + 's'
            elif str(key) == 'id':
                data['id'] = str(value)
            elif str(key) == 'services':
                relationships = []
                for index in range(len(value)):
                    if isinstance(value[index], dict):
                        relationships.append(servers_parse(value[index]))
                    else:
                        relationships.append(value[index])
                data['relationships'] = relationships
            else:
                attributes[key] = value
        data['attributes'] = attributes
    root['data'].append(data)
    return root