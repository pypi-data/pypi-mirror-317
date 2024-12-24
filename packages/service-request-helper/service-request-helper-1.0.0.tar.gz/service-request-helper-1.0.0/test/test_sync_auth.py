import unittest
from unittest.mock import patch, Mock

from servic_request_helper.auth import BasicAuthHeaderManager, StaticTokenAuthHeaderManager
from servic_request_helper.syncs.auth import AuthByServiceHeaderManager


class TestBasicAuthHeaderManager(unittest.TestCase):

    def test(self):
        manager1 = BasicAuthHeaderManager('ping', 'pong')
        self.assertEqual(manager1.get_header_name(), 'Authorization')
        self.assertEqual(manager1.get_header_value(), 'Basic cGluZzpwb25n')

        manager2 = BasicAuthHeaderManager('ping', '123!@#$%^&*(')
        self.assertEqual(manager2.get_header_value(), 'Basic cGluZzoxMjMhQCMkJV4mKig=')


class TestStaticTokenAuthHeaderManager(unittest.TestCase):

    def test(self):
        token = 'ping-ping-pong-123456789-1234567890-='
        manager1 = StaticTokenAuthHeaderManager(token)
        self.assertEqual(manager1.get_header_name(), 'Authorization')
        self.assertEqual(manager1.get_header_value(), 'Bearer ' + token)


class TestAuthByServiceHeaderManager(unittest.TestCase):

    @patch('requests.request')
    def test(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = lambda: {'test_token_field': 'MyTestTokenValue'}
        mock_request.return_value = mock_response

        manager = AuthByServiceHeaderManager(
            host='http://example.com',
            auth_uri='auth/login',
            credential={'ping': 'ping', 'pong': 'pong'},
            access_token_field='test_token_field',
        )
        self.assertEqual(manager.get_header_name(), 'Authorization')
        self.assertEqual(manager.get_header_value(),  'Bearer MyTestTokenValue')
        self.assertEqual(manager.get_header_value(),  'Bearer MyTestTokenValue')
        self.assertEqual(manager.get_header_value(),  'Bearer MyTestTokenValue')
        self.assertEqual(manager.get_header_value(),  'Bearer MyTestTokenValue')

        self.assertEqual(mock_request.call_count, 1)

        call_args, call_kwargs = mock_request.call_args

        self.assertEqual(call_args[0], "POST")
        self.assertEqual(call_args[1], "http://example.com/auth/login")

        self.assertIsNone(call_kwargs['params'])
        self.assertIsNone(call_kwargs['data'])
        self.assertIsNone(call_kwargs['files'])
        self.assertDictEqual(call_kwargs['json'], {'ping': 'ping', 'pong': 'pong'})


if __name__ == '__main__':
    unittest.main()
