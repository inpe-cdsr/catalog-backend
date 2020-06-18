#!/usr/bin/env python3

"""CDSR IP module"""

from requests import get as requests_get


class CDSRIPException(Exception):
    """CDSRIPException class"""


class CDSRIP:
    """CDSRIP class"""

    @staticmethod
    def get_location(ip=None):
        """get_location method"""

        if ip is None or ip == "" or len(ip.split('.')) != 4:
            raise CDSRIPException('Invalid IP: `{}`'.format(ip))

        response = requests_get('http://ip-api.com/json/{}'.format(ip))

        if response.status_code != 200:
            raise CDSRIPException(
                'Invalid IP: `{}`. Status code: `{}`'.format(
                    ip, response.status_code
                )
            )

        response = response.json()

        if 'status' in response and response['status'] != 'success':
            raise CDSRIPException(
                'API has not been able to find the IP `{}`. Response: `{}`'
                .format(ip, response)
            )

        return {
            "ip": ip,
            "longitude": response['lon'],
            "latitude": response['lat'],
            "city": response['city'],
            "region": response['regionName'],
            "region_code": response['region'],
            "country": response['country'],
            "country_code": response['countryCode'],
            "zip_code": response['zip'],
            "time_zone": response['timezone'],
            "isp_name": response['isp'],
            "org_name": response['org'],
            "as": response['as']
        }

# from cdsr_ip import CDSRIP
# CDSRIP.get_location('189.29.126.49')
