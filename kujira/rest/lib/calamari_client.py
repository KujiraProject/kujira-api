"""Calamari Authentication Client, which contains methods for;
- authenticating user (basing on credentials stored in config.py)
- basic GET and POST requests"""

import requests


class CalamariClient(object):
    def __init__(self, api_url, username, password, timeout):
        self._api_url = api_url
        self._username = username
        self._password = password
        self._timeout = timeout

    def authenticate(self):
        client = requests.session()
        client.post(self._api_url+"auth/login/",
                    {
                        'username': self._username,
                        'password': self._password
                    },
                    timeout=self._timeout)
        print client.cookies
        return client

    def get(self, endpoint):
        client = self.authenticate()
        response = client.get(self._api_url+endpoint, timeout=self._timeout)
        return response.json()

    def post(self, endpoint, data):
        client = self.authenticate()
        response = client.post(self._api_url+endpoint, data=data, timeout=self._timeout)
        return response.json()
