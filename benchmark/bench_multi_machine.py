from common import cc
from common import read_binary

import subprocess
from threading import Thread
import re
import sys
import uuid
import getopt
import os
from pathlib import Path
from time import localtime, strftime
import requests
import time
import json
import mimetypes

# r_mean_time = r"mean_time is [0-9 ^\.]*\.[0-9]*"
# r_pb = r"pB is [0-9 ^\.]*\.[0-9]*"
CHECK_STR = " " + cc.WARNING + "CHCK" + cc.ENDC + " "
OK_STR = "  " + cc.OKGREEN + "OK" + cc.ENDC + "  "
DEAD_STR = " " + cc.FAIL + "DEAD" + cc.ENDC + " "
MISM_STR = " " + cc.WARNING + "MISM" + cc.ENDC + " "
WARN_STR = " " + cc.WARNING + "WARN" + cc.ENDC + " "

BENCHMARK_SCRIPT = "python bench_multi_get.py"

API_MONITORING_LOAD_URL = "monitoring/load"
RES_API_MONITORING_LOAD_SCHEDULER_NAME = "scheduler_name"
RES_API_MONITORING_LOAD_K = "functions_running_max"

API_DISCOVERY_PORT = 19000
API_DISCOVERY_LIST_URL = "list"


def getTxtOutput(num_thread, l, dir_path):
    return "{0}/lambda{1}-machine-{2:02}.txt".format(dir_path, str(round(l, 2)).replace(".", "_"), num_thread)


def getResTxtOutput(num_thread, dir_path):
    return "{0}/results-machine-{1:02}.txt".format(dir_path, num_thread)


def doBenchmark(l, hosts, function_url, port, payload, requests, poisson, dir_path):
    print("[START] Starting test suite with l = %.2f" % l)
    processes = []
    threads = []
    output = ["" for i in range(len(hosts))]

    def build_cmdline(host):
        out = BENCHMARK_SCRIPT
        out += " " + "--host {0}:{1}".format(host, port)
        out += " " + "--function-url {0}".format(function_url)
        out += " " + "--payload {0}".format(payload)
        out += " " + "--requests {0}".format(requests)
        out += " " + "--start-lambda \"{0}\" --end-lambda \"{1}\" --lambda-delta \"{2}\" ".format(l, l, 0.1)
        if poisson:
            out += " " + "--poisson"
        return out

    def threaded_fun(i, process):
        print("[TEST] Starting thread#%d" % i)
        out, err = process.communicate()
        print("[TEST] Terminated thread#%d" % i)

        out_f = open(getTxtOutput(i, l, dir_path), "w")
        out_f.write(str(out))
        out_f.close()

        out_f = open(getTxtOutput(i, l, dir_path), "r")
        last_line = out_f.readlines()[-1]
        out_f.close()
        output[i] = last_line

    i = 0
    for host in hosts:
        processes.append(subprocess.Popen(build_cmdline(host), stdout=subprocess.PIPE, text=True, shell=True))
        threads.append(Thread(target=threaded_fun, args=[i, processes[i]]))
        i += 1

    # start threads
    for i in range(len(hosts)):
        threads[i].start()
    for i in range(len(hosts)):
        threads[i].join()

    print("[END] Ending test suite with l = %.2f" % l)
    print()
    return output


def startSuite(hosts, function_url, port, payload, requests,  poisson, start_lambda, end_lambda, lambda_delta):
    time_str = strftime("%m%d%Y-%H%M%S", localtime())
    dir_path = "./_test_multi_machine-" + time_str
    os.makedirs(dir_path, exist_ok=True)

    l = start_lambda
    results = ["" for i in range(len(hosts))]

    while True:
        lines = doBenchmark(l, hosts, function_url, port, payload, requests, poisson, dir_path)
        i = 0
        for line in lines:
            results[i] += line
            i += 1

        l += lambda_delta

        if l > end_lambda:
            break

    # save results
    i = 0
    for result in results:
        out_f = open(getResTxtOutput(i, dir_path), "w")
        out_f.write(result)
        out_f.close()
        i += 1


def checkHosts(hosts, scheduler_port):
    print("==> Checking hosts configurations if matches")
    last_scheduler = ""
    last_k = ""
    test_passed = True

    i = 0
    for host in hosts:
        config_url = "http://{0}:{1}/{2}".format(host, scheduler_port, API_MONITORING_LOAD_URL)
        print("\r[%s] %s checking..." % (CHECK_STR, host), end="")

        ok = True

        try:
            res = requests.get(config_url, timeout=5)
        except (requests.Timeout, requests.ConnectionError) as e:
            print("\r[%s] %s is not responding" % (DEAD_STR, host))
            ok = False
            test_passed = False

        if ok:
            body = res.json()
            this_scheduler = body[RES_API_MONITORING_LOAD_SCHEDULER_NAME]
            this_k = body[RES_API_MONITORING_LOAD_K]
            print_str = OK_STR

            if i == 0:
                last_scheduler = this_scheduler
                last_k = this_k
            elif this_scheduler != last_scheduler or this_k != last_k:
                print_str = MISM_STR
                test_passed = False

            print("\r[%s] %s uses scheduler \"%s\" with k=%d" % (print_str, host, this_scheduler, this_k))

        i += 1

    print()
    return test_passed


def checkDiscoveryLists(hosts, discovery_port):

    print("==> Checking peers hosts configurations if matches")
    last_hosts = []
    test_passed = True

    def parsePeersArray(peers):
        out = []
        for peer in peers:
            out.append(peer["ip"])
        return out

    i = 0
    for host in hosts:
        config_url = "http://{0}:{1}/{2}".format(host, discovery_port, API_DISCOVERY_LIST_URL)
        print("\r[%s] %s checking..." % (CHECK_STR, host), end="")

        ok = True

        try:
            res = requests.get(config_url, timeout=5)
        except (requests.Timeout, requests.ConnectionError) as e:
            print("\r[%s] %s is not responding" % (DEAD_STR, host))
            ok = False
            test_passed = False

        if ok:
            body = res.json()
            this_hosts = parsePeersArray(body)

            print_str = OK_STR

            if i == 0:
                last_hosts = this_hosts
            elif not len(last_hosts) == len(this_hosts):
                print_str = MISM_STR
                test_passed = False

            print("\r[%s] %s knows %d peers" % (print_str, host, len(this_hosts)))

        i += 1

    print()
    return test_passed


def checkFunction(hosts, scheduler_port, function_url, payload):
    print("==> Checking if function works on all hosts")
    last_scheduler = ""
    last_k = ""
    test_passed = True

    payload_binary = read_binary(payload)
    payload_mime = mimetypes.guess_type(payload)[0]

    i = 0
    for host in hosts:
        url = "http://{0}:{1}/{2}".format(host, scheduler_port, function_url)
        print("\r[%s] %s checking function..." % (CHECK_STR, host), end="")

        ok = True

        try:
            headers = {'Content-Type': payload_mime}
            res = requests.post(url, timeout=5, data=payload_binary, headers=headers)
        except (requests.Timeout, requests.ConnectionError) as e:
            print("\r[%s] %s is not responding" % (DEAD_STR, host))
            ok = False
            test_passed = False

        if ok:
            print_str = OK_STR
            if res.status_code != 200:
                print_str = WARN_STR
                test_passed = False

            print("\r[%s] %s function results is %s" % (print_str, host, res.status_code))

        i += 1

    print()
    return test_passed


def main(argv):
    hosts_file_path = ""
    scheduler_port = 18080
    discovery_port = 19000
    requests = 200
    poisson = False
    function_url = ""
    payload = ""
    start_lambda = 1.0
    end_lambda = 1.1
    lambda_delta = 0.1

    usage = "bench_multi_machine.py"
    try:
        opts, args = getopt.getopt(
            argv, "hf:k:", ["hosts-file=", "function-url=", "requests=", "payload=", "poisson", "start-lambda=", "end-lambda=", "lambda-delta=", "scheduler-port=", "discovery-port="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        # print(opt + " -> " + arg)
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-f", "--hosts-file"):
            hosts_file_path = arg
        elif opt in ("--scheduler-port"):
            scheduler_port = int(arg)
        elif opt in ("--discovery-port"):
            discovery_port = int(arg)
        elif opt in ("--requests"):
            requests = int(arg)
        elif opt in ("--poisson"):
            poisson = True
        elif opt in ("--function-url"):
            function_url = arg
        elif opt in ("--payload"):
            payload = arg
        elif opt in ("-q", "--lambda-delta"):
            lambda_delta = float(arg)
        elif opt in ("--start-lambda"):
            start_lambda = float(arg)
        elif opt in ("--end-lambda"):
            end_lambda = float(arg)

    my_file = Path(hosts_file_path)
    if not my_file.is_file():
        print("Passed file does not exist at %s" % hosts_file_path)
        print(usage)
        sys.exit()

    hosts_file_f = open(hosts_file_path, "r")
    hosts = []
    for line in hosts_file_f:
        hosts.append(line.strip())
    hosts_file_f.close()

    print("====== P2P-FOG Multimachine benchmark ======")
    print("> file %s" % hosts_file_path)
    print("> scheduler_port %d" % scheduler_port)
    print("> discovery_port %d" % discovery_port)
    print("> hosts %d" % len(hosts))
    print("> function_url %s" % function_url)
    print("> requests %d" % requests)
    print("> payload %s" % payload)
    print("> poisson %s" % poisson)
    print("> lambda [%.2f,%.2f]" % (start_lambda, end_lambda))
    print("> lambda_delta %.2f" % (lambda_delta))
    print("")

    if len(hosts) == 0:
        print("No host passed!")
        sys.exit(1)

    if not checkHosts(hosts, scheduler_port):
        print("Preliminary hosts check not passed!")
        sys.exit(1)

    if not checkDiscoveryLists(hosts, discovery_port):
        print("Preliminary discovery check not passed!")
        sys.exit(1)

    if not checkFunction(hosts, scheduler_port, function_url, payload):
        print("Preliminary function check not passed!")
        sys.exit(1)

    startSuite(hosts, function_url, scheduler_port, payload, requests, poisson, start_lambda, end_lambda, lambda_delta)
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
