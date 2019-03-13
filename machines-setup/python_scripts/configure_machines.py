import requests
import json
from common import status_str

SERVICE_PORT = 19000
API_CONFIGURATION_URL = "configuration"

ips = []
ids = []


def preparePayload(host_id, host_ip, init_servers):
    payload = {}
    payload["machine_ip"] = host_ip
    payload["machine_id"] = host_id
    payload["init_servers"] = init_servers
    return json.dumps(payload)


def setConfiguration(host_id, host_ip, init_servers):
    # prepare request
    url = "http://{0}:{1}/{2}".format(host_ip, SERVICE_PORT, API_CONFIGURATION_URL)
    headers = {'Content-Type': "application/json"}
    ok = True

    print("\r[%s] %s configuring..." % (status_str.CHECK_STR, host_ip), end="")
    try:
        res = requests.post(url, data=preparePayload(host_id, host_ip, init_servers), headers=headers, timeout=5)
    except (requests.Timeout, requests.ConnectionError):
        print("\r[%s] %s is not responding" % (status_str.DEAD_STR, host_ip))
        ok = False

    if ok:
        print_str = status_str.OK_STR
        if res.status_code != 200:
            print_str = status_str.DEAD_STR

        print("\r[%s] %s set as \"%s\" [%s]" % (print_str, host_ip, host_id, res.status_code))


conf_file = open("hosts_configuration.txt", "r")

for line in conf_file:
    comp = line.split()
    host_ip = comp[1]
    host_id = comp[0]
    ips.append(host_ip)
    ids.append(host_id)

conf_file.close()

print("> got %d hosts\n" % len(ips))

# start requests
for i in range(len(ips)):
    setConfiguration(ids[i], ips[i], [ips[0]])

print("\n> Done!")
