"""
Blueprint

This file configures application routes, adding namespaces
into global API object
"""

from flask import Blueprint
from flask_restplus import Api

from dgi_catalog.auth.controller import api as auth_ns
from dgi_catalog.user.controller import api as user_ns
from dgi_catalog.status.controller import api as status_ns
from dgi_catalog.download.controller import api as download_ns


blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(blueprint, doc=False)

api.add_namespace(auth_ns)
api.add_namespace(user_ns)
api.add_namespace(status_ns)
api.add_namespace(download_ns)
