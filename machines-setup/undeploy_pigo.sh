#!/bin/sh
cd ../functions/pigo-openfaas
faas-cli login -u admin --password admin
faas-cli remove pigo-face-detector
docker system prune -f --volumes