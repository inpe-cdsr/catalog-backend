"""business.py"""

from werkzeug.exceptions import Forbidden

from catalog_backend.model import DatabaseConnection
from catalog_backend.log import logging


class DownloadBusiness():
    """DownloadBusiness class"""

    def __init__(self):
        self.db_connection = DatabaseConnection()

    def select_location(self, ip):
        return self.db_connection.select_location(ip)

    def insert_statistics(self, username=None, password=None, urn=None,
                          location=None, scene_id=None, **kwards):
        """It inserts statistics in the database"""

        logging.info('DownloadBusiness.insert_statistics()')

        logging.debug('DownloadBusiness.insert_statistics() - username: %s', username)
        # logging.debug('DownloadBusiness.insert_statistics() - password: %s', password)
        logging.info('DownloadBusiness.insert_statistics() - urn: %s', urn)
        logging.info('DownloadBusiness.insert_statistics() - scene_id: %s', scene_id)
        logging.info('DownloadBusiness.insert_statistics() - kwards: %s', kwards)

        # check if user exists in the database
        result = self.db_connection.select_user(
            email=username, password=password
        )

        # logging.debug('DownloadBusiness.insert_statistics() - result: %s', result)

        if not result:
            raise Forbidden('E-mail or Password was not found.')

        # save the new location
        self.db_connection.insert_location(**location)

        logging.info('DownloadBusiness.insert_statistics() - location has been inserted successfully!')

        # save the statistics
        self.db_connection.insert_statistics(
            user_id=result[0]['userId'], scene_id=scene_id, path=urn, ip=location['ip']
        )

        logging.info('DownloadBusiness.insert_statistics() - statistics have been inserted successfully!')
