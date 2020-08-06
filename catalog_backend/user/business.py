"""business.py"""

from werkzeug.exceptions import Conflict

from catalog_backend.model import DatabaseConnection


class UserBusiness():
    """UserBusiness class"""

    def __init__(self):
        self.db_connection = DatabaseConnection()

    def insert_user(self, data):
        """Inserts a user into database and it returns his/her id"""

        # check if user exists
        user = self.db_connection.select_user(email=data['email'])

        if user:
            raise Conflict('E-mail already registered!')

        # if there is 'address' field, then try to insert address
        # information in the database
        if 'address' in data:
            # if there are properties inside 'address' field,
            # then insert the address in the database
            if data['address']:
                address_id = self.db_connection.insert_address(data['email'],
                                                               **data['address'])
                data['addressId'] = address_id

            # remove 'address' field from dict
            del data['address']

        return self.db_connection.insert_user(**data)

    def delete_user(self, user_id):
        """Deletes a user into database based on 'user_id' argument"""

        return self.db_connection.delete_user(user_id)
