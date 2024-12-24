# coding: utf-8

"""
    AIMMS Cloud rest API client
"""
from aimms_openapi_client import api_client
from aimms_openapi_client import configuration


class AIMMScloudapi:
    """Class to work with the AIMMS Cloud rest API

            :param host_url: Base url of your AIMMS account.
                Something like `https://myaccount.aimms.cloud/pro-api/v2`
            :param api_key: API key to authenticate with the AIMMS Cloud API.
                You need to create an API key in the AIMMS Cloud web interface.
                For more information please look at: https://documentation.aimms.com/cloud/rest-api.html#api-keys-and-scopes

            :Example:
    client = AIMMScloud(host_url='https://myaccount.aimms.cloud/pro-api/v2', api_key='test1234')
    """

    def __init__(self, host_url: str, api_key: str):
        config = configuration.Configuration(host=host_url)
        self.config = config
        self.api_client = api_client.ApiClient(
            config, header_name="apikey", header_value=api_key
        )
