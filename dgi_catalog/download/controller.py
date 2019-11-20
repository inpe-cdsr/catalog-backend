# disable pylint(line-too-long) (All codes: http://pylint-messages.wikidot.com/all-codes)
# pylint: disable=C0301

"""
Controllers
"""

from flask import request, Response
from bdc_core.utils.flask import APIResource

from dgi_catalog.download import ns
from dgi_catalog.download.business import DownloadBusiness
from ip2geotools.databases.noncommercial import DbIpCity
from ip2geotools.models import IpLocation

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

        credentials = request.authorization
        image = download_business.get_image(credentials, path, address)

        return Response(image, 200, content_type='image/tif')
