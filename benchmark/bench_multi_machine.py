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
from common import cc

# r_mean_time = r"mean_time is [0-9 ^\.]*\.[0-9]*"
# r_pb = r"pB is [0-9 ^\.]*\.[0-9]*"

BENCHMARK_SCRIPT = "python bench_multi_get.py"

API_MONITORING_LOAD_URL = "monitoring/load"
RES_API_MONITORING_LOAD_SCHEDULER_NAME = "scheduler_name"
RES_API_MONITORING_LOAD_K = "functions_running_max"


def getTxtOutput(num_thread, l, dir_path):
    return "{0}/l{1}-line-{2}.txt".format(dir_path, round(l, 2), num_thread)


def getResTxtOutput(num_thread, dir_path):
    return "{0}/res-line-{1}.txt".format(dir_path, num_thread)


def doBenchmark(l, hosts, function_url, payload, requests, poisson, dir_path):
    print("[START] Starting test suite with l = %.2f" % l)
    processes = []
    threads = []
    output = ["" for i in range(len(hosts))]

    def build_cmdline(host):
        out = BENCHMARK_SCRIPT
        out += " " + "--host {0}".format(host)
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


def startSuite(hosts, function_url, payload, requests,  poisson, start_lambda, end_lambda, lambda_delta):
    time_str = strftime("%m%d%Y-%H%M%S", localtime())
    dir_path = "./_test_multi_machine-" + time_str
    os.makedirs(dir_path, exist_ok=True)

    l = start_lambda
    results = ["" for i in range(len(hosts))]

    while True:
        lines = doBenchmark(l, hosts, function_url, payload, requests, poisson, dir_path)
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


def checkHosts(hosts):
    print("==> Checking hosts configurations if matches")
    CHECK_STR = " " + cc.WARNING + "CHCK" + cc.ENDC + " "
    OK_STR = "  " + cc.OKGREEN + "OK" + cc.ENDC + "  "
    DEAD_STR = " " + cc.FAIL + "DEAD" + cc.ENDC + " "
    MISM_STR = " " + cc.WARNING + "MISM" + cc.ENDC + " "
    last_scheduler = ""
    last_k = ""
    test_passed = True

    i = 0
    for host in hosts:
        print("\r[%s] %s checking..." % (CHECK_STR, host), end="")
        config_url = "http://{0}/{1}".format(host, API_MONITORING_LOAD_URL)
        ok = True

        try:
            res = requests.get(config_url, timeout=10)
        except (requests.Timeout, requests.ConnectionError) as e:
            print("\r[%s] %s is not responding: %s" % (DEAD_STR, host, e))
            ok = False

        if ok:
            body = res.json()
            this_scheduler = body[RES_API_MONITORING_LOAD_SCHEDULER_NAME]
            this_k = body[RES_API_MONITORING_LOAD_K]
            if i == 0:
                last_scheduler = this_scheduler
                last_k = this_k
            elif this_scheduler != last_scheduler or this_k != last_k:
                print("\r[%s] %s uses scheduler \"%s\" with k=%d" % (MISM_STR, host, this_scheduler, this_k))
                test_passed = False
                pass
            else:
                print("\r[%s] %s uses scheduler \"%s\" with k=%d" % (OK_STR, host, this_scheduler, this_k))

        i += 1
        return test_passed


def main(argv):
    hosts_file_path = ""
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
            argv, "hf:k:", ["hosts-file=", "function-url=", "requests=", "payload=" "poisson", "start-lambda=", "end-lambda=", "lambda-delta="])
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
        sys.exit()

    checkHosts(hosts)
    #startSuite(hosts, function_url, payload, requests, poisson, start_lambda, end_lambda, lambda_delta)


if __name__ == "__main__":
    main(sys.argv[1:])
