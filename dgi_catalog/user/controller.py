# disable pylint(line-too-long) (All codes: http://pylint-messages.wikidot.com/all-codes)
# pylint: disable=C0301

"""
Controllers
"""

from json import loads, dumps
from flask import request
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound
from bdc_core.utils.flask import APIResource

from dgi_catalog.user import ns
from dgi_catalog.user.business import UserBusiness
from dgi_catalog.user.parsers import validate, INSERT_USER_SCHEMA


api = ns

user_business = UserBusiness()


@api.route('/')
class User(APIResource):
    """
    User
    Full route: /catalog/user/
    """

    def post(self):
        """
        Creates a user into the system

        Request Parameters
        ----------
        request.data : bytes
            JSON in bytes format that contains username and password information of a user
            Example: b'{"username": "test", "password": "test"}'

        Returns
        -------
        boolean
            -
        """

        body = request.data

        if body == b'':
            raise BadRequest('Request data is empty.')

        # get request data (bytes) and convert it to dict
        body = loads(body.decode('utf-8'))

        # validate request body
        data, status = validate(body, INSERT_USER_SCHEMA)

        if status is False:
            raise BadRequest(data)

        # validate user login
        result_id = user_business.insert_user(body)

        # if ..., then raise an exception
        if not result_id:
            raise NotFound('E-mail or Password was not found.')

        return result_id
