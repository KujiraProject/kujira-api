# Helpers
import argparse

from kujira.rest.lib.authenticated_http_client import AuthenticatedHttpClient

CALAMARI_API_URL = "http://localhost/api/v2/"


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
