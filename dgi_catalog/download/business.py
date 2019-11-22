"""
business.py
"""

from werkzeug.exceptions import Forbidden

from dgi_catalog.model import DatabaseConnection

BASE = 'media'

class DownloadBusiness():
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def parse_path(self, path):
        infos = path.split('/')
        scene_id = infos[len(infos) - 1]
        url_path = "{}/{}".format(BASE, path)
        return scene_id, url_path

    def get_file(self, url_path):
        print(url_path)
        return b''

    def get_image(self, credentials, path, address):
        # validate credentials
        result = self.db_connection.select_user(
            email=credentials.username, password=credentials.password)
        if not result:
            raise Forbidden('E-mail or Password was not found.')

        # get file
        # e.g: path = /Repository/.../CBERS_4_MUX_20191022_154_126_L2.tif
        scene_id, url_path = self.parse_path(path)
        image = self.get_file(url_path)

        # save statistics
        self.db_connection.insert_statistics(
            result[0]['userId'], scene_id, url_path,
            address.ip_address, address.country, address.region,
            address.latitude, address.longitude)

        return image
        