rm ./python_scripts/hosts.txt
{
    echo $(docker-machine ip n1)
    echo $(docker-machine ip n2)
    echo $(docker-machine ip n3)
    echo $(docker-machine ip n4)
} > ./python_scripts/hosts.txt

rm ./python_scripts/configure_discovery.txt
{
    echo docker@$n1 $(docker-machine ip n1)
    echo docker@$n2 $(docker-machine ip n2)
    echo docker@$n3 $(docker-machine ip n3)
    echo docker@$n4 $(docker-machine ip n4)
} > ./python_scripts/configure_discovery.txt