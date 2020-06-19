# pylint: disable-msg=C0103
# from werkzeug.exceptions import BadRequest

from unittest import TestCase

from catalog_backend import app as catalog_backend_app


catalog_backend_app.testing = True
app = catalog_backend_app.test_client()

'''
class TestCatalogDownload(TestCase):
    # def setUp(self):
    #     self.response = app.get('/wtss/list_coverages')

    def test_example(self):
        # response = app.get('/wtss/list_coverages')
        # print('\n\n>>> response: ', response, "\n\n")
        self.assertEqual(10, 10)
'''
