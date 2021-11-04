./delete_machines.sh
./create_machines.sh

./setup_machines.sh
./setup_hosts_txt.sh

cd python_scripts

git add .
git commit -m "Updated files hosts.txt and configure_discovery.txt"
git push origin master

./clone_stack.sh

./sync_machines.sh


./configure_discovery.sh

./configure_no_scheduler.sh
