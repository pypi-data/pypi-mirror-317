import unittest
from unittest.mock import patch, Mock, AsyncMock, MagicMock

from servic_request_helper.asyncs.auth import AuthByServiceHeaderManager


class TestAuthByServiceHeaderManager(unittest.IsolatedAsyncioTestCase):

    async def test(self):
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={'test_token_field': 'MyTestTokenValue'})

        mock_request = AsyncMock()
        mock_request.return_value = mock_response

        mock_ClientSession = MagicMock()
        mock_ClientSession.__aenter__.return_value.request = mock_request

        with unittest.mock.patch('aiohttp.ClientSession', return_value=mock_ClientSession):
            manager = AuthByServiceHeaderManager(
                host='http://example.com',
                auth_uri='auth/login',
                credential={'ping': 'ping', 'pong': 'pong'},
                access_token_field='test_token_field',
            )
            self.assertEqual(manager.get_header_name(), 'Authorization')
            self.assertEqual(await manager.get_header_value(),  'Bearer MyTestTokenValue')
            self.assertEqual(await manager.get_header_value(),  'Bearer MyTestTokenValue')
            self.assertEqual(await manager.get_header_value(),  'Bearer MyTestTokenValue')
            self.assertEqual(await manager.get_header_value(),  'Bearer MyTestTokenValue')

        self.assertEqual(mock_request.call_count, 1)

        call_args, call_kwargs = mock_request.call_args

        self.assertEqual(call_args[0], "POST")
        self.assertEqual(call_args[1], "http://example.com/auth/login")

        self.assertIsNone(call_kwargs['params'])
        self.assertIsNone(call_kwargs['data'])
        self.assertDictEqual(call_kwargs['json'], {'ping': 'ping', 'pong': 'pong'})


if __name__ == '__main__':
    unittest.main()
