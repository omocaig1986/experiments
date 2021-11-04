docker-machine create -d virtualbox --virtualbox-no-vtx-check  n1
docker-machine create -d virtualbox --virtualbox-no-vtx-check  n2
docker-machine create -d virtualbox --virtualbox-no-vtx-check  n3
docker-machine create -d virtualbox --virtualbox-no-vtx-check  n4

ssh-copy-id docker@$(docker-machine ip n1)
ssh-copy-id docker@$(docker-machine ip n2)
ssh-copy-id docker@$(docker-machine ip n3)
ssh-copy-id docker@$(docker-machine ip n4)

ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 docker@$(docker-machine ip n1) "tce-load -wi coreutils -y"