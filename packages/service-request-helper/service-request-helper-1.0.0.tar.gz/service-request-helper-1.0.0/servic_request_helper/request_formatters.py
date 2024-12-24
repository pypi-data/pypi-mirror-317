import humps

from servic_request_helper.abstracts import AbstractRequestFormatter


class DefaultRequestFormatter(AbstractRequestFormatter):
    def format(self, data):
        return data


class CamelizeRequestFormatter(AbstractRequestFormatter):
    def format(self, data):
        if not data:
            return data

        return humps.camelize(data)
