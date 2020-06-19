"""business.py"""

from werkzeug.exceptions import NotFound

from catalog_backend.common import jwt_encode
from catalog_backend.log import logging
from catalog_backend.model import DatabaseConnection


class AuthBusiness():
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def login(self, email, password):
        logging.info('AuthBusiness.login()\n')

        result = self.db_connection.select_user(email=email, password=password)

        # if an empty list (i.e. result == []), then raise an exception
        if not result:
            raise NotFound('E-mail or Password was not found.')

        # get the only one available result
        result = result[0]

        logging.info('AuthBusiness.login() - result[\'email\']: %s', result['email'])

        encoded_token = jwt_encode(result)

        return encoded_token, result
