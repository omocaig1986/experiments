docker swarm leave --force
docker swarm init --advertise-addr $(ip addr show eth1 | grep 'inet\b' | awk '{print $2}' | cut -d/ -f 1)