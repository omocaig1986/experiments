echo "***DELETING MACHINES***"
./delete_machines.sh
echo "***CREATING MACHINES***"
./create_machines.sh

echo "***SETTING MACHINES***"
./setup_machines.sh
echo "***MODIFING HOSTS.TXT AND CONFIGURE_DISCOVERY.TXT***"
./setup_hosts_txt.sh

cd python_scripts

echo "***COMMITTING CHANGES***"
git add .
git commit -m "Updated files hosts.txt and configure_discovery.txt"
git push origin master

echo "***CLONING STACK***"
./clone_stack.sh

echo "***SYNCHRONIZING MACHINES***"
./sync_machines.sh

echo "***CONFIGURING DISCOVERY SERVICE***"
./configure_discovery.sh

echo "***CONFIGURING SCHEDULER SERVICE***"
./configure_no_scheduler.sh
