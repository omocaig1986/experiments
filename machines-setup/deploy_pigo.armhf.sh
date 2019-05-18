#!/bin/sh
cd ../functions/pigo-openfaas-arm
faas-cli login -u admin --password admin
faas-cli build
faas-cli deploy
docker system prune -f --volumes