# disable pylint(line-too-long) (All codes: http://pylint-messages.wikidot.com/all-codes)
# pylint: disable=C0301

"""
Controllers
"""

from flask import request, send_from_directory
from bdc_core.utils.flask import APIResource

from ip2geotools.databases.noncommercial import DbIpCity
from ip2geotools.models import IpLocation

from werkzeug.exceptions import Unauthorized

from dgi_catalog.download import ns
from dgi_catalog.download.business import DownloadBusiness
from dgi_catalog.log import logging


api = ns


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

        try:
            ip = request.headers.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

            logging.info('Download.get() - ip: %s', ip)

            address = DbIpCity.get(ip, api_key='free')
        except Exception:
            address = IpLocation(request.remote_addr)

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
            'address': address,
            'collection': request.args.get('collection'),
            'scene_id': request.args.get('scene_id')
        }

        logging.debug('Download.get() - parameters: %s', parameters)

        parameters['username'] = username
        parameters['password'] = password

        path_image, file_name = self.download_business.get_image(**parameters)

        logging.info('Download.get() - path_image: %s', path_image)
        logging.info('Download.get() - file_name: %s', file_name)

        return send_from_directory(path_image, file_name)
