# disable pylint(line-too-long) (All codes: http://pylint-messages.wikidot.com/all-codes)
# pylint: disable=C0301

"""
test_auth.py file
"""

from json import loads
from unittest import TestCase

from dgi_catalog import app as dgi_catalog_app


app = dgi_catalog_app.test_client()


URL = '/catalog/auth/login'

'''
class TestCatalogAuthLoginSuccess(TestCase):
    """TestCatalogAuthLoginSuccess"""

    def test__post__catalog_auth_login(self):
        """
        TestCatalogAuthLoginSuccess.test__post__catalog_auth_login
        """

        body = b'{"username": "test", "password": "test"}'

        response = app.post(URL, data=body)

        # body = loads(response.data.decode('utf-8'))

        self.assertEqual(200, response.status_code)
        # self.assertEqual(body['message'], 'Request data is empty.')
'''

class TestCatalogAuthLoginError(TestCase):
    """TestCatalogAuthLoginError"""

    def test__post__catalog_auth_login__request_data_is_empty(self):
        """
        TestCatalogAuthLoginError.test__post__catalog_auth_login__request_data_is_empty
        """

        response = app.post(URL)

        body = loads(response.data.decode('utf-8'))

        self.assertEqual(400, response.status_code)
        self.assertEqual(body['message'], 'Request data is empty.')

    def test__post__catalog_auth_login__required_field(self):
        """
        TestCatalogAuthLoginError.test__post__catalog_auth_login__required_field
        """

        test_cases = [
            {
                # when I send this request body to the server, [...]
                'body': b'{"username": "test"}',
                # [...] an 'error_message' should go back
                'error_message': '{"password": ["required field"]}'
            },
            {
                # when I send this request body to the server, [...]
                'body': b'{"password": "test"}',
                # [...] an 'error_message' should go back
                'error_message': '{"username": ["required field"]}'
            }
        ]

        for case in test_cases:
            response = app.post(URL, data=case['body'])

            # response.data is bytes, then convert it to dict
            body = loads(response.data.decode('utf-8'))

            self.assertEqual(400, response.status_code)
            self.assertEqual(body['message'], case['error_message'])
