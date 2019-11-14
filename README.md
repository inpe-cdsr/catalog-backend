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

Run the server application with the following commands:

```
pyenv activate dgi_catalog_backend
python manage.py run
```


## Docker

You can configure the environment to run through Docker containers. In order to do that, build the image `dgi/catalog`:

```bash
docker build --tag dgi_catalog_backend:0.0.1 -f docker/Dockerfile .
```

After that, you can run the application with  the following command:

```bash
docker run --interactive \
           --tty \
           --detach \
           --name tiler_app \
           --publish 5080:80 \
           dgi_catalog_backend:0.0.1
```
