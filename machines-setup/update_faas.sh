#!/bin/sh
# Update the openfaas distribution
cd ../../../
cd faas
# update
git checkout $(git rev-parse --abbrev-ref HEAD) --force
git pull
# undeploy
docker stack rm func
sleep 5
# re-reploy
./deploy_stack.sh