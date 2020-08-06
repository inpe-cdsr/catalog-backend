"""Get environment variables"""

from os import environ as os_environ


TEST_USER_EMAIL = os_environ.get('TEST_USER_EMAIL', 'test@localhost.com')
TEST_USER_PASSWORD = os_environ.get('TEST_USER_PASSWORD', 'test')
TEST_VALID_EMAIL_TO_SEND = os_environ.get('TEST_VALID_EMAIL_TO_SEND', 'test@localhost.com')
