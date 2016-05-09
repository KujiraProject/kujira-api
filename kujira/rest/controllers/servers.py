from kujira.blueprints import SERVER_BP
from kujira.rest.lib.request_methods import send_get_alt


@SERVER_BP.route("/<fsid>")
def all_servers(fsid):
    return send_get_alt('cluster/' + fsid + '/server')


@SERVER_BP.route("/<fsid>/<fqdn>")
def server(fsid, fqdn):
    return send_get_alt('cluster/' + fsid + '/server/' + fqdn)


@SERVER_BP.route("/<fqdn>")
def server_fqdn(fqdn):
    return send_get_alt('server/' + fqdn)


def servers_parse(json_dict):
    try:
        new_dict = json_dict[0]
    except Exception as e:
        new_dict = json_dict
        print e.message
    data = {'data': {}}
    attributes = {}
    withattr = True
    if new_dict:
        for key, value in new_dict.iteritems():
            if str(key) == 'type':
                withattr = False
                data['data']['type'] = str(value)
            elif str(key) == 'id':
                data['data']['id'] = str(value)
                withattr = False
            elif str(key) == 'services':
                service = {}
                for index in range(len(value)):
                    service['service ' + str(index)] = {}
                    service['service ' + str(index)] = servers_parse(value[index])
                data['data']['relationships'] = service
            else:
                attributes[key] = value
        if withattr:
            data['data']['attributes'] = attributes
            data['data']['type'] = 'server'
    return data