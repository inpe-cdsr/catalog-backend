"""
business.py
"""

from dgi_catalog.model import DatabaseConnection
from dgi_catalog.common import jwt_encode, jwt_decode


class UserBusiness():
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def insert_user(self, data):
        # insert user into database and get user id
        return self.db_connection.insert_user(**data)

    def delete_user(self, user_id):
        # delete user into database
        return self.db_connection.delete_user(user_id)
