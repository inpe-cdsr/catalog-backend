# DGI Catalog - API

## Installation

### Requirements

- [`Python 3+`](https://python.org)

Install dgi_catalog [`requirements.txt`](./requirements.txt) with the following command:

```bash
pip install -r requirements.txt
```

## Running

Run dgi_catalog application with command:

```bash
python manage.py run
```

## Docker

You can configure the environment to run through Docker containers. In order to do that, build the image `dgi/catalog`:

```bash
docker build --tag dgi/catalog_api:0.0.1 -f docker/Dockerfile .
```

After that, you can run the application with command:

```bash
docker run --interactive \
           --tty \
           --detach \
           --name tiler_app \
           --publish 5080:80 \
           dgi/catalog_api:0.0.1
```
