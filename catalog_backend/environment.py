#!/usr/bin/env python3

"""Get environment variables"""

from os import environ
from logging import DEBUG, INFO


os_environ_get = environ.get


FLASK_ENV = os_environ_get('FLASK_ENV', 'production')

SERVER_HOST = os_environ_get('SERVER_HOST', '0.0.0.0')

try:
    SERVER_PORT = int(os_environ_get('SERVER_PORT', '5000'))
except ValueError:
    SERVER_PORT = 5000

# default logging level in production server
LOGGING_LEVEL = INFO
# default debug mode in production server
DEBUG_MODE = False

# if the application is in development mode, then change the logging level and debug mode
if FLASK_ENV == 'development':
    LOGGING_LEVEL = DEBUG
    DEBUG_MODE = True

# enviroment
ENV = os_environ_get('ENV', 'debug')

# MYSQL connection
MYSQL_DB_USER = os_environ_get('MYSQL_DB_USER', 'test')
MYSQL_DB_PASSWORD = os_environ_get('MYSQL_DB_PASSWORD', 'test')
MYSQL_DB_HOST = os_environ_get('MYSQL_DB_HOST', 'localhost')
MYSQL_DB_PORT = os_environ_get('MYSQL_DB_PORT', '3306')
MYSQL_DB_DATABASE = os_environ_get('MYSQL_DB_DATABASE', 'database')

# JWT
JWT_SECRET = os_environ_get('JWT_SECRET', 'MY_SECRET')
JWT_ALGORITHM = os_environ_get('JWT_ALGORITHM', 'JWT_ALGORITHM')

# URLs
URL_DOWNLOAD = os_environ_get('URL_DOWNLOAD', 'http://localhost:8089/datastore')
URL_CATALOG_RESET_PASSWORD = os_environ_get(
    'URL_CATALOG_RESET_PASSWORD', 'http://localhost:8089/catalog/reset-password'
)

# e-mail sender
EMAIL_SENDER_FROM = os_environ_get('EMAIL_SENDER_FROM', None)
EMAIL_SENDER_FROM_PASSWORD = os_environ_get('EMAIL_SENDER_FROM_PASSWORD', None)
EMAIL_SMTP_HOST = os_environ_get('EMAIL_SMTP_HOST', 'smtp.gmail.com')
EMAIL_SMTP_PORT = os_environ_get('EMAIL_SMTP_PORT', 587)

# other
BASE_PATH = os_environ_get('BASE_PATH', '')
