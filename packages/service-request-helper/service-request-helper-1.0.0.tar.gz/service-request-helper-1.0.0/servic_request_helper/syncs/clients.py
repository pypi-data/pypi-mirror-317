try:
    import requests
except ImportError:
    raise Exception("For user sync rest api client you must have the requests package installed")

from servic_request_helper import errors, utils
from servic_request_helper.request_formatters import DefaultRequestFormatter
from servic_request_helper.syncs.error_builders import ResponseStatusErrorBuilder
from servic_request_helper.syncs.response_formatters import FullResponseFormatter


_default_request_formatter = DefaultRequestFormatter()
_default_response_formatter = FullResponseFormatter()
_default_response_error_builder = ResponseStatusErrorBuilder()


class RequestHelper:
    host = None
    default_request_formatter = None
    default_response_formatter = None
    request_header_managers = []
    default_response_error_builder = None

    def __init__(self, host,
                 default_request_formatter=_default_request_formatter,
                 default_response_formatter=_default_response_formatter,
                 request_header_managers=tuple(),
                 default_response_error_builder=_default_response_error_builder,
                 **kwargs):
        self.host = host
        self.default_request_formatter = default_request_formatter
        self.default_response_formatter = default_response_formatter
        self.request_header_managers = request_header_managers
        self.default_response_error_builder = default_response_error_builder

    def _build_headers(self, headers=None):
        if headers is None:
            headers = {}

        for header_manager in self.request_header_managers:
            headers[header_manager.get_header_name()] = header_manager.get_header_value()

        return headers

    def request(self, uri, method, request_formatter=None, response_formatter=None, response_error_builder=None, params=None, json=None, data=None, files=None, headers=None, **kwargs):
        url = utils.build_url(self.host, uri)

        _headers = self._build_headers(headers)
        _request_formatter = request_formatter or self.default_request_formatter
        _response_formatter = response_formatter or self.default_response_formatter
        _response_error_builder = response_error_builder or self.default_response_error_builder

        try:
            response = requests.request(
                method,
                url,
                headers=_headers,

                params=_request_formatter.format(params),
                json=_request_formatter.format(json),
                data=_request_formatter.format(data),
                files=files,
                **kwargs,
            )
        except requests.exceptions.ConnectionError as e:
            raise errors.ApiConnectionError(url, method, e)
        except requests.exceptions.Timeout as e:
            raise errors.ApiTimeoutError(url, method, e)
        except requests.exceptions.RequestException as e:
            raise errors.ApiRequestError(url, method, e)

        response_error = _response_error_builder.build_error(url, method, response)
        if response_error:
            raise response_error

        return _response_formatter.format(response)
