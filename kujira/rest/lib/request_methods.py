"""Library which contains methods representing HTTP Requests via CalamariClient"""

import logging

from requests import ConnectionError

from config import CALAMARI_API_URL, CALAMARI_API_PWD, CALAMARI_API_USER, CALAMARI_API_TIMEOUT
from kujira.rest.lib.calamari_client import CalamariClient
from kujira.rest.lib.parsing_methods import create_error_422


def send_get(url):
    """Method wraps CalamariClient object and calls GET method to get Response"""
    try:
        client = CalamariClient(api_url=CALAMARI_API_URL, username=CALAMARI_API_USER,
                                password=CALAMARI_API_PWD, timeout=CALAMARI_API_TIMEOUT)
        response = client.get(url)
    except ConnectionError as err:
        response = create_error_422(url, str(err))
        logging.warning(str(err))
    return response
