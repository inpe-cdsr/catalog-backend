"""
DGI Catalog
"""

from os import environ as os_environ

# get environment variables
ENV = os_environ.get('ENV', 'development')
MYSQL_DB_USER = os_environ.get('MYSQL_DB_USER', 'test')
MYSQL_DB_PASSWORD = os_environ.get('MYSQL_DB_PASSWORD', 'test')
MYSQL_DB_HOST = os_environ.get('MYSQL_DB_HOST', 'localhost')
MYSQL_DB_DATABASE = os_environ.get('MYSQL_DB_DATABASE', 'test')
