#!/usr/bin/env python3

"""test_cdsr_ip.py test module"""

from unittest import TestCase

from catalog_backend.cdsr_ip import CDSRIP, CDSRIPException, \
                                    EXC_MSG_INVALID_IP, EXC_MSG_STATUS_IS_NOT_SUCCESS


class TestCDSRIP(TestCase):
    """TestCDSRIP"""

    def test__get_location__success(self):
        """TestCDSRIP.test__get_location__success"""

        expected = {
            "ip": "8.8.8.8",
            "longitude": -77.5,
            "latitude": 39.03,
            "city": "Ashburn",
            "district": "",
            "region": "Virginia",
            "region_code": "VA",
            "country": "United States",
            "country_code": "US",
            "continent": "North America",
            "continent_code": "NA",
            "zip_code": "20149",
            "time_zone": "America/New_York"
        }

        location = CDSRIP.get_location(expected['ip'])

        self.assertEqual(expected, location)


class TestCDSRIPError(TestCase):
    """TestCDSRIPError"""

    def test__get_location__error__invalid_ip(self):
        """TestCDSRIPError.test__get_location__error"""

        expected = {
            "ip": "8.8.8.8.8",
            "longitude": 0,
            "latitude": 0,
            "city": "",
            "district": "",
            "region": "",
            "region_code": "",
            "country": "",
            "country_code": "",
            "continent": "",
            "continent_code": "",
            "zip_code": "",
            "time_zone": ""
        }

        self.assertRaises(CDSRIPException, CDSRIP.get_location, expected['ip'])
        self.assertRaisesRegex(CDSRIPException, EXC_MSG_INVALID_IP.format(expected['ip']),
                               CDSRIP.get_location, expected['ip'])

    def test__get_location__error__status_is_not_success(self):
        """TestCDSRIPError.test__get_location__error"""

        expected = {
            "ip": "127.0.0.1",
            "longitude": 0,
            "latitude": 0,
            "city": "",
            "district": "",
            "region": "",
            "region_code": "",
            "country": "",
            "country_code": "",
            "continent": "",
            "continent_code": "",
            "zip_code": "",
            "time_zone": ""
        }

        self.assertRaises(CDSRIPException, CDSRIP.get_location, expected['ip'])
        self.assertRaisesRegex(
            CDSRIPException,
            EXC_MSG_STATUS_IS_NOT_SUCCESS.format(
                expected['ip'], "{'status': 'fail', 'message': 'reserved range'}"
            ),
            CDSRIP.get_location, expected['ip']
        )
