import requests


"""Calamari Authentication Client, which contains methods for;
- authenticating user (basing on credentials stored in config.py)
- basic GET and POST requests
"""


class CalamariClient(object):
    def __init__(self, api_url, username, password):
        self._api_url = api_url
        self._username = username
        self._password = password

    def authenticate(self):
        client = requests.session()
        client.post(self._api_url+"auth/login/",
                    {
                        'username': self._username,
                        'password': self._password
                    })
        print client.cookies
        return client

    def get(self, endpoint):
        client = self.authenticate()
        response = client.get(self._api_url+endpoint)
        return response.json()

    def post(self, endpoint, data):
        client = self.authenticate()
        response = client.post(self._api_url+endpoint, data=data)
        return response.json()