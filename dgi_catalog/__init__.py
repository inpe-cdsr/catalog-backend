"""DGI Catalog"""

from os import environ as os_environ

from flask import Flask
from flask.logging import create_logger, logging

from flask_cors import CORS

from dgi_catalog.blueprint import blueprint
from dgi_catalog.config import get_settings


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


ENV = os_environ.get('ENV', 'development')

# create Flask app
app = create_app(get_settings(ENV))

# set debug mode to True if ENV == 'development'
app.debug = True if ENV == 'development' else False
# app.debug = False

CORS(app, resorces={r'/d/*': {"origins": '*'}})

# create Flask logger
logger = create_logger(app)
logger.setLevel(logging.INFO)

logger.info('ENV: %s', ENV)
# logger.warning('>>> 1 warning: %s', ENV)
# logger.error('>>> 1 error: %s', ENV)
# logger.critical('>>> 1 critical: %s', ENV)
