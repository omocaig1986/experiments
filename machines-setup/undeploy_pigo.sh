#!/bin/sh
cd ../functions/pigo-openfaas
faas-cli login -u admin --password admin
faas-cli build pigo-face-detector
docker system prune -f --volumes