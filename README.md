# DGI Catalog - API

## Installation

### Requirements

Make sure you have the following libraries installed:

- [`Python 3`](https://www.python.org/)
- [`pyenv`](https://github.com/pyenv/pyenv#basic-github-checkout)
- [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv#installing-as-a-pyenv-plugin).

After that, install Python 3.6.8 using pyenv:

```
pyenv install 3.6.8
```

Create a Python environment with the Python version above through pyenv-virtualenv:

```
pyenv virtualenv 3.6.8 dgi_catalog_backend
```

Activate the environment:

```
pyenv activate dgi_catalog_backend
```

Install the requirements:

```
pip install -r requirements.txt
```

## Running

Activating environment variables and pyenv.

```
pyenv activate dgi_catalog_backend
```

Run manage.py file using in test mode:

```
set -a && source environment.dev.env && set +a
python manage.py run
or
python manage.py test
```

Run manage.py file using in production or development mode:

```
set -a && source environment.prod.env && set +a
python manage.py run
```


## Docker

You can configure the environment to run through Docker containers. In order to do that, build the image `dgi/catalog`:

```bash
docker build -t inpe-cdsr-catalog-backend -f docker/dev.Dockerfile . --no-cache
docker build -t registry.dpi.inpe.br/inpe-cdsr/catalog-backend:0.0.1 -f docker/prod.Dockerfile . --no-cache
```

Push the Docker image to the registry:

```
docker push registry.dpi.inpe.br/inpe-cdsr/catalog-backend:0.0.1
```

After that, you can run the application with  the following command:

```bash
docker run --interactive \
           --tty \
           --detach \
           --name tiler_app \
           --publish 5080:5000 \
           dgi_catalog_backend:0.0.1
```
