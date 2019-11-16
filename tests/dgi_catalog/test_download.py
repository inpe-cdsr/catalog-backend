# pylint: disable-msg=C0103
# from werkzeug.exceptions import BadRequest

from dgi_catalog import app as dgi_catalog_app
# from bdc_wtss.schemas import coverage_list_response, \
#                              describe_coverage_response, \
#                              time_series_response

# from json import loads as json_loads
# from jsonschema import validate

from unittest import TestCase


app = dgi_catalog_app.test_client()


# class TestCatalogDownload(TestCase):
#     # def setUp(self):
#     #     self.response = app.get('/wtss/list_coverages')

#     def test_example(self):
#         # response = app.get('/wtss/list_coverages')
#         # print('\n\n>>> response: ', response, "\n\n")
#         self.assertEqual(10, 10)
