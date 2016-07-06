###################################################################
# The Client class provides several convenient routines to interact
# with Arcsight API Service. It was tested with Python 2.7.5
###################################################################

import ast
import logging
from helpers.http import HTTPClient


class ArcsightClient(object):
    """ArcsightClient"""  # TODO documentation
    def __init__(self, arcsight_hostname, arcsight_login, arcsight_password):
        logging.info('Initiate Arcsight client with url {}'.format(arcsight_hostname))
        self.arcsight_url = "https://{}:8443".format(arcsight_hostname)
        self.arcsight_login = arcsight_login
        self.arcsight_password = arcsight_password
        self._client = HTTPClient(
            hostname=self.arcsight_url, login=self.arcsight_login, password=self.arcsight_password)

    @property
    def client(self):
        return self._client

    def getCaseIds(self):
        endpoint = '/www/manager-service/rest/CaseService/findAllIds?&alt=json'
        return ast.literal_eval(self.client.get(endpoint))['cas.findAllIdsResponse']['cas.return']

    def getCaseContent(self, caseid):
        endpoint = '/www/manager-service/rest/CaseService/getResourceById?&resourceId={}'.format(caseid)
        return self.client.get(endpoint)

    def getCaseContentJson(self, caseid):
        endpoint = '/www/manager-service/rest/CaseService/getResourceById?&alt=json&resourceId={}'.format(caseid)
        return self.client.get(endpoint)

    def getAnyService(self, service):
        endpoint = '/www/manager-service/rest/CaseService/{}?&alt=json&'.format(service)
        return self.client.get(endpoint)

    def updateCase(self, data, caseid):
        endpoint = '/www/manager-service/rest/CaseService/update?&resource={}'.format(caseid)
        return self.client.post(endpoint, data)

    def get_auth_token(self):
        return self.client.token


