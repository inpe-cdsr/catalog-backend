"""business.py"""

'''
from flask import request
from werkzeug.exceptions import Forbidden

from catalog_backend.cdsr_ip import CDSRIP, CDSRIPException
from catalog_backend.model import DatabaseConnection
from catalog_backend.log import logging


class NonceBusiness():
    """NonceBusiness class"""

    def __init__(self):
        self.db_connection = DatabaseConnection()

    @staticmethod
    def create_nonce():
        """create_nonce method"""
        return 'abc'

    def insert_nonce(self, email=None, nonce=None):
        """It inserts the nonce in the database"""

        logging.info('NonceBusiness.insert_nonce()\n')

        logging.debug('DownloadBusiness.insert_statistics() - username: %s', username)
        # logging.debug('DownloadBusiness.insert_statistics() - password: %s', password)
        logging.info('DownloadBusiness.insert_statistics() - urn: %s', urn)
        logging.info('DownloadBusiness.insert_statistics() - scene_id: %s', scene_id)
        logging.info('DownloadBusiness.insert_statistics() - kwards: %s', kwards)

        # check if user exists in the database
        user = self.db_connection.select_user(
            email=username, password=password
        )

        # logging.debug('DownloadBusiness.insert_statistics() - result: %s', result)

        if not user:
            raise Forbidden('E-mail or Password was not found.')

        location = self.get_location(ips_list)

        logging.info('Download.insert_statistics() - location: %s', location)

        # I search if the chose location has already been added in the database
        result = self.select_location(location['ip'])

        logging.info('Download.insert_statistics() - result: %s', result)

        # if the location has not been added in the database, then I insert it once
        if not result:
            # save the new location
            self.db_connection.insert_location(**location)

            logging.info(
                'DownloadBusiness.insert_statistics() - location has been inserted successfully!'
            )

        # save the statistics
        self.db_connection.insert_statistics(
            user_id=user[0]['userId'], scene_id=scene_id, path=urn, ip=location['ip']
        )

        logging.info(
            'DownloadBusiness.insert_statistics() - statistics have been inserted successfully!'
        )
'''
