#!/bin/sh
cd ../functions/pigo-openfaas-f-double
faas-cli login -u admin --password admin
faas-cli remove pigo-face-detector-f-double
docker system prune -f --volumes