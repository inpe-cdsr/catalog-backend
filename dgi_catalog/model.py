"""
DGI Catalog
"""

from mysql.connector import connect, errorcode, Error

from dgi_catalog import logger
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
            # logger.info('Database was successfully connected.')
        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                # print("Something is wrong with your user name or password")
                logger.error('Access was denied to your credentials.')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                # print("Database does not exist")
                logger.error('Database does not exist.')
            else:
                # print(err)
                logger.error('An error occurred during database connection: %s', err)

            self.close()
            # print('Database connection was closed.')
            logger.warning('Database connection was closed.')

    def execute(self, query):
        self.connect()
        cursor = self.connection.cursor()

        try:
            result = cursor.execute(query)
        except Error as err:
            # print('execute error: ', err)
            logger.error('An error occurred during query execution: %s', err)

        cursor.close()
        self.close()

        return result

    def select_user(self, username=None, password=None):
        query = '''
            SELECT * FROM User
            WHERE username={0} AND password={1}
        '''

        result = self.execute(query)
        logger.info('query result: %s', result)
        # print('query result: ', result)

        return result
