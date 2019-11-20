# disable pylint(line-too-long) (All codes: http://pylint-messages.wikidot.com/all-codes)
# pylint: disable=C0301

"""
Controllers
"""

from json import loads, dumps
from flask import request
from flask import Response
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound
from bdc_core.utils.flask import APIResource

from dgi_catalog.user import ns
from dgi_catalog.user.business import UserBusiness
from dgi_catalog.user.parsers import validate, INSERT_USER_SCHEMA


api = ns

user_business = UserBusiness()


@api.route('/')
@api.route('/<string:argument>')
class User(APIResource):
    """
    User
    Full route: /catalog/user/
    """

    def post(self, argument=None):
        """
        Creates a user into the system

        Request Parameters
        ----------
        request.data : bytes
            JSON in bytes format that contains user information to be inserted
            Example: b"{
                'email': 'test_user@test_user.com', 'password': 'test', 'fullname': 'Test',
                'cnpjCpf': '123456', 'areaCode': '12', 'phone': '1452-2563', 'company': 'Abc',
                'companyType': '', 'activity': 'developer', 'addressId': 3
            }"

        Returns
        -------
        string
            Returns the user id. User id is the user e-mail
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

        # if there is not an id, then raise an exception
        if not result_id:
            raise NotFound('E-mail or Password was not found.')

        return Response(result_id)

    def delete(self, argument):
        """
        Deletes a user into the system based on his/her id passed as argument

        Request Parameters
        ----------
        argument : string
            User id

        Returns
        -------
        None
            Nothing
        """

        # TODO: get user token to validate

        print('\n\n argument: ', argument)

        if argument == b'':
            raise BadRequest('User id was not passed.')

        # get request data (bytes) and convert it to dict
        # body = loads(body.decode('utf-8'))

        # delete user
        # user_business.delete_user(argument)
