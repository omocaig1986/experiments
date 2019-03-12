import subprocess
import warnings

SSH_USERNAME = "docker"

hosts = []
commands = [
    "\"cd /home/docker/code/p2p-fog/experiments/machines-setup ; bash -c ./pull_repositories.sh && ./deploy_stack.sh\"",
    "\"cd /home/docker/code/p2p-fog/experiments/machines-setup ; bash -c ./pigo_deploy.sh\"",
]

hosts_file = open("hosts.txt", "r")
for host in hosts_file:
    hosts.append(host.strip())
hosts_file.close()

print("> got %d hosts" % len(hosts))

for host in hosts:
    for cmd in commands:
        print("> Executing %s" % command)
        command = "ssh {0}@{1} {2}".format(SSH_USERNAME, host, cmd)
        (status, output) = subprocess.getstatusoutput(command)
        print("> Done! Result %s" % status)
        print(output)
        print()
