# pylint: disable-msg=C0103
# from werkzeug.exceptions import BadRequest

from unittest import TestCase

from dgi_catalog import app as dgi_catalog_app


app = dgi_catalog_app.test_client()

URL = '/catalog/status'


'''
class TestCatalogStatusSuccess(TestCase):
    """
    TestCatalogStatusSuccess
    """

    def test__get__catalog_status(self):
        """
        TestCatalogStatusSuccess
        """

        # response = app.get('/wtss/list_coverages')
        # print('\n\n>>> response: ', response, "\n\n")
        self.assertEqual(10, 10)
'''
