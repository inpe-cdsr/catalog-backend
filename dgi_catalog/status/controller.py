"""Controllers
"""
from bdc_core.utils.flask import APIResource

from dgi_catalog.status import ns
from dgi_catalog.manifest import version, provider

api = ns

@api.route('/')
class Status(APIResource):

    def get(self):
        return {
            "dgi_catalog_version": version,
            "dgi_catalog_provider": provider,
            "base": "http://localhost:5000/catalog",
            "description": "API - DGI Catalog (http://localhost:5000)"
        }
