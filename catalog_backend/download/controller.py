#!/usr/bin/env python3
# disable pylint(line-too-long) (All codes: http://pylint-messages.wikidot.com/all-codes)
# pylint: disable=C0301

"""Controllers"""

from flask import request, redirect
from flask_restplus import Resource as APIResource
from werkzeug.exceptions import Unauthorized

from catalog_backend.download import ns
from catalog_backend.download.business import DownloadBusiness
from catalog_backend.environment import URL_DOWNLOAD, BASE_PATH
from catalog_backend.log import logging


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
        logging.info('Download.get() - request.remote_addr: %s', request.remote_addr)

        ips_string = request.headers.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

        logging.info('Download.get() - ips_string: %s', ips_string)

        ips_list = [ip.strip() for ip in ips_string.split(',')]

        # logging.debug('Download.get() - request.authorization: %s', request.authorization)
        # logging.debug('Download.get() - request.args: %s', request.args)

        # Nginx credentials
        # if request.authorization:
        #     credentials = request.authorization
        #     username = credentials.username
        #     password = credentials.password
        # Url credentials
        if request.args.get('key'):
            credentials = request.args['key'].split(':')
            username = credentials[0]
            password = credentials[1]
        else:
            raise Unauthorized('Credentials are required!')

        logging.info('DownloadBusiness.get() - BASE_PATH: %s', BASE_PATH)

        # get the path to the file
        # e.g: url = '/data/TIFF/.../CBERS_4_MUX_20191022_154_126_L2.tif'
        urn = "{}/{}".format(BASE_PATH, path)

        parameters = {
            'urn': urn,
            'ips_list': ips_list,
            'dataset': request.args.get('collection'),
            'scene_id': request.args.get('scene_id')
        }

        # do not print username and password
        logging.debug('Download.get() - parameters: %s', parameters)

        parameters['username'] = username
        parameters['password'] = password

        self.download_business.insert_statistics(**parameters)

        uri = URL_DOWNLOAD + urn

        logging.debug('Download.get() - uri: %s', uri)

        return redirect(uri)
