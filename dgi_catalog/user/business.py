"""
business.py
"""

from dgi_catalog.model import DatabaseConnection
from dgi_catalog.common import jwt_encode, jwt_decode


class UserBusiness():
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def insert_user(self, data):
        # print('\n\n UserBusiness.insert_user()')

        # insert user into database and get user id
        return self.db_connection.insert_user(**data)
