rm ./python_scripts/hosts.txt
{
    echo $(docker-machine ip n1)
    echo $(docker-machine ip n2)
    echo $(docker-machine ip n3)
    echo $(docker-machine ip n4)
} > ./python_scripts/hosts.txt