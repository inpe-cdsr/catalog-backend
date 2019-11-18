"""
Get environment variables
"""

from os import environ as os_environ

TEST_USER_EMAIL = os_environ.get('TEST_USER_EMAIL', 'MY_EMAIL')
TEST_USER_PASSWORD = os_environ.get('TEST_USER_PASSWORD', 'MY_PASSWORD')
