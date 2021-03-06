#!/usr/bin/env python3

"""DGI Catalog"""

from flask import Flask
from flask.logging import create_logger, logging
from flask_cors import CORS

from catalog_backend.blueprint import blueprint
from catalog_backend.config import get_settings
from catalog_backend.environment import ENV


def create_app(config):
    """
    Args:
        config (string|catalog_backend.config.Config) Config instance

    Returns:
        Flask Application with config instance scope

    """

    internal_app = Flask(__name__)

    with internal_app.app_context():
        internal_app.config.from_object(config)
        internal_app.register_blueprint(blueprint)

    return internal_app


# create Flask app
app = create_app(get_settings(ENV))

app.config['ERROR_404_HELP'] = False

# set debug mode to True if ENV == 'development'
app.debug = ENV == 'development'
# app.debug = False

# activate CORS
CORS(app, resources={r'/d/*': {"origins": '*'}})

# create Flask logger
logger = create_logger(app)
logger.setLevel(logging.INFO)

# print environment variables
logger.info('ENV: %s', ENV)
