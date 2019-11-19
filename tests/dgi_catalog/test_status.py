# disable pylint(line-too-long) (All codes: http://pylint-messages.wikidot.com/all-codes)
# pylint: disable=C0301
# pylint: disable-msg=C0103

from unittest import TestCase
# from json import loads, dumps

from dgi_catalog import app as dgi_catalog_app


app = dgi_catalog_app.test_client()

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

        expected = '{"dgi_catalog_version": version, "dgi_catalog_provider": provider, \
        "base": "http://localhost:5000/catalog", \
        "description": "API - DGI Catalog (http://localhost:5000)"}'

        response = app.get(URL)

        body = loads(response.data.decode('utf-8'))

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, body)
'''
