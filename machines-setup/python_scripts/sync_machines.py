import subprocess
import os
from time import localtime, strftime
import threading

THREAD_POOL_N = 8
SSH_USERNAME = "docker"

consumer_sem = threading.Semaphore(THREAD_POOL_N)

hosts = []
commands = [
    "\"cd /home/docker/code/p2p-fog/experiments/machines-setup ; bash -c ./pull_repositories.sh\"",
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


def threaded_fun(host, i):
    j = 0
    for cmd in commands:
        j += 1
        command = "ssh -o ConnectTimeout=5 {0}@{1} {2}".format(SSH_USERNAME, host, cmd)
        print("[%2d/%2d] Executing %s" % (i, len(hosts), command))
        (status, output) = subprocess.getstatusoutput(command)

        # print the output to file
        file_path = "{0}/machine-{1:02}-command-{2}-res-{3}.txt".format(dir_path, i, j, status)
        outfile = open(file_path, "w")
        outfile.write(output)
        outfile.close()

        print("[%2d/%2d] Command #%d Done! [%s]" % (i, len(hosts), j, status))
        consumer_sem.release()


thread_pool = []

i = 0
for host in hosts:
    i += 1
    consumer_sem.acquire()
    print("> Started job for Machine#%d" % i)
    t = threading.Thread(target=threaded_fun, args=[host, i])
    thread_pool.append(t)
    t.start()

for t in thread_pool:
    t.join()

print("\n> Done!")
