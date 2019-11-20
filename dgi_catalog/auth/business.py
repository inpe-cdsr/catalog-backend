"""
business.py
"""

from werkzeug.exceptions import NotFound

from dgi_catalog.model import DatabaseConnection
from dgi_catalog.common import jwt_encode, jwt_decode


class AuthBusiness():
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def login(self, email, password):
        result = self.db_connection.select_user(email=email, password=password)

        # if an empty list (i.e. result == []), then raise an exception
        if not result:
            raise NotFound('E-mail or Password was not found.')

        encoded_token = jwt_encode(result[0])

        return encoded_token
