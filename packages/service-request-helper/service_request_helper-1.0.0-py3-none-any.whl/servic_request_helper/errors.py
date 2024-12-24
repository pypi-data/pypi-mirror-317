import json

class ApiError(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ApiRequestError(ApiError):

    def __init__(self, url, method, e, *args, **kwargs):
        super().__init__("Request to {} {} raise error {}".format(method, url, e))


class ApiConnectionError(ApiRequestError):
    pass


class ApiTimeoutError(ApiRequestError):
    pass


class ApiResponseWithError(ApiError):

    def __init__(self, url, method, status_code, text, *args, **kwargs):
        super().__init__("Endpoint {} {} response with {}:{}".format(method, url, status_code, text))
        self.status_code = status_code
        try:
            self.response_body = json.loads(text)
            self.has_response_body = True
        except:
            self.response_body = {}
            self.has_response_body = False


class ApiServerError(ApiResponseWithError):
    pass


class ApiBadGatewayError(ApiServerError):
    pass


class ApiGatewayTimeoutError(ApiServerError):
    pass


class ApiClientError(ApiResponseWithError):
    pass


class ApiBadRequestError(ApiClientError):
    pass


class ApiUnauthorizedError(ApiClientError):
    pass


class ApiForbiddenError(ApiClientError):
    pass


class ApiNotFoundError(ApiClientError):
    pass
