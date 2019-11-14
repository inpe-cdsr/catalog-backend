"""DGI Catalog"""

import os
from flask import Flask
from flask_cors import CORS
from dgi_catalog.blueprint import blueprint
from dgi_catalog.config import get_settings


ENV = os.environ.get('ENV', 'development')


def create_app(config):
    """
    Args:
        config (string|dgi_catalog.config.Config) Config instance

    Returns:
        Flask Application with config instance scope

    """

    internal_app = Flask(__name__)

    with internal_app.app_context():
        internal_app.config.from_object(config)
        internal_app.register_blueprint(blueprint)

    return internal_app


app = create_app(get_settings(ENV))

# debug mode if ENV == 'development'
app.debug = True if ENV == 'development' else False

CORS(app, resorces={r'/d/*': {"origins": '*'}})
