import unittest
from unittest.mock import patch, Mock, MagicMock, AsyncMock

from servic_request_helper import errors
from servic_request_helper.asyncs.clients import RequestHelper


class TestAsyncRequestHelper(unittest.IsolatedAsyncioTestCase):

    async def test_successful_response(self):
        mock_response = Mock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value='{"ping": "pong"}')

        mock_request = AsyncMock()
        mock_request.return_value = mock_response

        mock_ClientSession = MagicMock()
        mock_ClientSession.__aenter__.return_value.request = mock_request

        with unittest.mock.patch('aiohttp.ClientSession', return_value=mock_ClientSession):
            request_helper = RequestHelper(host='http://example.com')
            result = await request_helper.request('test-successful', 'POST')

        self.assertIs(result, mock_response)
        self.assertEqual(mock_request.call_count, 1)

        call_args, call_kwargs = mock_request.call_args

        self.assertEqual(call_args[0], "POST")
        self.assertEqual(call_args[1], "http://example.com/test-successful")

        self.assertIsNone(call_kwargs['params'])
        self.assertIsNone(call_kwargs['json'])
        self.assertIsNone(call_kwargs['data'])

    async def test_request_data_passing(self):
        mock_request = AsyncMock()
        mock_request.return_value.status = 200
        mock_request.return_value.text = AsyncMock(return_value='{"ping": "pong"}')

        mock_ClientSession = MagicMock()
        mock_ClientSession.__aenter__.return_value.request = mock_request

        with unittest.mock.patch('aiohttp.ClientSession', return_value=mock_ClientSession):
            request_helper = RequestHelper(host='http://example.com')
            result = await request_helper.request('test-successful', 'POST',
                                            params={'params': 'params'},
                                            json={'json': 'json'},
                                            data={'data': 'data'},
                                            files={'files': 'files'})

        self.assertEqual(mock_request.call_count, 1)

        call_args, call_kwargs = mock_request.call_args

        params = call_kwargs['params']
        self.assertEqual(len(params), 1)
        self.assertEqual(params['params'], 'params')

        json = call_kwargs['json']
        self.assertEqual(len(json), 1)
        self.assertEqual(json['json'], 'json')

        data = call_kwargs['data']
        self.assertEqual(len(data), 2)
        self.assertEqual(data['data'], 'data')
        self.assertEqual(data['files'], 'files')

        self.assertNotIn('files', call_kwargs)

    async def test_error_responses(self):
        expected_response_text = b'{"ping": "pong"}'

        # Тест для статуса 400 (BadRequest)
        mock_request = AsyncMock()
        mock_request.return_value.status = 400
        mock_request.return_value.text = AsyncMock(return_value='{"ping": "pong"}')

        mock_ClientSession = MagicMock()
        mock_ClientSession.__aenter__.return_value.request = mock_request

        with unittest.mock.patch('aiohttp.ClientSession', return_value=mock_ClientSession):
            request_helper = RequestHelper(host='http://example.com')
            with self.assertRaises(errors.ApiBadRequestError):
                await request_helper.request('test/400', 'POST')

    async def test_headers(self):
        class SyncHeaderManager:

            def get_header_name(self):
                return 'X-TEST-HEADER-SYNC'

            def get_header_value(self):
                return 'x-test-header-sync-value;1234'

        class AsyncHeaderManager:

            def get_header_name(self):
                return 'X-TEST-HEADER-ASYNC'

            async def get_header_value(self):
                return 'x-test-header-async-value;1234'


        mock_request = AsyncMock()
        mock_request.return_value.status = 200
        mock_request.return_value.text = AsyncMock(return_value='{"ping": "pong"}')

        mock_ClientSession = MagicMock()
        mock_ClientSession.__aenter__.return_value.request = mock_request

        with unittest.mock.patch('aiohttp.ClientSession', return_value=mock_ClientSession):
            request_helper = RequestHelper(host='http://example.com',
                                           request_header_managers=[SyncHeaderManager(), AsyncHeaderManager()])
            result = await request_helper.request('test-successful', 'POST',
                                                  headers={'X-TEST-HEADER-STATIC': 'x-test-header-static-value;1234'})

        call_args, call_kwargs = mock_request.call_args

        headers = call_kwargs['headers']
        self.assertDictEqual(
            headers,
            {
                'X-TEST-HEADER-SYNC': 'x-test-header-sync-value;1234',
                'X-TEST-HEADER-ASYNC': 'x-test-header-async-value;1234',
                'X-TEST-HEADER-STATIC': 'x-test-header-static-value;1234',
            },
        )

    async def test_request_all(self):
        mock_response_1 = AsyncMock()
        mock_response_1.status = 201

        mock_response_2 = AsyncMock()
        mock_response_2.status = 202

        mock_request = AsyncMock(side_effect=[mock_response_1, mock_response_2])

        mock_ClientSession = MagicMock()
        mock_ClientSession.__aenter__.return_value.request = mock_request

        with unittest.mock.patch('aiohttp.ClientSession', return_value=mock_ClientSession):
            request_helper = RequestHelper(host='http://example.com')

            result1, result2 = await request_helper.request_all(
                request_helper.prepare_request('test-1', 'POST', json={'ping': 'pong'}),
                request_helper.prepare_request('test-2', 'PUT', json={'foo': 'bar'}),
            )

        self.assertEqual(result1, mock_response_1)
        self.assertEqual(result2, mock_response_2)

        self.assertEqual(mock_request.call_count, 2)

        call_args_1, call_kwargs_1 = mock_request.call_args_list[0]
        method_1, url_1  = call_args_1

        self.assertEqual(url_1, 'http://example.com/test-1')
        self.assertEqual(method_1, 'POST')
        self.assertDictEqual(call_kwargs_1['json'], {'ping': 'pong'})

        call_args_2, call_kwargs_2 = mock_request.call_args_list[1]
        method_2, url_2 = call_args_2

        self.assertEqual(url_2, 'http://example.com/test-2')
        self.assertEqual(method_2, 'PUT')
        self.assertDictEqual(call_kwargs_2['json'], {'foo': 'bar'})


if __name__ == '__main__':
    unittest.main()
