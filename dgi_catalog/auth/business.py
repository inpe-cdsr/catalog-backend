"""
business.py
"""

from dgi_catalog.model import DatabaseConnection
from dgi_catalog.common import jwt_encode, jwt_decode


class AuthBusiness():
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def login(self, username, password):
        print('\nusername: ', username)
        print('password: ', password)

        # result = self.db_connection.select_user(username=username, password=password)

        # encoded_token = jwt_encode(result)

        return True
