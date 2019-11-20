# disable pylint(line-too-long) (All codes: http://pylint-messages.wikidot.com/all-codes)
# pylint: disable=C0301

"""
Controllers
"""

from json import loads, dumps
from flask import request
from flask import Response
from werkzeug.exceptions import BadRequest, InternalServerError
from bdc_core.utils.flask import APIResource

from dgi_catalog.auth import ns
from dgi_catalog.auth.business import AuthBusiness
from dgi_catalog.auth.parsers import validate


api = ns

auth_business = AuthBusiness()


@api.route('/login')
class Login(APIResource):
    """
    Login
    Full route: /catalog/auth/login
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

        body = request.data

        if body == b'':
            raise BadRequest('Request data is empty.')

        # get request data (bytes) and convert it to dict
        body = loads(body.decode('utf-8'))

        # validate request body
        data, status = validate(body, 'login')

        if status is False:
            raise BadRequest(data)

        # validate user login
        token = auth_business.login(body['email'], body['password'])

        # if there is not a token (i.e. empty string), then raise an error
        if not token:
            raise InternalServerError('Error during login.')

        return Response(token)
