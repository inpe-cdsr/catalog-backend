"""
Get environment variables
"""

from os import environ as os_environ

# enviroment
ENV = os_environ.get('ENV', 'debug')

# MYSQL connection
MYSQL_DB_USER = os_environ.get('MYSQL_DB_USER', 'test')
MYSQL_DB_PASSWORD = os_environ.get('MYSQL_DB_PASSWORD', 'test')
MYSQL_DB_HOST = os_environ.get('MYSQL_DB_HOST', 'localhost')
MYSQL_DB_DATABASE = os_environ.get('MYSQL_DB_DATABASE', 'database')

# JWT
JWT_SECRET = os_environ.get('JWT_SECRET', 'MY_SECRET')
JWT_ALGORITHM = os_environ.get('JWT_ALGORITHM', 'JWT_ALGORITHM')
