#!/usr/bin/env python3

"""test_auth.py test module"""

from json import loads, dumps
from unittest import TestCase

from catalog_backend import app as catalog_backend_app

from tests.test_environment import TEST_USER_EMAIL, TEST_USER_PASSWORD


catalog_backend_app.testing = True
app = catalog_backend_app.test_client()

URL = '/api/auth/login'


class TestCatalogAuthLoginSuccess(TestCase):
    """TestCatalogAuthLoginSuccess"""

    def test__post__catalog_auth_login__200_success(self):
        """TestCatalogAuthLoginSuccess.test__post__catalog_auth_login"""

        body = {'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD}

        response = app.post(URL, data=dumps(body))

        self.assertEqual(200, response.status_code)
        # check if a non-empty string has been returned (i.e. a token has been returned)
        self.assertNotEqual('', response.data.decode('utf-8'))


class TestCatalogAuthLoginError(TestCase):
    """TestCatalogAuthLoginError"""

    def test__post__catalog_auth_login__400_bad_request__request_data_is_empty(self):
        """TestCatalogAuthLoginError.test__post__catalog_auth_login__400_bad_request__request_data_is_empty"""

        response = app.post(URL)

        body = loads(response.data.decode('utf-8'))

        self.assertEqual(400, response.status_code)
        self.assertEqual('Request data is empty.', body['message'])

    def test__post__catalog_auth_login__400_bad_request__required_field(self):
        """TestCatalogAuthLoginError.test__post__catalog_auth_login__400_bad_request__required_field"""

        test_cases = [
            {
                # when I send this request body to the server, [...]
                'body': b'{"email": "test"}',
                # [...] an 'error_message' should go back
                'expected': {"password": ["required field"]}
            },
            {
                # when I send this request body to the server, [...]
                'body': b'{"password": "test"}',
                # [...] an 'error_message' should go back
                'expected': {"email": ["required field"]}
            }
        ]

        for case in test_cases:
            response = app.post(URL, data=case['body'])

            # response.data is bytes, then convert it to dict
            result = loads(response.data.decode('utf-8'))

            self.assertEqual(400, response.status_code)
            self.assertEqual(case['expected'], result['message'])

    def test__post__catalog_auth_login__404_not_found__email_or_password_was_not_found(self):
        """TestCatalogAuthLoginError.test__post__catalog_auth_login__404_not_found__email_or_password_was_not_found"""

        test_cases = [
            {
                'body': {'email': 'invalid@email.com', 'password': 'invalid_password'}
            },
            {
                'body': {'email': TEST_USER_EMAIL, 'password': 'invalid_password'}
            },
            {
                'body': {'email': 'invalid@email.com', 'password': TEST_USER_PASSWORD}
            }
        ]

        for case in test_cases:
            response = app.post(URL, data=dumps(case['body']))

            result = loads(response.data)

            self.assertEqual(404, response.status_code)
            self.assertEqual('E-mail or Password was not found.', result['message'])
