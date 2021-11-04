ssh-copy-id docker@$(docker-machine ip n1)
ssh-copy-id docker@$(docker-machine ip n2)
ssh-copy-id docker@$(docker-machine ip n3)
ssh-copy-id docker@$(docker-machine ip n4)

ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 docker@$(docker-machine ip n1) "tce-load -wi coreutils -y"
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 docker@$(docker-machine ip n2) "tce-load -wi coreutils -y"
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 docker@$(docker-machine ip n3) "tce-load -wi coreutils -y"
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 docker@$(docker-machine ip n4) "tce-load -wi coreutils -y"