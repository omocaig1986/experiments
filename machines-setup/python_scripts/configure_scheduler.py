import requests
import json
from common import status_str
import sys
import getopt

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
    url = "http://{0}:{1}/{2}".format(host_ip,
                                      SERVICE_PORT, API_CONFIGURATION_URL)
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


def main(argv):
    hosts_file_path = ""
    host = ""
    scheduler = ""

    usage = "configure_scheduler.py"

    try:
        opts, args = getopt.getopt(
            argv, "h", ["hosts-file=", "host=", "scheduler="])
    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)
    for opt, arg in opts:
        # print(opt + " -> " + arg)
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in "--hosts-file":
            hosts_file_path = arg
        elif opt in "--scheduler":
            scheduler = arg
        elif opt in "--host":
            host = arg

    print("====== P2P-FAAS Machines Setup ======")
    print("> hosts-file %s" % hosts_file_path)
    print("> host %s" % host)
    print("> scheduler_params %s" % scheduler)

    if host != "" and hosts_file_path != "":
        print("Please specify host or hosts file")
        sys.exit(2)

    if hosts_file_path != "":
        conf_file = open(hosts_file_path, "r")

        for line in conf_file:
            if line[0] == "#":
                continue
            ips.append(line.strip())

        conf_file.close()

        # start requests
        for i in range(len(ips)):
            setConfiguration(ips[i], scheduler.split())

    if host != "":
        setConfiguration(ips[i], scheduler.split())

    print("\n> Done!")


if __name__ == "__main__":
    main(sys.argv[1:])
