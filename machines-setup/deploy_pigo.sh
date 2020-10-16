#!/bin/sh
FAAS_CLI=~/bin/faas-cli

cd ../functions/pigo-openfaas
$FAAS_CLI login -u admin --password admin
$FAAS_CLI build
$FAAS_CLI deploy
docker system prune -f --volumes