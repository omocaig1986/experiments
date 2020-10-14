import subprocess
import os
from time import localtime, strftime
import threading
import time
import sys

if(len(sys.argv) != 4):
    print("usage: clone_stack.py host-username hosts.txt deploy_token_user:pass")
    exit(1)

host_username = sys.argv[1]
hosts_file_path = sys.argv[2]
deploy_token = sys.argv[3]

THREAD_POOL_N = 16
SSH_USERNAME = host_username

consumer_sem = threading.Semaphore(THREAD_POOL_N)

DEPLOY_TOKEN = deploy_token

hosts = []
commands = [
    "rm -rfv ~/code/p2p-faas",
    "mkdir -p ~/code/p2p-faas",
    f"git clone https://{DEPLOY_TOKEN}@gitlab.com/p2p-faas/experiments.git ~/code/p2p-faas/experiments",
    f"git clone https://{DEPLOY_TOKEN}@gitlab.com/p2p-faas/stack.git ~/code/p2p-faas/stack",
    f"git clone https://{DEPLOY_TOKEN}@gitlab.com/p2p-faas/stack-scheduler.git ~/code/p2p-faas/stack-scheduler",
    f"git clone https://{DEPLOY_TOKEN}@gitlab.com/p2p-faas/stack-discovery.git ~/code/p2p-faas/stack-discovery"
]

time_str = strftime("%m%d%Y-%H%M%S", localtime())
dir_path = "./_clone-" + time_str
os.makedirs(dir_path, exist_ok=True)

hosts_file = open(hosts_file_path, "r")
for host in hosts_file:
    if host[0] == "#":
        continue
    hosts.append(host.strip())
hosts_file.close()

print("> got %d hosts\n" % len(hosts))


def threaded_fun(host, i):
    j = 0
    for cmd in commands:
        consumer_sem.acquire()
        j += 1
        command = "ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 {0}@{1} {2}".format(
            SSH_USERNAME, host, cmd)
        print("[%2d/%2d] Executing %s" % (i, len(hosts), command))
        (status, output) = subprocess.getstatusoutput(command)

        # print the output to file
        file_path = "{0}/machine-{1:02}-command-{2}-res-{3}.txt".format(
            dir_path, i, j, status)
        outfile = open(file_path, "w")
        outfile.write(output)
        outfile.close()

        print("[%2d/%2d] Command #%d Done! [%s]" % (i, len(hosts), j, status))
        consumer_sem.release()

        time.sleep(5)


thread_pool = []

i = 0
for host in hosts:
    i += 1
    # print("> Started job for Machine#%d" % i)
    t = threading.Thread(target=threaded_fun, args=[host, i])
    thread_pool.append(t)
    t.start()

for t in thread_pool:
    t.join()

print("\n> Done!")
exit(0)
