"""
Get environment variables
"""

from os import environ as os_environ

TEST_USER_EMAIL = os_environ.get('TEST_USER_EMAIL', 'test@localhost.com')
TEST_USER_PASSWORD = os_environ.get('TEST_USER_PASSWORD', 'test')
