"""Library which contains methods representing HTTP Requests via CalamariClient"""
import logging

from requests import ConnectionError
from flask import Response

import config
from kujira.rest.lib.calamari_client import CalamariClient
from kujira.rest.lib.parsing_methods import create_error_422, parse_and_return


def send_get(url):
    """Method wraps CalamariClient object and calls GET method to get Response"""
    try:
        client = CalamariClient(api_url=config.CALAMARI_API_URL, username=config.CALAMARI_API_USER,
                                password=config.CALAMARI_API_PWD, timeout=config.CALAMARI_API_TIMEOUT)
        response = client.get(url)
    except ConnectionError as err:
        response = create_error_422(url, str(err))
        logging.warning(str(err))
    return response


def check_fsid(before_fsid, after_fsid, parse_method):
    """Method which will check and try to get fsid before sending a get request"""
    if config.CEPH_FSID is None:
        get_fsid()
    else:
        if config.CEPH_FSID is not None:
            url = before_fsid + config.CEPH_FSID + after_fsid
            response = send_get(url)
            if not isinstance(response, Response):
                response = parse_and_return(parse_method, response)
            return response
        else:
            return []


def get_fsid():
    """Request getting ceph fsid"""
    response = send_get("/cluster")
    response_dict = response[0]
    if "id" in response_dict:
        config.CEPH_FSID = response_dict["id"]
    else:
        config.CEPH_FSID = None
