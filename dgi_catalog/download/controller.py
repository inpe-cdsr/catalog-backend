# disable pylint(line-too-long) (All codes: http://pylint-messages.wikidot.com/all-codes)
# pylint: disable=C0301

"""
Controllers
"""

from flask import request, send_from_directory
from bdc_core.utils.flask import APIResource

from dgi_catalog.download import ns
from dgi_catalog.download.business import DownloadBusiness
from ip2geotools.databases.noncommercial import DbIpCity
from ip2geotools.models import IpLocation
from werkzeug.exceptions import Unauthorized

api = ns
download_business = DownloadBusiness()


@api.route('/<path:path>')
class Download(APIResource):
    """
    Download
    Full route: /catalog/download/<path>
    """

    def get(self, path):
        """
        Returns
        -------
        image/tif
        """
        try:
            address = DbIpCity.get(request.remote_addr, api_key='free')
        except Exception:
            address = IpLocation(request.remote_addr)

        if request.authorization:
            credentials = request.authorization
            username = credentials.username
            password = credentials.password
        elif request.args.get('key'):
            credentials = request.args['key'].split(':')
            username = credentials[0]
            password = credentials[1]
        else:
            raise Unauthorized('credentials are required')

        path_image, file_name = download_business.get_image(username, password, path, address)
        return send_from_directory(path_image, file_name)
