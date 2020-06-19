"""business.py"""

from werkzeug.exceptions import Forbidden

from catalog_backend.model import DatabaseConnection
from catalog_backend.log import logging


class DownloadBusiness():
    """DownloadBusiness class"""

    def __init__(self):
        self.db_connection = DatabaseConnection()

    def insert_statistics(self, username=None, password=None, urn=None,
                          location=None, scene_id=None, **kwards):
        """It inserts statitics in the database"""
        logging.info('DownloadBusiness.get_image()')

        logging.debug('DownloadBusiness.get_image() - username: %s', username)
        # logging.debug('DownloadBusiness.get_image() - password: %s', password)
        logging.info('DownloadBusiness.get_image() - urn: %s', urn)
        logging.info('DownloadBusiness.get_image() - scene_id: %s', scene_id)
        logging.info('DownloadBusiness.get_image() - kwards: %s', kwards)

        # check if user exists in the database
        result = self.db_connection.select_user(
            email=username, password=password
        )

        # logging.debug('DownloadBusiness.get_image() - result: %s', result)

        if not result:
            raise Forbidden('E-mail or Password was not found.')

        # save the statistics
        self.db_connection.insert_statistics(
            user_id=result[0]['userId'], scene_id=scene_id, path=urn, **location
        )
