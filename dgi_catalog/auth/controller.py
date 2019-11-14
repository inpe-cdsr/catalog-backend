"""Controllers
"""
import json
from flask import request
from werkzeug.exceptions import BadRequest
from bdc_core.utils.flask import APIResource

from dgi_catalog.auth import ns
from dgi_catalog.auth.business import AuthBusiness
from dgi_catalog.auth.parsers import validate

api = ns

@api.route('/login')
class Login(APIResource):

    def post(self):
        """
        Logging in to the system
        """
        data, status = validate(request.json, 'login')
        if status is False:
            raise BadRequest(json.dumps(data))

        auth = AuthBusiness.login(data['username'], data['password'])
        if not auth:
            raise InternalServerError('Error logging!')

        return auth

