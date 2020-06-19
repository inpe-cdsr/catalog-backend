"""Controllers"""

from flask_restplus import Resource as APIResource

from catalog_backend.manifest import version, provider
from catalog_backend.status import ns


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
            "catalog_backend_version": version,
            "catalog_backend_provider": provider,
            "base": "http://localhost:5000/catalog",
            "description": "API - DGI Catalog (http://localhost:5000)"
        }
