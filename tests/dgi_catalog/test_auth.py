# disable pylint(line-too-long) (All codes: http://pylint-messages.wikidot.com/all-codes)
# pylint: disable=C0301

"""
test_auth.py file
"""

from unittest import TestCase
from json import loads, dumps

from dgi_catalog import app as dgi_catalog_app
from test_environment import TEST_USER_EMAIL, TEST_USER_PASSWORD


app = dgi_catalog_app.test_client()

URL = '/catalog/auth/login'

'''
class TestCatalogAuthLoginSuccess(TestCase):
    """
    TestCatalogAuthLoginSuccess
    """

    def test__post__catalog_auth_login(self):
        """
        TestCatalogAuthLoginSuccess.test__post__catalog_auth_login
        """

        body = { "email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD }

        response = app.post(URL, data=dumps(body))

        # print('\nresponse.data: ', response.data)

        self.assertEqual(200, response.status_code)
        self.assertTrue(loads(response.data))
'''


class TestCatalogAuthLoginError(TestCase):
    """
    TestCatalogAuthLoginError
    """

    def test__post__catalog_auth_login__request_data_is_empty(self):
        """
        TestCatalogAuthLoginError.test__post__catalog_auth_login__request_data_is_empty
        """

        response = app.post(URL)

        body = loads(response.data.decode('utf-8'))

        self.assertEqual(400, response.status_code)
        self.assertEqual('Request data is empty.', body['message'])

    def test__post__catalog_auth_login__required_field(self):
        """
        TestCatalogAuthLoginError.test__post__catalog_auth_login__required_field
        """

        test_cases = [
            {
                # when I send this request body to the server, [...]
                'body': b'{"email": "test"}',
                # [...] an 'error_message' should go back
                'expected': '{"password": ["required field"]}'
            },
            {
                # when I send this request body to the server, [...]
                'body': b'{"password": "test"}',
                # [...] an 'error_message' should go back
                'expected': '{"email": ["required field"]}'
            }
        ]

        for case in test_cases:
            response = app.post(URL, data=case['body'])

            # response.data is bytes, then convert it to dict
            body = loads(response.data.decode('utf-8'))

            self.assertEqual(400, response.status_code)
            self.assertEqual(case['expected'], body['message'])
