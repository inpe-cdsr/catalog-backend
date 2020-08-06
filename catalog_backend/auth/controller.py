# disable pylint(line-too-long) (All codes: http://pylint-messages.wikidot.com/all-codes)
# pylint: disable=C0301

"""Controllers"""

from json import loads

from flask import request, Response
from flask_restplus import Resource as APIResource
from werkzeug.exceptions import BadRequest, InternalServerError

from catalog_backend.auth import ns
from catalog_backend.auth.business import AuthLoginBusiness, AuthForgotPasswordBusiness
from catalog_backend.auth.parsers import validate
from catalog_backend.log import logging


api = ns

auth_login_business = AuthLoginBusiness()
auth_forgot_password_business = AuthForgotPasswordBusiness()


@api.route('/login')
class Login(APIResource):
    """
    Login
    Full route: /api/auth/login
    """

    def post(self):
        """
        Logs a user into the system

        Request Parameters
        ----------
        request.data : bytes
            JSON in bytes format that contains username and password information of a user
            Example: b'{"username": "test", "password": "test"}'

        Returns
        -------
        string
            Token related to the logged user
        """
        logging.info('Login.post()\n')

        body = request.data

        if body == b'':
            raise BadRequest('Request data is empty.')

        # get request data (bytes) and convert it to dict
        body = loads(body.decode('utf-8'))

        # validate request body
        data, status = validate(body, 'login')

        if status is False:
            raise BadRequest(data)

        logging.info('Login.post() - data[\'email\']: %s', data['email'])

        # validate user login
        token, user_info = auth_login_business.login(data['email'], data['password'])

        # logging.info('Login.post() - user_info[\'userId\']: %s', user_info['userId'])
        # logging.info('Login.post() - user_info[\'email\']: %s', user_info['email'])

        # if there is not a token (i.e. empty string), then raise an error
        if not token or not user_info:
            raise InternalServerError('Error during login.')

        return {
            "access_token": token,
            "user_id": user_info['userId'],
            "fullname": user_info['fullname'],
            "email": user_info['email'],
            "password": data['password']
        }


@api.route('/forgot-password')
class ForgotPassword(APIResource):
    """
    ForgotPassword
    Full route: /api/auth/forgot-password
    """

    URN_RESET_PASSWORD = '/api/auth/reset-password'

    def get(self):
        """
        Sends an e-mail to the user to make him create a new password.

        Request Parameters
        ----------
        email : string
            User's e-mail
            Example: my-email@mail.com

        Returns
        -------
        None
            Sends an e-mail with a link to create a new password.
        """
        logging.info('ForgotPassword.get()')

        email = request.args.get('email')

        logging.info('ForgotPassword.get() - email: %s', email)

        # validate request body
        data, status = validate({'email': email}, 'forgot_password')

        if status is False:
            raise BadRequest('Invalid e-mail format!')

        auth_forgot_password_business.send_an_email_to(email)

        return Response(status=200)

'''
@api.route('/reset-password')
class ResetPassword(APIResource):
    """
    Login
    Full route: /api/auth/reset-password
    """

    def post(self):
        """
        Logs a user into the system

        Request Parameters
        ----------
        request.data : bytes
            JSON in bytes format that contains username and password information of a user
            Example: b'{"username": "test", "password": "test"}'

        Returns
        -------
        string
            Token related to the logged user
        """
        logging.info('Login.post()\n')

        body = request.data

        if body == b'':
            raise BadRequest('Request data is empty.')

        # get request data (bytes) and convert it to dict
        body = loads(body.decode('utf-8'))

        # validate request body
        data, status = validate(body, 'login')

        if status is False:
            raise BadRequest(data)

        logging.info('Login.post() - data[\'email\']: %s', data['email'])

        # validate user login
        token, user_info = auth_login_business.login(data['email'], data['password'])

        # logging.info('Login.post() - user_info[\'userId\']: %s', user_info['userId'])
        # logging.info('Login.post() - user_info[\'email\']: %s', user_info['email'])

        # if there is not a token (i.e. empty string), then raise an error
        if not token or not user_info:
            raise InternalServerError('Error during login.')

        return {
            "access_token": token,
            "user_id": user_info['userId'],
            "fullname": user_info['fullname'],
            "email": user_info['email'],
            "password": data['password']
        }
'''
