# pylint: disable-msg=C0103
from werkzeug.exceptions import BadRequest

from dgi_catalog import app as dgi_catalog_app
# from bdc_wtss.schemas import coverage_list_response, \
#                              describe_coverage_response, \
#                              time_series_response

# from json import loads as json_loads
# from jsonschema import validate

from unittest import TestCase


app = dgi_catalog_app.test_client()


class TestExample(TestCase):
    # def setUp(self):
    #     self.response = app.get('/wtss/list_coverages')

    def test_example(self):
        # response = app.get('/wtss/list_coverages')
        # print('\n\n>>> response: ', response, "\n\n")
        self.assertEqual(10, 10)

"""
class TestListCoverage(unittest.TestCase):
    def setUp(self):
        self.response = app.get('/wtss/list_coverages')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_response_format_with_json_schema(self):
        self.assertEqual(self.response.content_type, 'application/json')

        coverage_response = json_loads(self.response.data.decode('utf-8'))

        validate(instance=coverage_response, schema=coverage_list_response)


class TestDescribeCoverage(unittest.TestCase):
    def test_get_without_required_parameters(self):
        resp = app.get('/wtss/describe_coverage')
        self.assertEqual(400, resp.status_code)
        self.assertEqual(resp.content_type, 'application/json')

        coverage_response = json_loads(resp.data.decode('utf-8'))

        self.assertEqual(400, coverage_response['code'])
        self.assertEqual("'name' is a required property", coverage_response['message'])

    def test_get_with_required_parameters(self):
        resp = app.get('/wtss/describe_coverage?name=C64m:MEDIAN')

        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.content_type, 'application/json')

    def test_get_response_validate_json_schema(self):
        resp = app.get('/wtss/describe_coverage?name=C64m:MEDIAN')

        coverage_response = json_loads(resp.data.decode('utf-8'))

        validate(instance=coverage_response, schema=describe_coverage_response)

    def test_coverage_not_found(self):
        resp = app.get('/wtss/describe_coverage?name=notfoundcoverage')

        self.assertEqual(404, resp.status_code)

        coverage_response = json_loads(resp.data.decode('utf-8'))

        self.assertEqual(coverage_response['message'], 'Coverage "notfoundcoverage" not found')


class TestTimeSeries(unittest.TestCase):
    @staticmethod
    def make_request(**properties):
        '''
        Builds Flask Request object with properties values which generates query string args
        :param properties: Properties to pass to time series request. Each parameter represents query string args
        :return:
        '''
        query_string = ""

        if len(properties.keys()) > 0:
            query_string = "?" + "&".join(['{}={}'.format(key, value) for (key, value) in properties.items()])

        return app.get('/wtss/time_series{}'.format(query_string))

    def invalid_request(self, **properties):
        '''
        Helper to validate error request of WTSS Time Series Service

        It already validates resp message code. **You must validate message code**

        :param properties: Properties to pass to time series request. Each parameter represents query string args
        :return: Tuple with Flask Response object and parsed JSON response data
        '''
        resp = TestTimeSeries.make_request(**properties)

        self.assertEqual(400, resp.status_code)
        self.assertEqual(resp.content_type, 'application/json')
        coverage_response = json_loads(resp.data.decode('utf-8'))
        self.assertEqual(400, coverage_response['code'])

        return resp, coverage_response

    def test_get_without_coverage(self):
        resp = TestTimeSeries.make_request()

        self.assertEqual(400, resp.status_code)
        self.assertEqual(resp.content_type, 'application/json')

        coverage_response = json_loads(resp.data.decode('utf-8'))

        self.assertEqual(400, coverage_response['code'])

    def test_get_without_bbox(self):
        resp, data = self.invalid_request(
            coverage='fake_coverage',
            start_date='2018-01-01',
            attributes='nir,nvdi'
        )

        self.assertEqual("'latitude' is a required property", data['message'])

        resp, data = self.invalid_request(
            coverage='fake_cube',
            start_date='2018-01-01',
            attributes='nir,nvdi',
            latitude=-12.5
        )
        self.assertEqual("'longitude' is a required property", data['message'])

    def test_lat_long_not_in_bbox(self):
        resp, data = self.invalid_request(
            coverage='C64m:MEDIAN',
            start_date='2018',  # 2018-01-01
            end_date='2018',  # 2018-12-31
            attributes='nir,nvdi',
            latitude=-90,
            longitude=-120
        )

        self.assertEqual(data['message'], 'No features found')

    def test_get_time_series_json_schema(self):
        resp = TestTimeSeries.make_request(
            coverage="C64m:MEDIAN",
            start_date='2018-01-01',
            end_date='2019-01-01',
            attributes='nir,ndvi',
            latitude=-15,
            longitude=-53
        )

        self.assertEqual(200, resp.status_code)

        time_series_result = json_loads(resp.data.decode('utf-8'))

        validate(instance=time_series_result, schema=time_series_response)

        timeline_size = len(time_series_result['result']['timeline'])

        for attr in time_series_result['result']['attributes']:
            self.assertEqual(timeline_size, len(attr['values']))
"""