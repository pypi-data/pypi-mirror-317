import asyncio
import inspect

try:
    import aiohttp
except ImportError:
    raise Exception("For user sync rest api client you must have the aiohttp package installed")

from servic_request_helper import errors, utils
from servic_request_helper.request_formatters import DefaultRequestFormatter
from servic_request_helper.asyncs.response_formatters import FullResponseFormatter
from servic_request_helper.asyncs.error_builders import ResponseStatusErrorBuilder


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

    async def _build_headers(self, headers=None):
        if headers is None:
            headers = {}

        for header_manager in self.request_header_managers:
            if inspect.iscoroutinefunction(header_manager.get_header_value):
                header_value = await header_manager.get_header_value()
            else:
                header_value = header_manager.get_header_value()
            headers[header_manager.get_header_name()] = header_value

        return headers

    async def request(self, *args, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await self.request_with_session(session, *args, **kwargs)

    async def request_all(self, *prepared_requests):
        async with aiohttp.ClientSession() as session:

            coroutines = map(lambda pr: self.make_prepared_request_with_session(session, pr), prepared_requests)

            result = await asyncio.gather(*coroutines)

        return result

    def prepare_request(self, *args, **kwargs):
        return args, kwargs

    async def make_prepared_request_with_session(self, session, prepared_requests):
        return await self.request_with_session(session, *(prepared_requests[0]), **(prepared_requests[1]))

    async def request_with_session(self, session, uri, method, request_formatter=None, response_formatter=None, response_error_builder=None, params=None, json=None, data=None, files=None, headers=None, **kwargs):
        url = utils.build_url(self.host, uri)

        _headers = await self._build_headers(headers)
        _request_formatter = request_formatter or self.default_request_formatter
        _response_formatter = response_formatter or self.default_response_formatter
        _response_error_builder = response_error_builder or self.default_response_error_builder

        _data = None
        if data or files:
            _data = {}
            if data:
                _data.update(data)
            if files:
                _data.update(files)

        try:
            response = await session.request(
                method,
                url,
                headers=_headers,

                params=_request_formatter.format(params),
                json=_request_formatter.format(json),
                data=_request_formatter.format(_data),
                **kwargs,
            )
        except aiohttp.client_exceptions.ServerTimeoutError as e:
            raise errors.ApiTimeoutError(url, method, e)
        except aiohttp.client_exceptions.ClientConnectionError as e:
            raise errors.ApiConnectionError(url, method, e)
        except aiohttp.client_exceptions.ClientError as e:
            raise errors.ApiRequestError(url, method, e)

        response_error = await _response_error_builder.build_error(url, method, response)
        if response_error:
            raise response_error

        return await _response_formatter.format(response)
