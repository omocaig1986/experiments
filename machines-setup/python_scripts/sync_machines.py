import subprocess
import os
from time import localtime, strftime

SSH_USERNAME = "docker"

hosts = []
commands = [
    "\"cd /home/docker/code/p2p-fog/experiments/machines-setup ; bash -c ./pull_repositories.sh && ./deploy_stack.sh\"",
    "\"cd /home/docker/code/p2p-fog/experiments/machines-setup ; bash -c ./pigo_deploy.sh\"",
]

time_str = strftime("%m%d%Y-%H%M%S", localtime())
dir_path = "./_sync-" + time_str
os.makedirs(dir_path, exist_ok=True)

hosts_file = open("hosts.txt", "r")
for host in hosts_file:
    hosts.append(host.strip())
hosts_file.close()

print("> got %d hosts\n" % len(hosts))

i = 0
for host in hosts:
    i += 1
    j = 0
    for cmd in commands:
        j += 1
        command = "ssh {0}@{1} {2}".format(SSH_USERNAME, host, cmd)
        print("> [%2d/%2d] Executing %s" % (i, len(hosts), command))
        (status, output) = subprocess.getstatusoutput(command)
        # print the output to file
        outfile = open(
            "{0}/machine-{1}-command-{2}.txt".format(dir_path, i, j), "w")
        outfile.write(output)
        outfile.close()

        print("> [%2d/%2d] Done! Result %s" % (i, len(hosts), status))
    print()
