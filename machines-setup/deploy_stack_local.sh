#!/bin/sh
# deploy the stack
cd ../../
cd stack-discovery
docker build -t discovery:latest .
cd ..
cd stack-scheduler
docker build -t scheduler:latest .
cd ..
cd stack
docker stack rm p2p-fog
docker stack deploy -c docker-compose-local.yml p2p-fog

# remove unused images and containers
docker system prune -f --volumes