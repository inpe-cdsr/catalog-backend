"""
test_auth.py file
"""

from json import loads
from unittest import TestCase

from dgi_catalog import app as dgi_catalog_app


app = dgi_catalog_app.test_client()


class TestAuth(TestCase):
    """TestAuth"""

    # def setUp(self):
    #     self.response = app.get('/wtss/list_coverages')

    def test_post__catalog_auth_login__body_is_empty(self):
        """TestAuth.test_example"""

        response = app.post('/catalog/auth/login')

        body = loads(response.data.decode('utf-8'))

        self.assertEqual(400, response.status_code)
        self.assertEqual(body['message'], 'Body is empty.')
