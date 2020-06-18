# disable pylint(line-too-long) (All codes: http://pylint-messages.wikidot.com/all-codes)
# pylint: disable=C0301

"""
Controllers
"""

from json import loads, dumps
from flask import request
from flask import Response
from werkzeug.exceptions import BadRequest, InternalServerError
from flask_restplus import Resource as APIResource

from dgi_catalog.auth import ns
from dgi_catalog.auth.business import AuthBusiness
from dgi_catalog.auth.parsers import validate
from dgi_catalog.log import logging


api = ns

auth_business = AuthBusiness()


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
        token, user_info = auth_business.login(data['email'], data['password'])

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
