#!/bin/bash

##### DEPLOY

echo
echo "BUILD STARTED"
echo

echo
echo "NEW TAG - API DGI_CATALOG:"
read API_CATALOG_TAG

IMAGE_API_CATALOG="registry.dpi.inpe.br/dgi/catalog_api"

IMAGE_API_CATALOG_FULL="${IMAGE_API_CATALOG}:${API_CATALOG_TAG}"

docker build -t ${IMAGE_API_CATALOG_FULL} -f docker/Dockerfile .

docker push ${IMAGE_API_CATALOG_FULL}