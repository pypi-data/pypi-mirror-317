import unittest
from unittest.mock import patch, Mock

from servic_request_helper import errors
from servic_request_helper.syncs.clients import RequestHelper


class TestBlockingRequestHelper(unittest.TestCase):

    @patch('requests.request')
    def test_successful_response(self, mock_request):
        expected_response_text = b'{"ping": "pong"}'
        expected_status_code = 201

        mock_response = Mock()
        mock_response.status_code = expected_status_code
        mock_response.text = expected_response_text
        mock_request.return_value = mock_response

        #
        request_helper = RequestHelper(host='http://example.com')
        result = request_helper.request('test-successful', 'POST')
        #

        self.assertIs(result, mock_response)
        self.assertEqual(mock_request.call_count, 1)

        call_args, call_kwargs = mock_request.call_args

        self.assertEqual(call_args[0], "POST")
        self.assertEqual(call_args[1], "http://example.com/test-successful")

        self.assertIsNone(call_kwargs['params'])
        self.assertIsNone(call_kwargs['json'])
        self.assertIsNone(call_kwargs['data'])
        self.assertIsNone(call_kwargs['files'])

    @patch('requests.request')
    def test_request_data_passing(self, mock_request):
        expected_status_code = 201

        mock_response = Mock()
        mock_response.status_code = expected_status_code
        mock_request.return_value = mock_response

        #
        request_helper = RequestHelper(host='http://example.com')
        result = request_helper.request('test-successful', 'POST',
                                        params={'params': 'params'},
                                        json={'json': 'json'},
                                        data={'data': 'data'},
                                        files={'files': 'files'})
        #

        self.assertIs(result, mock_response)
        self.assertEqual(mock_request.call_count, 1)

        call_args, call_kwargs = mock_request.call_args

        params = call_kwargs['params']
        self.assertEqual(len(params), 1)
        self.assertEqual(params['params'], 'params')

        json = call_kwargs['json']
        self.assertEqual(len(json), 1)
        self.assertEqual(json['json'], 'json')

        data = call_kwargs['data']
        self.assertEqual(len(data), 1)
        self.assertEqual(data['data'], 'data')

        files = call_kwargs['files']
        self.assertEqual(len(files), 1)
        self.assertEqual(files['files'], 'files')

    @patch('requests.request')
    def test_error_responses(self, mock_request):
        expected_response_text = b'{"ping": "pong"}'

        mock_response_400 = Mock()
        mock_response_400.status_code = 400
        mock_response_400.text = expected_response_text
        mock_request.return_value = mock_response_400
        request_helper = RequestHelper(host='http://example.com')
        with self.assertRaises(errors.ApiBadRequestError):
            request_helper.request('test/400', 'POST')

        mock_response_401 = Mock()
        mock_response_401.status_code = 401
        mock_response_401.text = expected_response_text
        mock_request.return_value = mock_response_401
        with self.assertRaises(errors.ApiUnauthorizedError):
            request_helper.request('test/401', 'POST')

        mock_response_403 = Mock()
        mock_response_403.status_code = 403
        mock_response_403.text = expected_response_text
        mock_request.return_value = mock_response_403
        with self.assertRaises(errors.ApiForbiddenError):
            request_helper.request('test/403', 'POST')

        mock_response_404 = Mock()
        mock_response_404.status_code = 404
        mock_response_404.text = expected_response_text
        mock_request.return_value = mock_response_404
        with self.assertRaises(errors.ApiNotFoundError):
            request_helper.request('test/404', 'POST')

        mock_response_502 = Mock()
        mock_response_502.status_code = 502
        mock_response_502.text = expected_response_text
        mock_request.return_value = mock_response_502
        with self.assertRaises(errors.ApiBadGatewayError):
            request_helper.request('test/502', 'POST')

        mock_response_504 = Mock()
        mock_response_504.status_code = 504
        mock_response_504.text = expected_response_text
        mock_request.return_value = mock_response_504
        with self.assertRaises(errors.ApiGatewayTimeoutError):
            request_helper.request('test/504', 'POST')

        mock_response_error = Mock()
        mock_response_error.status_code = 500
        mock_response_error.text = expected_response_text
        mock_request.return_value = mock_response_error
        with self.assertRaises(errors.ApiResponseWithError):
            request_helper.request('test/500', 'POST')


if __name__ == '__main__':
    unittest.main()
