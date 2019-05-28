#!/bin/sh
# deploy pigo fake function
cd ../functions/pigo-openfaas-f
faas-cli login -u admin --password admin
faas-cli build
faas-cli deploy
docker system prune -f --volumes