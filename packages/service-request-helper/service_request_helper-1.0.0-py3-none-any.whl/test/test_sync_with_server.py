import unittest
import httpretty
from io import BytesIO
from servic_request_helper import errors

from servic_request_helper.syncs.clients import RequestHelper
from servic_request_helper.syncs.response_formatters import JsonResponseFormatter


class TestBlockingRequestHelper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        httpretty.enable()

        httpretty.register_uri(
            httpretty.POST, "http://example.com/test-successful",
            body="This is a test response",
            status=201
        )

        httpretty.register_uri(
            httpretty.GET, "http://example.com/test-with-query?foo=bar",
            body="This is a test with param response",
            status=200
        )

        httpretty.register_uri(
            httpretty.GET, "http://example.com/test-json",
            body=b'{"foo":"bar"}',
            status=200
        )

        httpretty.register_uri(
            httpretty.POST, "http://example.com/test/400",
            body="This is a error response",
            status=400
        )

        def request_multipart_callback(request, uri, response_headers):
            content_type = request.headers.get('Content-Type', '')
            if not content_type.lower().startswith('multipart/form-data'):
                return 400, response_headers, b'Request content type not multipart'

            boundary = content_type[31:]
            if not boundary:
                return 400, response_headers, b'Content type not have boundary'

            if not b'Content-Disposition: form-data; name="ping"\r\n\r\npong' in request.body:
                return 400, response_headers, b'No field ping with value pong in body'

            if not b'Content-Disposition: form-data; name="test_file"; filename="test.txt"\r\n\r\nTextTextText' in request.body:
                return 400, response_headers, b'No field test_file with value as file with name test.txt with content \'TextTextText\' in body'

            return [200, response_headers, b'Ok']

        httpretty.register_uri(
            httpretty.POST, "http://example.com/test-multipart",
            body=request_multipart_callback,
            status=200,
        )

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()

    def test_successful_response(self):
        request_helper = RequestHelper(host='http://example.com')
        response = request_helper.request('test-successful', 'POST')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.text, "This is a test response")

    def test_response_with_query_param(self):
        request_helper = RequestHelper(host='http://example.com')
        response = request_helper.request('test-with-query', 'GET', params={'foo': 'bar'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "This is a test with param response")

    def test_json_response(self):
        request_helper = RequestHelper(host='http://example.com')
        result = request_helper.request('test-json', 'GET', response_formatter=JsonResponseFormatter())

        self.assertDictEqual(result, {'foo': 'bar'})

    def test_file_response(self):
        request_helper = RequestHelper(host='http://example.com')
        with BytesIO() as f:
            f.write(b'TextTextText')
            f.name = 'test.txt'
            f.seek(0)
            response = request_helper.request('test-multipart', 'POST', data={'ping': 'pong'}, files={'test_file': f})

        self.assertEqual(response.text, 'Ok')
        self.assertEqual(response.status_code, 200)

    def test_failure_response(self):
        request_helper = RequestHelper(host='http://example.com')

        with self.assertRaises(errors.ApiBadRequestError):
            request_helper.request('test/400', 'POST')


if __name__ == '__main__':
    unittest.main()

