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


class TestCatalogAuthLoginSuccess(TestCase):
    """
    TestCatalogAuthLoginSuccess
    """

    def test__post__catalog_auth_login__200_success(self):
        """
        TestCatalogAuthLoginSuccess.test__post__catalog_auth_login
        """

        body = { 'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD }

        response = app.post(URL, data=dumps(body))

        self.assertEqual(200, response.status_code)
        # check if a non-empty string has been returned (i.e. a token has been returned)
        self.assertNotEqual('', loads(response.data))


class TestCatalogAuthLoginError(TestCase):
    """
    TestCatalogAuthLoginError
    """

    def test__post__catalog_auth_login__400_bad_request__request_data_is_empty(self):
        """
        TestCatalogAuthLoginError.test__post__catalog_auth_login__400_bad_request__request_data_is_empty
        """

        response = app.post(URL)

        body = loads(response.data.decode('utf-8'))

        self.assertEqual(400, response.status_code)
        self.assertEqual('Request data is empty.', body['message'])

    def test__post__catalog_auth_login__400_bad_request__required_field(self):
        """
        TestCatalogAuthLoginError.test__post__catalog_auth_login__400_bad_request__required_field
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

    def test__post__catalog_auth_login__404_not_found__email_or_password_was_not_found(self):
        """
        TestCatalogAuthLoginError.test__post__catalog_auth_login__404_not_found__email_or_password_was_not_found
        """

        body = { 'email': 'invalid@email.com', 'password': 'invalid_password' }

        response = app.post(URL, data=dumps(body))

        body = loads(response.data)

        self.assertEqual(404, response.status_code)
        self.assertEqual('E-mail or Password was not found.', body['message'])
