"""
business.py
"""

from dgi_catalog.model import DatabaseConnection
from dgi_catalog.common import jwt_encode, jwt_decode


class UserBusiness():
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def insert_user(self, data):
        """
        Inserts a user into database and it returns his/her id
        """

        return self.db_connection.insert_user(**data)

    def delete_user(self, user_id):
        """
        Deletes a user into database based on 'user_id' argument
        """

        return self.db_connection.delete_user(user_id)
