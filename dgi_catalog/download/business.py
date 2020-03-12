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

    def insert_statistics(self, username=None, password=None, urn=None,
                          location=None, dataset=None, scene_id=None):
        """It inserts statitics in the database"""
        logging.info('DownloadBusiness.get_image()')

        # logging.debug('DownloadBusiness.get_image() - username: %s', username)
        # logging.debug('DownloadBusiness.get_image() - password: %s', password)
        logging.info('DownloadBusiness.get_image() - urn: %s', urn)
        # logging.info('DownloadBusiness.get_image() - location: %s', location)
        logging.info('DownloadBusiness.get_image() - dataset: %s', dataset)
        logging.info('DownloadBusiness.get_image() - scene_id: %s', scene_id)

        # check if user exists in the database
        result = self.db_connection.select_user(
            email=username, password=password
        )

        # logging.debug('DownloadBusiness.get_image() - result: %s', result)

        if not result:
            raise Forbidden('E-mail or Password was not found.')

        # save statistics
        self.db_connection.insert_statistics(
            user_id=result[0]['userId'], scene_id=scene_id, path=urn,
            ip=location.ip_address, country=location.country, region=location.region,
            latitude=location.latitude, longitude=location.longitude, dataset=dataset
        )
