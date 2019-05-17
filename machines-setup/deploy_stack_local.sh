#!/bin/bash
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

if [ $(uname -m | cut -b 1-3) == "arm" ]
then
    echo "==> ARM architecture detected"
    docker stack deploy -c docker-compose-local.armhf.yml p2p-fog
else 
    docker stack deploy -c docker-compose-local.yml p2p-fog
fi

# remove unused images and containers
docker system prune -f --volumes