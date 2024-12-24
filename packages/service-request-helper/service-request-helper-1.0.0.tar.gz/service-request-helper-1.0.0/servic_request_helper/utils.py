import re

from servic_request_helper import http_methods


def build_url(host, uri):
    if host.endswith('/'):
        host = host[:-1]

    if uri.startswith('/'):
        uri = uri[1:]

    return f'{host}/{uri}'


def get_filename_from_content_disposition_header(header_value: str):
    if not header_value:
        return None

    match = re.search(r'filename=([^\s]+)', header_value)
    if match:
        return match.group(1)


def parse_content_type_header(header_value: str):
    if not header_value:
        return None

    return header_value.split(';')[0].strip()


class MethodWrapper:

    def __init__(self, request_helper):
        self.request_helper = request_helper

    def _request(self, *args, **kwargs):
        return self.request_helper.request(*args, **kwargs)

    def get(self, uri, **kwargs):
        return self._request(uri, http_methods.GET, **kwargs)

    def post(self, uri, **kwargs):
        return self._request(uri, http_methods.POST, **kwargs)

    def put(self, uri, **kwargs):
        return self._request(uri, http_methods.PUT, **kwargs)

    def patch(self, uri, **kwargs):
        return self._request(uri, http_methods.PATCH, **kwargs)

    def delete(self, uri, **kwargs):
        return self._request(uri, http_methods.DELETE, **kwargs)

    def head(self, uri, **kwargs):
        return self._request(uri, http_methods.HEAD, **kwargs)