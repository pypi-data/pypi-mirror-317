import unittest
from servic_request_helper import request_formatters as formatters


class AbstractFormatterTest(unittest.TestCase):
    data = {
        "string_field": "field_value",
        "integer_field": 111111,
        "nested_field": {
            "inner_1": "inner_1",
            "inner_two": "inner_two",
        }
    }


class TestDefaultRequestFormatter(AbstractFormatterTest):
    def test(self):
        formatted_data = formatters.DefaultRequestFormatter().format(self.data)

        self.assertDictEqual(self.data, formatted_data)


class TestCamelizeRequestFormatter(AbstractFormatterTest):
    def test(self):
        formatted_data = formatters.CamelizeRequestFormatter().format(self.data)

        self.assertDictEqual(
            {
                "stringField": "field_value",
                "integerField": 111111,
                "nestedField": {
                    "inner1": "inner_1",
                    "innerTwo": "inner_two",
                }
            },
            formatted_data
        )
