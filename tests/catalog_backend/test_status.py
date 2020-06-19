#!/usr/bin/env python3

"""test_status.py test module"""

# from unittest import TestCase
# from json import loads

from catalog_backend import app as catalog_backend_app


catalog_backend_app.testing = True
app = catalog_backend_app.test_client()

URL = '/catalog/status/'

'''
class TestCatalogStatusSuccess(TestCase):
    """
    TestCatalogStatusSuccess
    """

    def test__get__catalog_status(self):
        """
        TestCatalogStatusSuccess.test__get__catalog_status
        """

        expected = '{"catalog_backend_version": version, "catalog_backend_provider": provider, \
        "base": "http://localhost:5000/catalog", \
        "description": "API - DGI Catalog (http://localhost:5000)"}'

        response = app.get(URL)

        body = loads(response.data.decode('utf-8'))

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, body)
'''
