import contextlib
import os
from pathlib import Path
from dgi_catalog import app
from flask_script import Manager


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
    host = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        port = int(os.environ.get('PORT', '5000'))
    except ValueError:
        port = 5000

    app.run(host, port)


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

    pytest.main(["-v",
                 "--cov-report",
                 "html",
                 "--cov-report",
                 "annotate",
                 "--cov=bdc_eocubes",
                 "-s",
                 "tests/"])

if __name__ == '__main__':
    manager.run()
