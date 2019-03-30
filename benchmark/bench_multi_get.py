from common import cc
from common import read_binary

import requests
from threading import Thread
import time
import math
import os
import matplotlib.pyplot as plt
import sys
import getopt
import uuid
import numpy as np
import mimetypes
import random
import json
from time import localtime, strftime

RES_API_MONITORING_LOAD_SCHEDULER_NAME = "scheduler_name"
RES_API_MONITORING_LOAD_K = "functions_running_max"

API_MONITORING_LOAD_URL = "monitoring/load"

TIMEOUT = 60

TIMINGS_REQUEST_TIME = "request_time"
TIMINGS_QUEUE_TIME = "queue_time"
TIMINGS_FORWARDING_TIME = "forwarding_time"
TIMINGS_EXECUTION_TIME = "execution_time"
TIMINGS_FAAS_EXECUTION_TIME = "faas_execution_time"
TIMINGS_PROBING_TIME = "probing_time"

RES_HEADER_EXTERNALLY_EXECUTED = "X-PFog-Externally-Executed"
RES_HEADER_TIMING_PROBING_LIST = "X-PFog-Timing-Probing-Seconds-List"
RES_HEADER_TIMING_FORWARDING_LIST = "X-PFog-Timing-Forwarding-Seconds-List"
RES_HEADER_TIMING_QUEUE = "X-Pfog-Timing-Queue-Seconds"
RES_HEADER_TIMING_EXECUTION = "X-PFog-Timing-Execution-Seconds"
RES_HEADER_TIMING_FAAS_EXECUTION = "X-PFog-Timing-Faas-Execution-Seconds"


class FunctionTest():

    def __init__(self, url, payload, l, k, poisson, requests, out_dir, machine_id):
        self.debug_print = False
        self.url = url
        self.payload = payload
        self.l = l
        self.k = k
        self.out_dir = out_dir
        self.poisson = poisson
        self.test_name = "k" + str(k) + "_lambda" + str(round(l, 3)).replace(".", "_")
        self.machine_id = machine_id
        self.payload_binary = None
        self.payload_mime = None

        # prepare suite parameters
        self.total_requests = requests  # to be updated after test
        self.wait_time = 1 / self.l

        self.threads = []
        self.accepted_jobs = 0
        self.rejected_jobs = 0
        self.external_jobs = 0
        self.pa = 0.0
        self.pb = 0.0
        self.pe = 0.0
        self.mean_request_time = 0.0
        self.mean_queue_time = 0.0
        self.mean_execution_time = 0.0
        self.mean_faas_execution_time = 0.0
        self.mean_probing_time = 0.0
        self.mean_forwarding_time = 0.0
        # per-thread variables
        self.timings = {
            TIMINGS_QUEUE_TIME: [0.0] * self.total_requests,
            TIMINGS_FAAS_EXECUTION_TIME: [0.0] * self.total_requests,
            TIMINGS_FORWARDING_TIME: [0.0] * self.total_requests,
            TIMINGS_REQUEST_TIME: [0.0] * self.total_requests,
            TIMINGS_EXECUTION_TIME: [0.0] * self.total_requests,
            TIMINGS_PROBING_TIME: [0.0] * self.total_requests,
        }
        self.output = [None] * self.total_requests
        self.external = [None] * self.total_requests

        print("[INIT] Starting test")

        # load payload
        if len(payload) > 0:
            self.payload_binary = read_binary(self.payload)
            self.payload_mime = mimetypes.guess_type(self.payload)[0]
            print("[INIT] Loaded payload of mime " + self.payload_mime)

    def executeTest(self):
        """ Execute test by passing ro and mi as average execution time """

        print("[TEST] Starting with l = %.2f, k = %d, Poisson = %s" % (self.l, self.k, self.poisson))

        def get_request(arg):
            start_time = time.time()
            net_error = False

            if self.debug_print:
                print("==> [GET] Number #" + str(arg))

            try:
                headers = {'Content-Type': self.payload_mime}
                res = requests.post(self.url, data=self.payload_binary, headers=headers, timeout=TIMEOUT)
            except Exception as e:
                print(e)
                net_error = True

            end_time = time.time()
            total_time = end_time - start_time
            self.printReqResLine(arg, res, net_error, total_time)

            # update timings
            self.timings[TIMINGS_REQUEST_TIME][arg] = total_time

            if not net_error:
                self.external[arg] = res.headers.get(RES_HEADER_EXTERNALLY_EXECUTED) != None
                self.output[arg] = res.status_code
                # parse headers if request is successful
                if res.status_code == 200:
                    self.parseTimingsFromHeaders(res.headers, arg)
            else:
                self.output[arg] = 500

        def burst_requests():
            if not self.debug_print:
                print("[TEST] Request %d/%d" % (0, self.total_requests), end='')
            for i in range(self.total_requests):
                print("\r[TEST] Request %d/%d" % (i + 1, self.total_requests), end='')
                thread = Thread(target=get_request, args=(i,))
                thread.start()
                self.threads.append(thread)
                time.sleep(self.wait_time)

            for t in self.threads:
                t.join()

        def poisson_requests():
            elapsed = 0.0
            req_n = 0

            print("\r[TEST] Starting...", end='')
            for i in range(self.total_requests):
                wait_for = random.expovariate(self.l)

                print("\r[TEST] Request %4d/%4d | Elapsed Sec. %4.2f | Next in %.2fs" %
                      (req_n + 1, self.total_requests, elapsed, wait_for), end='')
                thread = Thread(target=get_request, args=(i,))
                self.threads.append(thread)

                elapsed += wait_for
                req_n += 1

                thread.start()
                time.sleep(wait_for)

            for t in self.threads:
                t.join()

        if self.poisson:
            poisson_requests()
        else:
            burst_requests()

        self.computeStats()

    def computeStats(self):
        timings_request_sum = 0.0
        timings_queue_sum = 0.0
        timings_execution_sum = 0.0
        timings_faas_execution_sum = 0.0
        timings_probing_time_sum = 0.0
        timings_forwarding_time_sum = 0.0

        for i in range(len(self.output)):
            if self.output[i] == 200:
                self.accepted_jobs += 1
                timings_request_sum += self.timings[TIMINGS_REQUEST_TIME][i]
                timings_queue_sum += self.timings[TIMINGS_QUEUE_TIME][i]
                timings_execution_sum += self.timings[TIMINGS_EXECUTION_TIME][i]
                timings_faas_execution_sum += self.timings[TIMINGS_FAAS_EXECUTION_TIME][i]
            else:
                self.rejected_jobs += 1

            if self.external[i]:
                self.external_jobs += 1
                timings_probing_time_sum += self.timings[TIMINGS_PROBING_TIME][i]
                timings_forwarding_time_sum += self.timings[TIMINGS_FORWARDING_TIME][i]

        self.pb = self.rejected_jobs / float(self.total_requests)
        self.pa = self.accepted_jobs / float(self.total_requests)

        if self.accepted_jobs > 0:
            self.mean_request_time = timings_request_sum / float(self.accepted_jobs)
            self.mean_queue_time = timings_queue_sum / float(self.accepted_jobs)
            self.mean_execution_time = timings_execution_sum / float(self.accepted_jobs)
            self.mean_faas_execution_time = timings_faas_execution_sum / float(self.accepted_jobs)
            self.pe = self.external_jobs / float(self.accepted_jobs)

        if self.external_jobs > 0:
            self.mean_probing_time = timings_probing_time_sum / float(self.external_jobs)
            self.mean_forwarding_time = timings_forwarding_time_sum / float(self.external_jobs)

        print("\n[TEST] Done. Of %d jobs, %d accepted, %d rejected." %
              (self.total_requests, self.accepted_jobs, self.rejected_jobs))
        print("[TEST] pB is %.6f, mean_request_time is %.6f" % (self.pb, self.mean_request_time))
        print("[TEST] %.6f%% jobs externally executed, forward and probing times are %.6fs %.6fs\n" %
              (self.pe, self.mean_forwarding_time, self.mean_probing_time))

        # self.plotTimings()

    def plotTimings(self):
        plt.clf()
        plt.plot(self.timings)
        plt.ylabel('Response time')
        plt.xlabel('Request number')
        # plt.show()
        plt.savefig(self.out_dir + "/" + self.test_name + "_job_timings")

    def saveRequestTimings(self):
        if self.out_dir == "":
            return
        file_path = "{}/req-times-l{}-machine{}.txt".format(self.out_dir,
                                                            str(round(self.l, 3)).replace(".", "_"), self.machine_id)
        f = open(file_path, "w")
        f.write("# mean={} - {} jobs {}/{} (a/r) - l={:.2} - k={}".format(self.mean_request_time, self.total_requests,
                                                                          self.accepted_jobs, self.rejected_jobs, self.l, self.k))
        for i in range(len(self.timings[TIMINGS_REQUEST_TIME])):
            if self.output[i] == 200:
                f.write("{:.06}\n".format(self.timings[TIMINGS_REQUEST_TIME][i]))
        f.close()

#
# Getters
#

    def getPb(self):
        return self.pb

    def getPe(self):
        return self.pe

    def getTimings(self):
        return {
            TIMINGS_REQUEST_TIME: self.mean_request_time,
            TIMINGS_QUEUE_TIME: self.mean_queue_time,
            TIMINGS_EXECUTION_TIME: self.mean_execution_time,
            TIMINGS_FAAS_EXECUTION_TIME: self.mean_faas_execution_time,
            TIMINGS_FORWARDING_TIME: self.mean_forwarding_time,
            TIMINGS_PROBING_TIME: self.mean_probing_time
        }

    #
    # Utils
    #

    def printReqResLine(self, i, res, net_error, time):
        if not self.debug_print:
            return

        if not net_error:
            if res.status_code == 200:
                print("%s ==> [RES] Status to #%d is %d Time %.6f %s" % (cc.OKGREEN, i, res.status_code, time, cc.ENDC))
            else:
                print("%s ==> [RES] Status to #%d is %d Time %.6f %s" % (cc.FAIL, i, res.status_code, time, cc.ENDC))
                print(str(res.content))

    def parseTimingsFromHeaders(self, headers, i):
        queue_time = float(headers.get(RES_HEADER_TIMING_QUEUE))
        execution_time = float(headers.get(RES_HEADER_TIMING_EXECUTION))
        faas_execution_time = float(headers.get(RES_HEADER_TIMING_FAAS_EXECUTION))

        if headers.get(RES_HEADER_EXTERNALLY_EXECUTED) != None:
            probing_times = json.loads(headers.get(RES_HEADER_TIMING_PROBING_LIST))
            forwarding_times = json.loads(headers.get(RES_HEADER_TIMING_FORWARDING_LIST))
            self.timings[TIMINGS_FORWARDING_TIME][i] = float(forwarding_times[0]) - faas_execution_time
            self.timings[TIMINGS_PROBING_TIME][i] = float(probing_times[0])

        self.timings[TIMINGS_QUEUE_TIME][i] = queue_time
        self.timings[TIMINGS_EXECUTION_TIME][i] = execution_time
        self.timings[TIMINGS_FAAS_EXECUTION_TIME][i] = faas_execution_time


def getSystemParameters(host):
    config_url = "http://{0}/{1}".format(host, API_MONITORING_LOAD_URL)
    res = requests.get(config_url)
    body = res.json()
    return {
        RES_API_MONITORING_LOAD_SCHEDULER_NAME: body[RES_API_MONITORING_LOAD_SCHEDULER_NAME],
        RES_API_MONITORING_LOAD_K: body[RES_API_MONITORING_LOAD_K]
    }


def start_suite(host, function_url, payload, start_lambda, end_lambda, lambda_delta, poisson, k, requests, out_dir, machine_id):
    url = "http://{0}/{1}".format(host, function_url)

    pbs = []
    pes = []
    timings_request = []
    timings_queue = []
    timings_execution = []
    timings_faas_execution = []
    timings_probing = []
    timings_forward = []
    l = start_lambda
    # test all ros
    while True:
        test = FunctionTest(url, payload, l, k, poisson, requests, out_dir, machine_id)
        test.executeTest()
        pbs.append(test.getPb())
        pes.append(test.getPe())
        timings_request.append(test.getTimings()[TIMINGS_REQUEST_TIME])
        timings_queue.append(test.getTimings()[TIMINGS_QUEUE_TIME])
        timings_execution.append(test.getTimings()[TIMINGS_EXECUTION_TIME])
        timings_faas_execution.append(test.getTimings()[TIMINGS_FAAS_EXECUTION_TIME])
        timings_probing.append(test.getTimings()[TIMINGS_PROBING_TIME])
        timings_forward.append(test.getTimings()[TIMINGS_FORWARDING_TIME])

        test.saveRequestTimings()

        if start_lambda >= end_lambda:
            l -= lambda_delta
            if l < end_lambda:
                break
        else:
            l += lambda_delta
            if l > end_lambda:
                break

    def print_res():
        print("\n[RESULTS] From lambda = %.2f to lambda = %.2f:" % (start_lambda, end_lambda))
        print("%s %s %s %s %s %s %s %s %s" % ("lambda", "pB", "MeanReqTime", "pE", "MeanQueueTime",
                                              "MeanExecTime", "MeanFaasExecTime", "MeanProbeTime", "MeanForwardingTime"))
        for i in range(len(pbs)):
            print("%.2f %.6f %.6f %.6f %.6f %.6f %.6f %.6f %.6f" %
                  (start_lambda + i * lambda_delta, pbs[i], timings_request[i], pes[i],
                   timings_queue[i], timings_execution[i], timings_faas_execution[i], timings_probing[i], timings_forward[i]))

    print_res()


def main(argv):
    host = ""
    function_url = ""
    start_lambda = -1
    end_lambda = -1
    lambda_delta = 0.5
    debug = False
    payload = ""
    poisson = False
    requests = 500
    out_dir = ""
    machine_id = 0

    usage = "multi_get.py"
    try:
        opts, args = getopt.getopt(
            argv, "hdm:u:p:k:t:", ["host=",
                                   "function-url=",
                                   "lambda-delta=",
                                   "start-lambda=",
                                   "end-lambda=",
                                   "mi=",
                                   "debug=",
                                   "poisson",
                                   "requests=",
                                   "config-url=",
                                   "payload=",
                                   "out-dir=",
                                   "machine-id="
                                   ])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        # print(opt + " -> " + arg)
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-d", "--debug"):
            debug = True
        elif opt in ("--host"):
            host = arg
        elif opt in ("--function-url"):
            function_url = arg
        elif opt in ("--lambda-delta"):
            lambda_delta = float(arg)
        elif opt in ("--start-lambda"):
            start_lambda = float(arg)
        elif opt in ("--end-lambda"):
            end_lambda = float(arg)
        elif opt in ("-p", "--payload"):
            payload = arg
        elif opt in ("--poisson"):
            poisson = True
        elif opt in ("-t", "--requests"):
            requests = int(arg)
        elif opt in ("--out-dir"):
            out_dir = arg
        elif opt in ("--machine-id"):
            machine_id = int(arg)

    if out_dir == "":
        time_str = strftime("%m%d%Y-%H%M%S", localtime())
        out_dir = "./_test_multi_get-" + time_str
    os.makedirs(out_dir, exist_ok=True)

    print("="*10 + " Starting test suite " + "="*10)
    print("> host %s" % host)
    print("> function_url %s" % function_url)
    print("> payload %s" % payload)
    print("> lambda [%.2f,%.2f]" % (start_lambda, end_lambda))
    print("> lambda_delta %.2f" % (lambda_delta))
    print("> requests %d" % (requests))
    print("> use poisson %s" % ("yes" if poisson else "no"))
    print("> out_dir %s" % (out_dir))
    print("> machine_id %d" % (machine_id))

    if start_lambda < 0 or end_lambda < 0 or lambda_delta < 0 or function_url == "" or host == "":
        print("Some needed parameter was not given")
        print(usage)
        sys.exit()

    params = getSystemParameters(host)
    k = int(params[RES_API_MONITORING_LOAD_K])
    print("-"*10 + " system info " + "-"*10)
    print("> scheduler name %s" % params[RES_API_MONITORING_LOAD_SCHEDULER_NAME])
    print("> k %d" % params[RES_API_MONITORING_LOAD_K])
    print("\n")

    if k < 0 or k == 0:
        print("Received bad k from server")
        print(usage)
        sys.exit()

    start_suite(host, function_url, payload, start_lambda, end_lambda,
                lambda_delta, poisson, k, requests, out_dir, machine_id)


if __name__ == "__main__":
    main(sys.argv[1:])
