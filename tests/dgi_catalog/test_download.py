# pylint: disable-msg=C0103
# from werkzeug.exceptions import BadRequest

from unittest import TestCase
# from json import loads, dumps

from dgi_catalog import app as dgi_catalog_app


app = dgi_catalog_app.test_client()


# class TestCatalogDownload(TestCase):
#     # def setUp(self):
#     #     self.response = app.get('/wtss/list_coverages')

#     def test_example(self):
#         # response = app.get('/wtss/list_coverages')
#         # print('\n\n>>> response: ', response, "\n\n")
#         self.assertEqual(10, 10)
