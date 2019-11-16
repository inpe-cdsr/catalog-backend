"""
Controllers
"""

from json import loads, dumps
from flask import request
from werkzeug.exceptions import BadRequest, InternalServerError
from bdc_core.utils.flask import APIResource

from dgi_catalog.auth import ns
from dgi_catalog.auth.business import AuthBusiness
from dgi_catalog.auth.parsers import validate


api = ns


# Full route: /catalog/auth/login
@api.route('/login')
class Login(APIResource):

    def post(self):
        """
        Logging into the system
        """

        body = request.data

        if body == b'':
            raise BadRequest('Request data is empty.')

        # get request data (bytes) and convert it to dict
        body = loads(body.decode('utf-8'))

        # validate request body
        data, status = validate(body, 'login')

        if status is False:
            raise BadRequest(dumps(data))

        # validate user login
        auth = AuthBusiness.login(data['username'], data['password'])

        if not auth:
            raise InternalServerError('Error logging!')

        return auth
