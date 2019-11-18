"""
business.py
"""

from dgi_catalog.model import DatabaseConnection


class AuthBusiness():
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def login(self, username, password):
        print('\nusername: ', username)
        print('password: ', password)

        # result = self.db_connection.select_user(username=username, password=password)

        return True
