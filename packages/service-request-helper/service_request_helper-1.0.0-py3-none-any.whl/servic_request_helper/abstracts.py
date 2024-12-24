import abc

class AbstractRequestHeaderManager:

    @abc.abstractmethod
    def get_header_name(self):
        return 'X-My-Hider'

    @abc.abstractmethod
    def get_header_value(self):
        return 'Hider value'


class AbstractRequestFormatter:

    @abc.abstractmethod
    def format(self, data):
        return data


class AbstractResponseFormatter:

    @abc.abstractmethod
    def format(self, response):
        return response.json


class AbstractResponseErrorBuilder:

    @abc.abstractmethod
    def build_error(self, url, method, response):
        if response.status_code // 100 != 2:
            return Exception('Error response')
        return None