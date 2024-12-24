from datetime import datetime, timedelta

from servic_request_helper import http_methods
from servic_request_helper.auth import BaseAuthHeaderManager
from servic_request_helper.asyncs.clients import RequestHelper
from servic_request_helper.asyncs.response_formatters import JsonResponseFormatter


class AuthByServiceHeaderManager(BaseAuthHeaderManager):

    def __init__(self, host, auth_uri, credential,
                 access_token_field='access_token',
                 access_expire_at_field=None,
                 datetime_converter=datetime.fromisoformat,
                 **kwargs):
        assert host, 'Host for auth service not provided.'
        assert credential, 'Credential for service auth not provided.'
        assert auth_uri, 'URI for service login endpoint not provided.'

        self.api_request_helper = RequestHelper(
            host=host,
            default_response_formatter=JsonResponseFormatter(),
        )
        self.auth_uri = auth_uri
        self.credential = credential
        self.auth_data = None

        self.access_token_field = access_token_field
        self.access_expire_at_field = access_expire_at_field
        self.datetime_converter = datetime_converter

    async def get_header_value(self):
        return 'Bearer ' + await self.get_alive_access_token()

    async def get_alive_access_token(self):
        auth = self.get_auth()
        if not auth or self.is_access_expired(auth):
            await self.refresh_auth()
            auth = self.get_auth()
        return self.get_access_token(auth)

    def get_auth(self):
        return self.auth_data

    def set_auth(self, auth):
        self.auth_data = auth

    async def refresh_auth(self):
        auth_data = await self.api_request_helper.request(
            uri=self.auth_uri,
            method=http_methods.POST,
            json=self.credential,
        )

        assert self.access_token_field in auth_data, 'Auth endpoint response not contain or contain empty value field {} (for assess token)'.format(self.access_token_field)
        assert (self.access_expire_at_field is None) or self.access_expire_at_field in auth_data, 'Auth endpoint response not contain or contain empty value field {} (for access expire at)'.format(self.access_expire_at_field)

        self.set_auth(auth_data)

    def get_access_token(self, auth):
        access_token = auth[self.access_token_field]
        return access_token

    def get_access_expire_at(self, auth):
        access_expire_at = auth[self.access_expire_at_field]
        return self.datetime_converter(access_expire_at)

    def is_access_expired(self, auth):
        if not self.access_expire_at_field:
            return False

        return self.get_access_expire_at(auth) < (datetime.now() + timedelta(minutes=1))
