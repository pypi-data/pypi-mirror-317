import base64

from servic_request_helper.abstracts import AbstractRequestHeaderManager


class BaseAuthHeaderManager(AbstractRequestHeaderManager):

    def get_header_name(self):
        return 'Authorization'


class StaticCredentialsHeaderManager(BaseAuthHeaderManager):
    def __init__(self, header_value):
        self.header_value = header_value

    def get_header_value(self):
        return self.header_value


class BasicAuthHeaderManager(StaticCredentialsHeaderManager):

    def __init__(self, username, password):
        credentials = '{}:{}'.format(username, password)
        header_value = 'Basic ' + base64.b64encode(credentials.encode()).decode()
        super().__init__(header_value)


class StaticTokenAuthHeaderManager(StaticCredentialsHeaderManager):

    def __init__(self, token):
        header_value = 'Bearer ' + token
        super().__init__(header_value)
