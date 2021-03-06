#!/usr/bin/env python3

"""log.py"""

import logging

from catalog_backend.environment import LOGGING_LEVEL


logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s', level=LOGGING_LEVEL)
