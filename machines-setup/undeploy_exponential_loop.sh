#!/bin/sh
cd ../functions/exponential-loop
faas-cli login -u admin --password admin
faas-cli remove exponential-loop
docker system prune -f --volumes