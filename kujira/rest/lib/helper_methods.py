# Helpers
import argparse
import json
from flask import Response

from kujira.rest.lib.authenticated_http_client import AuthenticatedHttpClient

CALAMARI_API_URL = "http://192.168.56.1:8080/api/v2/"


def generate_response(args):
    try:
        response = authenticate(args.user, args.password).request('GET', args.url).json()
        output = json_api_parser(response)
        response = Response(json.dumps(output, indent=2), content_type='application/json')
        return response
    except Exception as e:
        response = create_error_422(args.url, e.message)
        return response


def json_api_parser(response):
    json_response = json.dumps(response)
    json_dict = json.loads(json_response)
    try:
        dict = json_dict[0]
    except Exception as e:
        dict = json_dict
    data = {'data': {}}
    attributes = {}
    for key, value in dict.iteritems():
        if str(key) == 'type':
            data['data']['type'] = str(value)
        elif str(key) == 'id':
            data['data']['id'] = str(value)
        else:
            attributes[key] = value
    data['data']['attributes'] = attributes
    return data


def create_error_422(source, message):
    errors = {'errors': [{'status':'422'}]}
    errors['errors'][0]['source'] = str(source)
    errors['errors'][0]['details'] = message
    response = Response(json.dumps(errors, indent=2), content_type="application/vnd.api+json", status=422)
    return response


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
