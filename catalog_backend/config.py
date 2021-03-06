#!/usr/bin/env python3

"""
You can define these configurations and call using environment variable
`ENVIRONMENT`. For example: `export ENVIRONMENT=ProductionConfig`
"""

import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config():
    """Base configuration with default flags"""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production Mode"""
    DEVELOPMENT = False


class DevelopmentConfig(Config):
    """Development Mode"""
    DEVELOPMENT = True


class TestingConfig(Config):
    """Testing Mode (Continous Integration)"""
    TESTING = True


CONFIG = {
    "development": DevelopmentConfig(),
    "production": ProductionConfig(),
    "test": TestingConfig()
}


def get_settings(env):
    """Retrieve Config class from environment"""
    return CONFIG.get(env)
