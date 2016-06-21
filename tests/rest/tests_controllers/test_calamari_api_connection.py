"""Calamari API connection tests"""

import unittest
from requests import ConnectionError
from config import CALAMARI_API_URL, CALAMARI_API_PWD, CALAMARI_API_USER, CALAMARI_API_TIMEOUT
from kujira.rest.lib.calamari_client import CalamariClient
from kujira.rest.lib.parsing_methods import create_error_422


class CalamariAPIConnectionTestCase(unittest.TestCase):
    """Calamari API connection test case"""

    def test_server_is_up_and_running(self):
        """ Calamari API request test:
            expected response status code - 200
        """
        constr = CalamariClient(api_url=CALAMARI_API_URL,
                                username=CALAMARI_API_USER,
                                password=CALAMARI_API_PWD,
                                timeout=CALAMARI_API_TIMEOUT)
        client = constr.authenticate()
        response = client.get(constr._api_url, timeout=constr._timeout)
        self.assertEqual(response.status_code, 200)

    def test_error_422(self):
        """ Testing request with wrong Calamari API url:
            422 error is expected
        """
        try:
            constr = CalamariClient(api_url="http://wrong_calamari_api_url/api/v2/",
                                    username=CALAMARI_API_USER,
                                    password=CALAMARI_API_PWD,
                                    timeout=CALAMARI_API_TIMEOUT)
            client = constr.authenticate()
            response = client.get(constr._api_url, timeout=constr._timeout)
        except ConnectionError as err:
            response = create_error_422(constr._api_url, str(err))
        self.assertEqual(response.status_code, 422)


if __name__ == '__main__':
    unittest.main()
