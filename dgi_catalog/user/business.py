"""
business.py
"""
from werkzeug.exceptions import Conflict

from dgi_catalog.model import DatabaseConnection


class UserBusiness():
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def insert_user(self, data):
        """
        Inserts a user into database and it returns his/her id
        """

        # check if user exists
        user = self.db_connection.select_user_by_email(data['email'])

        if user:
            raise Conflict('E-mail already registered!')

        # if there is 'address' field, then insert it in the database
        if 'address' in data:
            address_id = self.db_connection.insert_address(data['email'],
                                                           **data['address'])

            del data['address']
            data['addressId'] = address_id

        return self.db_connection.insert_user(**data)

    def delete_user(self, user_id):
        """
        Deletes a user into database based on 'user_id' argument
        """

        return self.db_connection.delete_user(user_id)
