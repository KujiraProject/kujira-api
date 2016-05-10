"""API Controller for monitor objects.
Methods mapped:
- api/v2/clusters/fsid/mon
- api/v2/clusters/fsid/mon/name
- api/v2/clusters/fsid/mon/name/status"""

import logging

from kujira.blueprints import MON_BP
from kujira.rest.lib.request_methods import send_get
from kujira.rest.lib.parsing_methods import parse_and_return


@MON_BP.route("/<fsid>")
def all_monitors(fsid):
    response = send_get('cluster/' + fsid + '/mon')
    return parse_and_return(mons_parse, response)


@MON_BP.route("/<fsid>/<name>")
def monitor(fsid, name):
    response = send_get('cluster/' + fsid + '/mon/' + name)
    return parse_and_return(mons_parse, response)


def mons_parse(json_dict):
    try:
        new_dict = json_dict[0]
    except Exception as e:
        new_dict = json_dict
        logging.warning(e.message)
    data = {'data': {'type' : 'mon'}}
    attributes = {}
    if new_dict:
        for key, value in new_dict.iteritems():
            if str(key) == 'name':
                data['data']['id'] = str(value)
                attributes[key] = value
            else:
                attributes[key] = value
        data['data']['attributes'] = attributes
    return data