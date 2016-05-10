"""Library which contains methods representing HTTP Requests via CalamariClient"""

import logging

from config import CALAMARI_API_URL, CALAMARI_API_PWD, CALAMARI_API_USER
from kujira.rest.lib.calamari_client import CalamariClient
from kujira.rest.lib.parsing_methods import create_error_422


def send_get(url):
    try:
        client = CalamariClient(api_url=CALAMARI_API_URL, username=CALAMARI_API_USER, password=CALAMARI_API_PWD)
        response = client.get(url)
    except Exception as e:
        response = create_error_422(url, e.message)
        logging.warning(e.message)
    return response
