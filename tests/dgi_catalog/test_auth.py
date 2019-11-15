"""
test_auth.py file
"""

from json import loads
from unittest import TestCase

from dgi_catalog import app as dgi_catalog_app


app = dgi_catalog_app.test_client()


class TestCatalogAuthLogin(TestCase):
    """TestCatalogAuthLogin"""

    url = '/catalog/auth/login'

    def test__post__catalog_auth_login__body_is_empty(self):
        """TestAuth.test__post__catalog_auth_login__body_is_empty"""

        response = app.post(self.url)

        body = loads(response.data.decode('utf-8'))

        self.assertEqual(400, response.status_code)
        self.assertEqual(body['message'], 'Body is empty.')

    # def test__post__catalog_auth_login__(self):
    #     """TestAuth.test_example"""

    #     response = app.post(self.url)

    #     body = loads(response.data.decode('utf-8'))

    #     self.assertEqual(400, response.status_code)
    #     self.assertEqual(body['message'], 'Body is empty.')
