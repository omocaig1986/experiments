import requests
import json
from common import status_str
import sys

SERVICE_PORT = 18080
API_CONFIGURATION_URL = "configuration/scheduler"

ips = []


def preparePayload(scheduler_name, scheduler_parameters):
    payload = {}
    payload["name"] = scheduler_name
    payload["parameters"] = scheduler_parameters
    return json.dumps(payload)


def setConfiguration(host_ip, scheduler_line):
    scheduler_name = scheduler_line[0]
    scheduler_parameters = scheduler_line[1:]
    # prepare request
    url = "http://{0}:{1}/{2}".format(host_ip, SERVICE_PORT, API_CONFIGURATION_URL)
    headers = {'Content-Type': "application/json"}
    ok = True

    print("\r[%s] %s configuring..." % (status_str.CHECK_STR, host_ip), end="")
    try:
        res = requests.post(url, data=preparePayload(scheduler_name, scheduler_parameters
                                                     ), headers=headers, timeout=5)
    except (requests.Timeout, requests.ConnectionError):
        print("\r[%s] %s is not responding" % (status_str.DEAD_STR, host_ip))
        ok = False

    if ok:
        print_str = status_str.OK_STR
        if res.status_code != 200:
            print_str = status_str.DEAD_STR

        print("\r[%s] %s set with \"%s:%s\" [%s]" %
              (print_str, host_ip, scheduler_name, scheduler_parameters, res.status_code))


conf_file = open("hosts.txt", "r")

for line in conf_file:
    if line[0] == "#":
        continue
    ips.append(line.strip())

conf_file.close()

if sys.argv[1] != "--scheduler":
    sys.exit(1)

print("> got %d hosts\n" % len(ips))
print("> got scheduler \"%s\"" % sys.argv[2])

# start requests
for i in range(len(ips)):
    setConfiguration(ips[i], sys.argv[2].split())

print("\n> Done!")
