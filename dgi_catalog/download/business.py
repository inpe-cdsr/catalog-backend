"""
business.py
"""
from werkzeug.exceptions import Forbidden

from dgi_catalog.model import DatabaseConnection
from dgi_catalog.environment import BASE_PATH

class DownloadBusiness():
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def parse_path(self, path):
        infos = path.split('/')
        scene_id = infos[len(infos) - 1]
        url_path = "{}/{}".format(BASE_PATH, path)
        return scene_id, url_path

    def get_image(self, username, password, path, address):
        # validate credentials
        result = self.db_connection.select_user(
            email=username, password=password)
        if not result:
            raise Forbidden('E-mail or Password was not found.')

        # get file
        # e.g: path = /Repository/.../CBERS_4_MUX_20191022_154_126_L2.tif
        scene_id, url_path = self.parse_path(path)

        # save statistics
        self.db_connection.insert_statistics(
            result[0]['userId'], scene_id, url_path,
            address.ip_address, address.country, address.region,
            address.latitude, address.longitude)

        url = url_path if not BASE_PATH else '{}{}'.format(BASE_PATH, url_path)
        url_parts = url.split('/')
        file_name = url_parts[len(url_parts)-1]
        return url.replace('/{}'.format(file_name), ''), file_name
        