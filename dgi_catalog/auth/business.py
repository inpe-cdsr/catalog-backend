"""
business.py
"""

from werkzeug.exceptions import NotFound

from dgi_catalog.model import DatabaseConnection
from dgi_catalog.common import jwt_encode
from dgi_catalog.log import logging


class AuthBusiness():
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def login(self, email, password):
        logging.error('AuthBusiness.login()\n')

        result = self.db_connection.select_user(email=email, password=password)

        # if an empty list (i.e. result == []), then raise an exception
        if not result:
            raise NotFound('E-mail or Password was not found.')

        # get the only one available result
        result = result[0]

        logging.error('AuthBusiness.login() - result[\'email\']: %s', result['email'])

        encoded_token = jwt_encode(result)

        return encoded_token, result
