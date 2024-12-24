import os
import unittest
from unittest.mock import Mock

from servic_request_helper.syncs import response_formatters as formatters
from servic_request_helper.types import ResponseFile


class AbstractTestJsonResponse(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mock_response = Mock()
        self.mock_response.status_code = 200
        self.mock_response.json = lambda: {
            "testField": "testValue",
            "nestedField": {
                "inner1": "inner_1",
                "innerTwo": "inner_two",
            }
        }

    def get_formatted_mock_response(self, formatter):
         return formatter.format(self.mock_response)


class TestFullResponseFormatter(AbstractTestJsonResponse):

    def test(self):
        formatted_mock_response = self.get_formatted_mock_response(formatters.FullResponseFormatter())

        self.assertIs(self.mock_response, formatted_mock_response)


class TestJsonResponseFormatter(AbstractTestJsonResponse):

    def test(self):
        formatted_mock_response = self.get_formatted_mock_response(formatters.JsonResponseFormatter())

        self.assertDictEqual(
            formatted_mock_response,
            {
                "testField": "testValue",
                "nestedField": {
                    "inner1": "inner_1",
                    "innerTwo": "inner_two",
                }
            })



class TestJsonDecamelizeResponseFormatter(AbstractTestJsonResponse):

    def test(self):
        formatted_mock_response = self.get_formatted_mock_response(formatters.JsonDecamelizeResponseFormatter())

        self.assertDictEqual(formatted_mock_response, {
            "test_field": "testValue",
            "nested_field": {
                "inner1": "inner_1",
                "inner_two": "inner_two",
            }
        })


class AbstractTestContentResponse(unittest.TestCase):

    def get_formatted_mock_response(self, formatter):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'testText'
        mock_response.headers = {
            'Content-Disposition': 'attachment; filename=test.png',
            'Content-Type': 'image/png',
        }

        return formatter.format(mock_response)


class TestContentResponseFormatter(AbstractTestContentResponse):

    def test(self):
        formatted_mock_response = self.get_formatted_mock_response(formatters.ContentResponseFormatter())

        self.assertEqual(formatted_mock_response, b'testText')


class TestFileResponseFormatter(AbstractTestContentResponse):

    def test(self):
        formatted_mock_response = self.get_formatted_mock_response(formatters.FileResponseFormatter())

        self.assertIsInstance(formatted_mock_response, ResponseFile)

        self.assertEqual(getattr(formatted_mock_response, 'content', None), b'testText')
        self.assertEqual(getattr(formatted_mock_response, 'filename', None), 'test.png')
        self.assertEqual(getattr(formatted_mock_response, 'mimetype', None), 'image/png')
        self.assertEqual(getattr(formatted_mock_response, 'size_in_bytes', None), len(b'testText'))

        formatted_mock_response.save('./test_file_response_formatter.txt')

        with open('./test_file_response_formatter.txt', 'rb') as file:
            read_file = file.read()

        self.assertEqual(read_file, b'testText')

    def tearDown(self):
        os.remove('./test_file_response_formatter.txt')
