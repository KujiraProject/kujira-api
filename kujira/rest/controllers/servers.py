from kujira.blueprints import SERVER_BP
from kujira.rest.lib.request_methods import send_get
from kujira.rest.lib.parsing_methods import parse_and_return


"""API Controller for server objects.
Methods mapped:
- api/v2/clusters/fsid/server
- api/v2/clusters/fsid/server/fqdn
- api/v2/server/fqdn
"""


@SERVER_BP.route("/<fsid>")
def all_servers(fsid):
    response = send_get('cluster/' + fsid + '/server')
    return parse_and_return(servers_parse_alt, response)


@SERVER_BP.route("/<fsid>/<fqdn>")
def server(fsid, fqdn):
    response = send_get('cluster/' + fsid + '/server/' + fqdn)
    return parse_and_return(servers_parse_alt, response)


@SERVER_BP.route("/<fqdn>")
def server_fqdn(fqdn):
    response = send_get('/server/' + fqdn)
    return parse_and_return(servers_parse_alt, response)


def servers_parse_alt(json_dict):
    try:
        new_dict = json_dict[0]
    except Exception as e:
        new_dict = json_dict
    data = {'data': {'type' : 'server'}}
    attributes = {}
    if new_dict:
        for key, value in new_dict.iteritems():
            if str(key) == 'fqdn':
                data['data']['id'] = str(value)
                attributes[key] = value
            elif str(key) == 'type':
                data['data']['type'] = str(value)
            elif str(key) == 'id':
                data['data']['id'] = str(value)
            elif str(key) == 'services':
                relationships = []
                for index in range(len(value)):
                    if isinstance(value[index], dict):
                        relationships.append(servers_parse_alt(value[index]))
                    else:
                        relationships.append(value[index])
                data['data']['relationships'] = relationships
            else:
                attributes[key] = value
        data['data']['attributes'] = attributes
    return data