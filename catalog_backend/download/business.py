#!/usr/bin/env python3

"""business.py"""

from json import loads

from flask import request
from werkzeug.exceptions import BadRequest, Forbidden

from catalog_backend.cdsr_ip import CDSRIP, CDSRIPException
from catalog_backend.model import DatabaseConnection
from catalog_backend.log import logging


class DownloadBusiness():
    """DownloadBusiness class"""

    def __init__(self):
        self.db_connection = DatabaseConnection()

    def select_location(self, ip):
        return self.db_connection.select_location(ip)

    def get_location(self, ips_list):
        """
        Method to get the client's location

        return:
            location (dict): location information
        """

        logging.info('DownloadBusiness.get_location()')
        logging.info('DownloadBusiness.get_location() - ips_list: %s', ips_list)

        for ip in ips_list:
            logging.info('DownloadBusiness.get_location() - ip: %s', ip)

            # check if the IP exists inside the database in order to save requests
            location = self.select_location(ip)

            logging.info('DownloadBusiness.get_location() - location: %s', location)

            # if the location has already been added to the database, then I return it, [...]
            if location:
                return location[0]

            # [...] else I search the location by IP once
            try:
                # try to get the location based with a public IP
                location = CDSRIP.get_location(ip)

                logging.info('DownloadBusiness.get_location() - public IP was found: %s', ip)

                return location
            except (CDSRIPException, KeyError):
                # if an exception occurs, a public IP was not found, then try again with another IP
                continue

        logging.info(
            'DownloadBusiness.get_location() - public IP was not found,'
            f' then private IP was chose: {request.remote_addr}'
        )

        # if there is not one public IP, return a location object based on public IP,
        # in other words, there is not any location information
        return CDSRIP.get_location_structure(request.remote_addr)

    def insert_statistics(self, email=None, item_id=None, collection=None, urn=None,
                          ips_list=None, **kwards):
        """Inserts statistics in the database"""

        logging.info('DownloadBusiness.insert_statistics()')

        logging.info('DownloadBusiness.insert_statistics() - email: %s', email)
        logging.info('DownloadBusiness.insert_statistics() - item_id: %s', item_id)
        logging.info('DownloadBusiness.insert_statistics() - collection: %s', collection)
        logging.info('DownloadBusiness.insert_statistics() - urn: %s', urn)
        logging.info('DownloadBusiness.insert_statistics() - ips_list: %s', ips_list)
        logging.info('DownloadBusiness.insert_statistics() - kwards: %s', kwards)

        # check if user exists in the database
        user = self.db_connection.select_user(email=email)

        # logging.debug('DownloadBusiness.insert_statistics() - user: %s', user)

        if not user:
            raise Forbidden('Invalid e-mail.')

        # check if item exists in the database
        item = self.db_connection.select_item(item_id=item_id, collection=collection)

        logging.debug(f'DownloadBusiness.insert_statistics() - item: {item}')

        if not item:
            raise BadRequest('Invalid `item_id` or `collection` parameters.')

        # get the list of assets from item
        assets = loads(item[0]['assets'])
        # check if the path is a valid asset
        assets = list(filter(lambda asset: asset['href'] == urn.replace('.xml', '.tif'), assets))

        logging.info(f'DownloadBusiness.insert_statistics() - assets: {assets}')

        if not assets:
            raise BadRequest('Invalid asset.')

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
            user_id=user[0]['userId'], scene_id=item_id, dataset=collection,
            path=urn, ip=location['ip']
        )

        logging.info(
            'DownloadBusiness.insert_statistics() - statistics have been inserted successfully!'
        )
