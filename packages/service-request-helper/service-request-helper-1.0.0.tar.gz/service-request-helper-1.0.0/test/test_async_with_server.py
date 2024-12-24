import unittest
import asyncio
from io import BytesIO

import aiohttp
import httpretty
from aioresponses import aioresponses, CallbackResult

from servic_request_helper import errors

from servic_request_helper.asyncs.clients import RequestHelper
from servic_request_helper.asyncs.response_formatters import JsonResponseFormatter


class TestRequestHelper(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        httpretty.enable()

        httpretty.register_uri(
            httpretty.POST, "http://example.com/test-successful",
            body="This is a test response",
            status=201,
            adding_headers={
                'Content-Type': ' text/plain'
            }
        )

        httpretty.register_uri(
            httpretty.GET, "http://example.com/test-with-query?foo=bar",
            body="This is a test with param response",
            status=200,
            adding_headers={
                'Content-Type': ' text/plain'
            }
        )

        httpretty.register_uri(
            httpretty.GET, "http://example.com/test-json",
            body=b'{"foo":"bar"}',
            status=200,
            adding_headers={
                'Content-Type': ' application/json'
            }
        )

        httpretty.register_uri(
            httpretty.POST, "http://example.com/test/400",
            body="This is a error response",
            status=400,
            adding_headers={
                'Content-Type': ' text/plain'
            }
        )

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()

    async def test_successful_response(self):
        request_helper = RequestHelper(host='http://example.com')
        response = await request_helper.request('test-successful', 'POST')

        self.assertEqual(response.status, 201)
        self.assertEqual(await response.text(), "This is a test response")

    async def test_response_with_query_param(self):
        request_helper = RequestHelper(host='http://example.com')
        response = await request_helper.request('test-with-query', 'GET', params={'foo': 'bar'})

        self.assertEqual(response.status, 200)
        self.assertEqual(await response.text(), "This is a test with param response")

    async def test_json_response(self):
        request_helper = RequestHelper(host='http://example.com')
        result = await request_helper.request('test-json', 'GET', response_formatter=JsonResponseFormatter())

        self.assertDictEqual(result, {'foo': 'bar'})

    async def test_failure_response(self):
        request_helper = RequestHelper(host='http://example.com')

        with self.assertRaises(errors.ApiBadRequestError):
            await request_helper.request('test/400', 'POST')


class TestFileRequestHelper(unittest.IsolatedAsyncioTestCase):

    @aioresponses()
    async def test_file_response(self, m):
        def request_multipart_callback(url, *args, data=None, **kwargs):
            self.assertIn('ping', data)
            self.assertIn('test_file', data)

            return CallbackResult(
                status=200,
                body=b'Ok',
            )

        m.post('http://example.com/test-multipart', callback=request_multipart_callback)

        request_helper = RequestHelper(host='http://example.com')
        with BytesIO() as f:
            f.write(b'TextTextText')
            f.name = 'test.txt'
            f.seek(0)

            response = await request_helper.request('test-multipart', 'POST', data={'ping': 'pong'}, files={'test_file': f})

        self.assertEqual(await response.text(), 'Ok')
        self.assertEqual(response.status, 200)


class TestFailureConnectionRequestHelper(unittest.IsolatedAsyncioTestCase):

    async def test_connection_error(self):
        request_helper = RequestHelper(host='http://0.0.0.0')

        with self.assertRaises(errors.ApiRequestError):
            await request_helper.request('test-multipart', 'POST')


if __name__ == '__main__':
    unittest.main()
