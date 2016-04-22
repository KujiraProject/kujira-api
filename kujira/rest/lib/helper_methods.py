# Helpers
import argparse
import json

from kujira.rest.lib.authenticated_http_client import AuthenticatedHttpClient

CALAMARI_API_URL = "http://192.168.56.1:8080/api/v2/"


def json_api_parser(response):
    json_response = json.dumps(response)
    json_dict = json.loads(json_response)
    data = {'data': {}}
    attributes = {}
    for key, value in json_dict[0].iteritems():
        if str(key) == 'type':
            data['data']['type'] = str(value)
        elif str(key) == 'id':
            data['data']['id'] = str(value)
        else:
            attributes[str(key)] = str(value)
    data['data']['attributes'] = attributes
    return data


def print_and_return(response):
    print response
    return response


def arg_parser_init(url_str):
    p = argparse.ArgumentParser()
    p.add_argument('--user', default='admin')
    p.add_argument('--pass', dest='password', default='kujira')
    p.add_argument('-u', dest='url', default=url_str)
    return p


def authenticate(arg_user, arg_pwd):
    c = AuthenticatedHttpClient(CALAMARI_API_URL, arg_user, arg_pwd)
    c.login()
    return c
