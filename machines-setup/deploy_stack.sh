#!/bin/sh
cd ../../
cd stack-discovery
docker build -t discovery .
cd ..
cd stack-scheduler
docker build -t scheduler .
cd ..
cd stack
docker stack rm p2p-fog
docker stack deploy -c docker-compose-local.yml p2p-fog