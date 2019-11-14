"""
import mysql.connector
from mysql.connector import errorcode

try:
    cnx = mysql.connector.connect(user='', password='',
                                  host='',
                                  database='')

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()

Source: https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
"""


class AuthBusiness():

    @classmethod
    def login(cls, username, password):
        print('username: ', username)
        print('password: ', password)

        return True
