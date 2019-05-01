#!/bin/sh
# deploy the stack
docker login -u "gitlab+deploy-token-64025" -p "CfNK37-zH4oV1xDstDe6"

docker stack rm p2p-fog
docker stack deploy -c docker-compose.yml p2p-fog

# remove unused images and containers
docker system prune -af --volumes