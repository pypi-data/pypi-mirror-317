import humps

from servic_request_helper.abstracts import AbstractResponseFormatter
from servic_request_helper.types import ResponseFile
from servic_request_helper.utils import get_filename_from_content_disposition_header, parse_content_type_header


class FullResponseFormatter(AbstractResponseFormatter):

    async def format(self, response):
        return response


class JsonResponseFormatter(AbstractResponseFormatter):

    async def format(self, response):
        return await response.json()


class JsonDecamelizeResponseFormatter(JsonResponseFormatter):

    async def format(self, response):
        return humps.decamelize(await super().format(response))


class ContentResponseFormatter(AbstractResponseFormatter):

    async def format(self, response):
        return await response.read()


class FileResponseFormatter(AbstractResponseFormatter):

    async def format(self, response):
        headers = response.headers

        filename = get_filename_from_content_disposition_header(headers.get('Content-Disposition'))
        mimetype = parse_content_type_header(headers.get('Content-Type'))

        return ResponseFile(await response.read(), filename=filename, mimetype=mimetype)
