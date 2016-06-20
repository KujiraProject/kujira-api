"""API Controller for server objects.
Methods mapped:
- api/v2/clusters/fsid/server
- api/v2/clusters/fsid/server/fqdn
- api/v2/server/fqdn"""

import json
import re
import subprocess

from flask import Response

from kujira.blueprints import SERVER_BP
from kujira.rest.lib.parsing_methods import parse_and_return
from kujira.rest.lib.request_methods import send_get


@SERVER_BP.route("")
def all_servers():
    """Request for getting all servers"""
    response = send_get('/server')
    if not isinstance(response, Response):
        response = parse_and_return(parse_servers, response)
    return response


@SERVER_BP.route("/raw")
def all_servers_raw():
    response = send_get('/server')
    json_list = []
    for json_obj in response:
        hostname = json_obj['hostname']
        if hostname != 'mng':
            server = {'hostname': hostname}
            disks = []
            available = 0
            size = 0
            process = subprocess.Popen("sudo salt '"+hostname+"' osd_disk.get_disk_osd_mapping",
                                                      shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            bash_output = process.communicate()
            bash_output = bash_output[0]
            if bash_output.startswith(hostname):
                part_dict = json.loads(re.sub(''+hostname+':\n', '', bash_output))
            for elem in part_dict:
                elem_str = str(elem)
                temp = re.search(r'\d+$', elem_str)
                if elem_str.startswith('/dev/') and temp is None:
                    disks.append({elem_str: part_dict[elem]})
                    if 'available' in part_dict[elem]:
                        available += int(part_dict[elem]['available'][:-1])
                    if 'size' in part_dict[elem]:
                        size += int(part_dict[elem]['size'][:-1])
            server['size'] = str(size)+'M'
            server['disks_count'] = str(disks.__len__())
            server['available'] = str(available)+'M'
            server['disks'] = disks
            json_list.append(server)
    return json.dumps(json_list, indent=2)


@SERVER_BP.route("/<fsid>")
def all_servers_cluster(fsid):
    """Request for getting all servers in a cluster"""
    response = send_get('cluster/' + fsid + '/server')
    if not isinstance(response, Response):
        response = parse_and_return(parse_servers, response)
    return response


@SERVER_BP.route("/<fsid>/<fqdn>")
def server(fsid, fqdn):
    """Request for getting server of particular fqdn and fsid"""
    response = send_get('cluster/' + fsid + '/server/' + fqdn)
    if not isinstance(response, Response):
        response = parse_and_return(parse_servers, response)
    return response


@SERVER_BP.route("/<fqdn>")
def server_fqdn(fqdn):
    """Request for getting server of particular fqdn"""
    response = send_get('/server/' + fqdn)
    if response.status_code != 422:
        response = parse_and_return(parse_servers, response)
    return response


def parse_servers(servers):
    """Function which parses servers list or dict into JSON API format"""
    result = {
        'data': []
    }
    if isinstance(servers, list):
        for server_dict in servers:
            current_server = parse_server(server_dict)
            result['data'].append(current_server)
    else:
        current_server = parse_server(servers)
        result['data'].append(current_server)
    return result


def parse_server(server_dict):
    """Function which restructures server's dict entries into appropriate categories"""
    result = {
        'type': 'servers'
    }
    attributes = {}
    for key, value in server_dict.iteritems():
        key = key.replace('_', '-')
        if str(key) == 'fqdn':
            result['id'] = str(value)
            attributes[key] = value
        elif str(key) == 'type':
            result['type'] = str(value) + 's'
        elif str(key) == 'id':
            result['id'] = str(value)
        elif str(key) == 'services':
            relationships = []
            for index in range(len(value)):
                if isinstance(value[index], dict):
                    new_relative = {'data': parse_server(value[index])}
                    relationships.append(new_relative)
                else:
                    relationships.append(value[index])
            result['relationships'] = relationships
        else:
            attributes[key] = value
    result['attributes'] = attributes
    return result
