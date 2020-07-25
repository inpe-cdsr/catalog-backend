#!/usr/bin/env python3

"""manage.py"""

import contextlib
import os

from flask_script import Manager

from catalog_backend import app
from catalog_backend.environment import SERVER_HOST, SERVER_PORT, DEBUG_MODE


manager = Manager(app)


@contextlib.contextmanager
def working_directory(path):
    """Changes working directory and returns to previous on exit."""
    owd = os.getcwd()
    try:
        os.chdir(path)
        yield path
    finally:
        os.chdir(owd)


@manager.command
def run():
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=DEBUG_MODE)


@manager.command
def docs(serve=False, port=5001):
    import subprocess
    from http.server import test, CGIHTTPRequestHandler
    from pathlib import Path

    docs_directory = Path(os.path.abspath(os.path.dirname(__file__))) / 'docs'

    with working_directory(str(docs_directory)):
        # Generate Documentation through Makefile
        subprocess.call('make html', shell=True)

    if serve:
        with working_directory(str(docs_directory / 'build/html')):
            test(HandlerClass=CGIHTTPRequestHandler, port=int(port), bind='')


@manager.command
def test():
    """Run the unit tests."""

    import pytest
    from logging import disable, CRITICAL

    # disable logging during tests
    # comment this line if you want to show the logging
    disable(CRITICAL)

    pytest.main(["-v",
                 "--cov-report", "term",
                 "--cov-report", "html",
                 "--cov-report", "annotate",
                 "--cov=catalog_backend",
                 "-s",
                 "tests/"])


if __name__ == '__main__':
    manager.run()
