"""
business.py
"""

from dgi_catalog.model import DatabaseConnection
from dgi_catalog.common import jwt_encode, jwt_decode


class AuthBusiness():
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def login(self, email, password):
        # print('\n\n login()')

        result = self.db_connection.select_user(email=email, password=password)

        encoded_token = jwt_encode(result[0])

        return encoded_token
