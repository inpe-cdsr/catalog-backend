"""
business.py
"""

from werkzeug.exceptions import Forbidden

from dgi_catalog.model import DatabaseConnection
from dgi_catalog.environment import BASE_PATH
from dgi_catalog.log import logging


class DownloadBusiness():
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def get_image(self, username=None, password=None, path=None,
                        address=None, dataset=None, scene_id=None):
        logging.info('DownloadBusiness.get_image()')

        # logging.debug('DownloadBusiness.get_image() - username: %s', username)
        # logging.debug('DownloadBusiness.get_image() - password: %s', password)
        logging.info('DownloadBusiness.get_image() - path: %s', path)
        # logging.info('DownloadBusiness.get_image() - address: %s', address)
        logging.info('DownloadBusiness.get_image() - dataset: %s', dataset)
        logging.info('DownloadBusiness.get_image() - scene_id: %s', scene_id)

        # check if user exists in the database
        result = self.db_connection.select_user(
            email=username, password=password
        )

        # logging.debug('DownloadBusiness.get_image() - result: %s', result)

        if not result:
            raise Forbidden('E-mail or Password was not found.')

        # get file
        # e.g: path = /Repository/.../CBERS_4_MUX_20191022_154_126_L2.tif
        url = "{}/{}".format(BASE_PATH, path)

        logging.info('DownloadBusiness.get_image() - BASE_PATH: %s', BASE_PATH)
        logging.info('DownloadBusiness.get_image() - url: %s', url)

        # save statistics
        self.db_connection.insert_statistics(
            user_id=result[0]['userId'], scene_id=scene_id, path=url,
            ip=address.ip_address, country=address.country, region=address.region,
            latitude=address.latitude, longitude=address.longitude, dataset=dataset
        )

        # url = url if not BASE_PATH else '{}{}'.format(BASE_PATH, url)

        url_parts = url.split('/')

        # get the last element of the list, in other words, the filename
        filename = url_parts[len(url_parts)-1]

        # get just the directory, without the filename
        directory = url.replace('/{}'.format(filename), '')

        logging.info('DownloadBusiness.get_image() - url_parts: %s', url_parts)
        logging.info('DownloadBusiness.get_image() - filename: %s', filename)
        logging.info('DownloadBusiness.get_image() - directory: %s', directory)

        return directory, filename
