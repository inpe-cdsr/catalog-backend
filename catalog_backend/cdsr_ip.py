#!/usr/bin/env python3

"""CDSR IP module"""

from requests import get as requests_get


# Exception messages
EXC_MSG_INVALID_IP = 'Invalid IP: `{}`'
EXC_MSG_STATUS_CODE_IS_NOT_200 = 'Invalid IP: `{}`. Status code: `{}`'
EXC_MSG_STATUS_IS_NOT_SUCCESS = 'API has not been able to find the IP `{}`. Response: `{}`'


class CDSRIPException(Exception):
    """CDSRIPException class"""


class CDSRIP:
    """CDSRIP class"""

    fields = 'status,message,lon,lat,city,district,regionName,region,' + \
             'country,countryCode,continent,continentCode,zip,timezone'

    @staticmethod
    def get_location_structure(ip=None):
        """get_location_structure method"""

        return {
            "ip": ip,
            "longitude": None,
            "latitude": None,
            "city": None,
            "district": None,
            "region": None,
            "region_code": None,
            "country": None,
            "country_code": None,
            "continent": None,
            "continent_code": None,
            "zip_code": None,
            "time_zone": None
        }

    @staticmethod
    def get_location(ip=None):
        """get_location method"""

        if ip is None or ip == "" or len(ip.split('.')) != 4:
            raise CDSRIPException(EXC_MSG_INVALID_IP.format(ip))

        response = requests_get('http://ip-api.com/json/{}?fields={}'.format(ip, CDSRIP.fields))

        if response.status_code != 200:
            raise CDSRIPException(EXC_MSG_STATUS_CODE_IS_NOT_200.format(ip, response.status_code))

        response = response.json()

        if 'status' in response and response['status'] != 'success':
            raise CDSRIPException(EXC_MSG_STATUS_IS_NOT_SUCCESS.format(ip, response))

        return {
            "ip": ip,
            "longitude": response['lon'],
            "latitude": response['lat'],
            "city": response['city'],
            "district": response['district'],
            "region": response['regionName'],
            "region_code": response['region'],
            "country": response['country'],
            "country_code": response['countryCode'],
            "continent": response['continent'],
            "continent_code": response['continentCode'],
            "zip_code": response['zip'],
            "time_zone": response['timezone']
        }
