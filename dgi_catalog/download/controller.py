# disable pylint(line-too-long) (All codes: http://pylint-messages.wikidot.com/all-codes)
# pylint: disable=C0301

"""
Controllers
"""

from flask import request, send_from_directory
from bdc_core.utils.flask import APIResource
from werkzeug.exceptions import Unauthorized

from ip2geotools.databases.noncommercial import DbIpCity
from ip2geotools.models import IpLocation
from ip2geotools.errors import InvalidRequestError

from dgi_catalog.download import ns
from dgi_catalog.download.business import DownloadBusiness
from dgi_catalog.log import logging


api = ns


def get_location(ips_list):
    """
    Function to get the client's location
    """
    logging.info('Download.get_location()')
    logging.info('Download.get_location() - ips_list: %s', ips_list)

    for ip in ips_list:
        logging.info('Download.get_location() - ip: %s', ip)

        try:
            # try to get the location based with a public IP
            location = DbIpCity.get(ip, api_key='free')

            logging.info('Download.get_location() - public IP was found.')

            return location
        except (InvalidRequestError, KeyError):
            # if an exception occurs, a public IP was not found, then try again with another IP
            continue

    logging.info('Download.get_location() - public IP was not found, then private IP was chose.')

    # if there is not one public IP, return a location object based on public IP, in other words, there is not any location information
    return IpLocation(request.remote_addr)


@api.route('/<path:path>')
class Download(APIResource):
    """
    Download
    Full route: /api/download/<path>
    """
    download_business = DownloadBusiness()

    def get(self, path):
        """
        Returns
        -------
        image/tif
        """
        logging.info('Download.get()')

        logging.info('Download.get() - path: %s', path)

        logging.info('Download.get() - request.remote_addr: %s', request.remote_addr)

        ip = request.headers.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

        logging.info('Download.get() - ip: %s', ip)

        ips_list = ip.split(',')

        location = get_location(ips_list)

        # logging.debug('Download.get() - request.authorization: %s', request.authorization)
        # logging.debug('Download.get() - request.args: %s', request.args)

        if request.authorization:
            credentials = request.authorization
            username = credentials.username
            password = credentials.password
        elif request.args.get('key'):
            credentials = request.args['key'].split(':')
            username = credentials[0]
            password = credentials[1]
        else:
            raise Unauthorized('Credentials are required!')

        parameters = {
            'path': path,
            'location': location,
            'dataset': request.args.get('collection'),
            'scene_id': request.args.get('scene_id')
        }

        # do not print username and password
        logging.debug('Download.get() - parameters: %s', parameters)

        parameters['username'] = username
        parameters['password'] = password

        directory, filename = self.download_business.get_image(**parameters)

        return send_from_directory(directory, filename)
