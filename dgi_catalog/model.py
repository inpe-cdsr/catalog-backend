"""
DGI Catalog
"""

from mysql.connector import connect, errorcode, Error

from dgi_catalog.environment import MYSQL_DB_USER, MYSQL_DB_PASSWORD, \
                                    MYSQL_DB_HOST, MYSQL_DB_DATABASE


class DatabaseConnection():
    # Source: https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html

    def __init__(self):
        self.connection = None

    def close(self):
        self.connection.close()
        # print('Database connection was successfully closed.')

    def connect(self):
        try:
            self.connection = connect(user=MYSQL_DB_USER, password=MYSQL_DB_PASSWORD,
                                      host=MYSQL_DB_HOST, database=MYSQL_DB_DATABASE)

            # print('Database was successfully connected.')
        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                # print("Something is wrong with your user name or password")
                print('Access was denied to your credentials.')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                # print("Database does not exist")
                print('Database does not exist.')
            else:
                # print(err)
                print('An error occurred during database connection: %s', err)

            self.close()
            print('Database connection was closed.')

    def execute(self, query, params=None):
        self.connect()
        cursor = self.connection.cursor()

        try:
            result = cursor.execute(query, params=params)
        except Error as err:
            print('An error occurred during query execution: %s', err)

        cursor.close()
        self.close()

        return result

    def select_user(self, username=None, password=None):
        # Sources:
        # https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html
        # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

        query = '''
            SELECT * FROM User
            WHERE username=%(username)s AND password=%(password)s
        '''

        params = { 'username': username, 'password': password }

        result = self.execute(query, params)

        print('dir result: %s', dir(result))
        print('query result: %s', result)
        # print('query result: ', result)

        if result.with_rows:
            rows = result.fetchall()
            print('rows: %s', rows)

        return result

    # def insert/update/delete_user(self, username=None, password=None):
    #     # example of how to insert/update/delete records
    #     # you must commit the data after a sequence of INSERT, DELETE, and UPDATE statements
    #     # Source: https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html

    #     self.connection.commit()
