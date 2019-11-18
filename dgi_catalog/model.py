"""
DGI Catalog
"""

from mysql.connector import connect, errorcode, Error
from datetime import date, datetime

from dgi_catalog.environment import MYSQL_DB_USER, MYSQL_DB_PASSWORD, \
                                    MYSQL_DB_HOST, MYSQL_DB_DATABASE

def fix_rows(rows):
    for row in rows:
        for key in row:
            # datetime/date is not serializable by default, then get a serializable string representation
            if isinstance(row[key], (datetime, date)):
                row[key] = row[key].isoformat()

    return rows

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
        cursor = self.connection.cursor(dictionary=True)

        result = None

        try:
            cursor.execute(query, params=params)

            # if there are rows, then return them
            if cursor.with_rows:
                result = cursor.fetchall()

        except Error as err:
            print('An error occurred during query execution: %s', err)

        cursor.close()
        self.close()

        return result

    def select_user(self, email=None, password=None):
        # Sources:
        # https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html
        # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

        query = '''
            SELECT * FROM User
            WHERE email=%(email)s AND password=%(password)s
        '''

        params = { 'email': email, 'password': password }

        # execute the query and fix the resulted rows
        rows = self.execute(query, params)
        rows = fix_rows(rows)

        return rows

    # def insert/update/delete_user(self, username=None, password=None):
    #     # example of how to insert/update/delete records
    #     # you must commit the data after a sequence of INSERT, DELETE, and UPDATE statements
    #     # Source: https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html

    #     self.connection.commit()
