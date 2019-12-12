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

Run manage.py file using in production or development mode:

```
source environment.production.env
python manage.py run
```

Run manage.py file using in test mode:

```
source environment.development.env
python manage.py test
```


## Docker

You can configure the environment to run through Docker containers. In order to do that, build the image `dgi/catalog`:

```bash
docker build -t dgi-catalog-backend:0.0.1 -f docker/dev.Dockerfile . --no-cache
docker build -t registry.dpi.inpe.br/dgi/dgi-catalog-backend:0.0.1 -f docker/prod.Dockerfile . --no-cache
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
