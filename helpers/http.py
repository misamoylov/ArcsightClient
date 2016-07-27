import logging
import requests
import json


class HTTPClient(object):
    """HTTPClient."""  # TODO documentation

    def __init__(self, hostname, login, password):
        logging.info('Initiate HTTPClient with host {}'.format(hostname))
        self.hostname = hostname
        self.login = login
        self.password = password

    @property
    def token(self):
        """This method for get authentication token for Arsight Web Service
        :return: auth token string
        """
        uri = '/www/core-service/rest/LoginService/login?login={}&password={}&alt=json'.format(
            self.login, self.password)
        req = requests.get(self.hostname + uri, verify=False)
        return req.json()['log.loginResponse']['log.return']

    def get(self, endpoint):
        req = requests.get(self.hostname + endpoint + '&authToken={}'.format(self.token), verify=False)
        return req.text

    def post(self, endpoint, data=None):
        if not data:
            data = {}
        headers = {'Content-Type': 'application/xml;charset=utf-8'}
        return  requests.post(self.hostname + endpoint + '&authToken={}'.format(self.token),
                            verify=False, headers=headers, data=data)

    def post_json(self, endpoint, data=None):
        if not data:
            data = {}
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        return requests.post(self.hostname + endpoint + '&authToken={}&alt=json'.format(self.token),
                            verify=False, headers=headers, data=data)
