#!/bin/sh
cd ../functions/pigo-openfaas
faas-cli login -u admin --password admin
faas-cli build
faas-cli deploy
docker image prune -f