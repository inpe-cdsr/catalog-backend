# disable pylint(line-too-long) (All codes: http://pylint-messages.wikidot.com/all-codes)
# pylint: disable=C0301

"""Controllers"""

from json import loads

from flask import request
from flask_restplus import Resource as APIResource
from werkzeug.exceptions import BadRequest, NotFound

from catalog_backend.common import jwt_decode
from catalog_backend.log import logging
from catalog_backend.user import ns
from catalog_backend.user.business import UserBusiness
from catalog_backend.user.parsers import validate, INSERT_USER_SCHEMA


api = ns

user_business = UserBusiness()


@api.route('/')
@api.route('/<string:user_id>')
class User(APIResource):
    """
    User
    Full route: /api/user/
    """

    def post(self, user_id=None):
        """
        Creates a user into the system

        Request Parameters
        ----------
        request.data : bytes
            JSON in bytes format that contains user information to be inserted
            Example: b"{
                'email': 'test_user@test_user.com', 'password': 'test', 'fullname': 'Test',
                'phone': '1452-2563', 'company': 'Abc',
                'companyType': '', 'activity': 'developer'
            }"

        Returns
        -------
        string
            Returns the user id. User id is the user e-mail
        """

        logging.info('User.post()\n')

        body = request.data

        if body == b'':
            raise BadRequest('Request data is empty.')

        # get request data (bytes) and convert it to dict
        body = loads(body.decode('utf-8'))

        # validate request body
        data, status = validate(body, INSERT_USER_SCHEMA)

        if status is False:
            raise BadRequest(data)

        logging.info('User.post() - fullname: %s', body['fullname'])
        logging.info('User.post() - email: %s\n', body['email'])

        # insert user in the database
        result_id = user_business.insert_user(body)

        # if there is not an id, then raise an exception
        if not result_id:
            raise NotFound('E-mail or password was not found.')

        return {
            "user_id": result_id
        }

    def delete(self, user_id):
        """
        Deletes a user into the system based on his/her id passed as argument

        Request Arguments
        ----------
        user_id : string
            User id

        Returns
        -------
        None
            Nothing
        """

        # get Authorization header and extract just the token
        authorization = request.headers.get('Authorization')[7:]

        # decode the token
        decoded_auth = jwt_decode(authorization)

        # if the logged user is trying to delete another user, then raise an error,
        # because a user can delete just [him|her]self
        if decoded_auth['userId'] != user_id:
            raise BadRequest('Logged user is not allowed to delete another user.')

        if user_id == b'':
            raise BadRequest('User id was not passed.')

        # delete user
        user_business.delete_user(user_id)
