# catalog-backend

This application is a back-end service to support the [front-end application](https://github.com/inpe-cdsr/catalog-frontend).


## Requirements

Make sure you have the following packages installed:

- [`Python 3`](https://www.python.org/downloads/)
- [`pyenv`](https://github.com/pyenv/pyenv#basic-github-checkout)
- [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv#installing-as-a-pyenv-plugin).


## Normal installation

Install a specific Python version using `pyenv`:

```
pyenv install 3.6.8
```

Create a Python environment with the Python version above through `pyenv-virtualenv`:

```
pyenv virtualenv 3.6.8 inpe-cdsr-catalog-backend
```

Activate the virtual environment:

```
pyenv activate inpe-cdsr-catalog-backend
```

Install the requirements:

```
pip install -r requirements.txt
```

Create the environment variables file related to either development or production mode:

```
cp environment.env.EXAMPLE environment.[dev|prod].env
```


### Run the application

Activate the virtual environment:

```
pyenv activate inpe-cdsr-catalog-backend
```

Activate the environment variables either in development or production mode:

```
set -a && source environment.[dev|prod].env && set +a
```

Run `manage.py` file in order to run the application:

```
python manage.py run
```

You can run the test files as well:

```
python manage.py test
```


## Installation inside a Docker container

Build the Docker image in development mode:

```
docker build -t inpe-cdsr-catalog-backend -f docker/dev.Dockerfile . --no-cache
```

Build the Docker image in production mode. If you do not have access to `registry.dpi.inpe.br` registry, then you should change to another one.

```
docker build -t registry.dpi.inpe.br/inpe-cdsr/catalog-backend:0.0.5 -f docker/prod.Dockerfile . --no-cache
```

Push the Docker image to the registry:

```
docker push registry.dpi.inpe.br/inpe-cdsr/catalog-backend:0.0.5
```

The Docker images above are used inside docker compose files. Instructions related to how to run these files can be found inside the [Quick Start](https://github.com/inpe-cdsr/catalog/blob/master/quick-start.md).
