import humps

from servic_request_helper.abstracts import AbstractResponseFormatter
from servic_request_helper.types import ResponseFile
from servic_request_helper.utils import get_filename_from_content_disposition_header, parse_content_type_header


class FullResponseFormatter(AbstractResponseFormatter):

    def format(self, response):
        return response


class JsonResponseFormatter(AbstractResponseFormatter):

    def format(self, response):
        return response.json()


class JsonDecamelizeResponseFormatter(JsonResponseFormatter):

    def format(self, response):
        return humps.decamelize(super().format(response))


class ContentResponseFormatter(AbstractResponseFormatter):

    def format(self, response):
        return response.content


class FileResponseFormatter(AbstractResponseFormatter):

    def format(self, response):
        headers = response.headers

        filename = get_filename_from_content_disposition_header(headers.get('Content-Disposition'))
        mimetype = parse_content_type_header(headers.get('Content-Type'))

        return ResponseFile(response.content, filename=filename, mimetype=mimetype)
