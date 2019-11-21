"""
business.py
"""
from werkzeug.exceptions import Conflict

from dgi_catalog.model import DatabaseConnection
from dgi_catalog.common import jwt_encode, jwt_decode


class UserBusiness():
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def insert_user(self, data):
        """
        Inserts a user into database and it returns his/her id
        """

        # Verify if exists user
        user = self.db_connection.select_user_by_email(data['email'])
        if user:
            raise Conflict('E-mail already registered!')

        # insert address
        address = self.db_connection.insert_address(data['email'], **data['address'])

        user_infos = data
        user_infos['addressId'] = address
        del user_infos['address']
        
        return self.db_connection.insert_user(**user_infos)

    def delete_user(self, user_id):
        """
        Deletes a user into database based on 'user_id' argument
        """

        return self.db_connection.delete_user(user_id)
