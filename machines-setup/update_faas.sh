#!/bin/sh
# Update the openfaas distribution
cd ../../
cd faas

git checkout $(git rev-parse --abbrev-ref HEAD) --force
git pull
docker stack rm func
./deploy_stack.sh