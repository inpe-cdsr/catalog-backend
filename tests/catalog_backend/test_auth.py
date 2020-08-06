#!/usr/bin/env python3

"""test_auth.py test module"""

from json import loads, dumps
from unittest import TestCase

from catalog_backend import app as catalog_backend_app

from tests.test_environment import TEST_USER_EMAIL, TEST_USER_PASSWORD, TEST_VALID_EMAIL_TO_SEND


catalog_backend_app.testing = True
app = catalog_backend_app.test_client()

URL_AUTH_LOGIN = '/api/auth/login'
URL_AUTH_FORGOT_PASSWORD = '/api/auth/forgot-password'


##################################################
# TestAuthLogin
##################################################

class TestAuthLoginSuccess(TestCase):
    """TestAuthLoginSuccess"""

    def test__post__catalog_auth_login__200_success(self):
        """TestAuthLoginSuccess.test__post__catalog_auth_login"""

        body = {'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD}

        response = app.post(URL_AUTH_LOGIN, data=dumps(body))

        self.assertEqual(200, response.status_code)
        # check if a non-empty string has been returned (i.e. a token has been returned)
        self.assertNotEqual('', response.data.decode('utf-8'))


class TestAuthLoginError(TestCase):
    """TestAuthLoginError"""

    def test__post__catalog_auth_login__400_bad_request__request_data_is_empty(self):
        """TestAuthLoginError.test__post__catalog_auth_login__400_bad_request__request_data_is_empty"""

        response = app.post(URL_AUTH_LOGIN)

        body = loads(response.data.decode('utf-8'))

        self.assertEqual(400, response.status_code)
        self.assertEqual('Request data is empty.', body['message'])

    def test__post__catalog_auth_login__400_bad_request__required_field(self):
        """TestAuthLoginError.test__post__catalog_auth_login__400_bad_request__required_field"""

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
            response = app.post(URL_AUTH_LOGIN, data=case['body'])

            # response.data is bytes, then convert it to dict
            result = loads(response.data.decode('utf-8'))

            self.assertEqual(400, response.status_code)
            self.assertEqual(case['expected'], result['message'])

    def test__post__catalog_auth_login__404_not_found__email_or_password_was_not_found(self):
        """TestAuthLoginError.test__post__catalog_auth_login__404_not_found__email_or_password_was_not_found"""

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
            response = app.post(URL_AUTH_LOGIN, data=dumps(case['body']))

            result = loads(response.data)

            self.assertEqual(404, response.status_code)
            self.assertEqual('E-mail or Password was not found.', result['message'])


##################################################
# TestAuthForgotPassword
##################################################

class TestAuthForgotPasswordSuccess(TestCase):
    """TestAuthForgotPasswordSuccess"""

    def test__get__auth_forgot_password__200_success(self):
        """TestAuthForgotPasswordSuccess.test__get__auth_forgot_password__200_success"""

        email = TEST_VALID_EMAIL_TO_SEND

        response = app.get(URL_AUTH_FORGOT_PASSWORD + '?email={}'.format(email))

        self.assertEqual(200, response.status_code)
        self.assertEqual('', response.data.decode('utf-8'))


class TestAuthForgotPasswordError(TestCase):
    """TestAuthForgotPasswordError"""

    def test__get__auth_forgot_password__400_bad_request__invalid_email_format(self):
        """TestAuthForgotPasswordError.test__get__auth_forgot_password__400_bad_request__invalid_email_format"""

        email = 'test_at_test.com'

        response = app.get(URL_AUTH_FORGOT_PASSWORD + '?email={}'.format(email))

        self.assertEqual(400, response.status_code)
        self.assertEqual({"message": "Invalid e-mail format!"}, loads(response.data))

    def test__get__auth_forgot_password__400_bad_request__email_was_not_found(self):
        """TestAuthForgotPasswordError.test__get__auth_forgot_password__400_bad_request__email_was_not_found"""

        email = 'test@test.com'

        response = app.get(URL_AUTH_FORGOT_PASSWORD + '?email={}'.format(email))

        self.assertEqual(404, response.status_code)
        self.assertEqual({"message": "E-mail was not found."}, loads(response.data))
