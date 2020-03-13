"""
Controllers
"""

# from bdc_core.utils.flask import APIResource
from flask_restplus import Resource as APIResource

from dgi_catalog.status import ns
from dgi_catalog.manifest import version, provider


api = ns


@api.route('/')
class Status(APIResource):
    """
    Status
    Full route: /catalog/status
    """

    def get(self):
        """
        Returns server status

        Request Parameters
        ----------

        Returns
        -------
        dict
            A dictionary that contains server status
        """

        return {
            "dgi_catalog_version": version,
            "dgi_catalog_provider": provider,
            "base": "http://localhost:5000/catalog",
            "description": "API - DGI Catalog (http://localhost:5000)"
        }
