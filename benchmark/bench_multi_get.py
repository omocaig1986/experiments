import requests
from threading import Thread
import time
from common import cc
from common import read_binary
import math
import os
import matplotlib.pyplot as plt
import sys
import getopt
import uuid
import numpy as np
import mimetypes
import random

debug_print = False


class FunctionTest():

    def __init__(self, url, payload, l, k, poisson, requests, dir_name):
        self.url = url
        self.payload = payload
        self.l = l
        self.k = k
        self.dir_name = dir_name
        self.poisson = poisson
        self.test_name = "k" + str(k) + "_lambda" + str(round(l, 3)).replace(".", "_")
        self.payload_binary = None
        self.payload_mime = None

        # prepare suite parameters
        self.sec = 30  # total running time for test, in seconds
        self.total_requests = requests  # to be updated after test
        self.wait_time = 1 / self.l

        self.threads = []
        self.accepted_jobs = 0
        self.rejected_jobs = 0
        self.external_jobs = 0
        self.pa = 0.0
        self.pb = 0.0
        self.mean_time = 0.0
        # per-thread variables
        self.timings = []
        self.output = []
        self.external = []

        print("[INIT] Starting test")

        # load payload
        if payload != None:
            self.payload_binary = read_binary(self.payload)
            self.payload_mime = mimetypes.guess_type(self.payload)[0]
            print("[INIT] Loaded payload of mime " + self.payload_mime)

    def execute_test(self):
        """ Execute test by passing ro and mi as average execution time """

        print("[TEST] Starting with l = %.2f, k = %d, Poisson = %s" % (self.l, self.k, self.poisson))

        def get_request(arg):
            start_time = time.time()

            if debug_print:
                print("==> [GET] Number #" + str(arg))

            headers = {'Content-Type': self.payload_mime}
            res = requests.post(self.url, data=self.payload_binary, headers=headers)

            end_time = time.time()
            total_time = end_time - start_time

            if debug_print:
                if res.status_code == 200:
                    print(cc.OKGREEN + "==> [RES] Status to #" + str(arg) + " is " +
                          str(res.status_code) + " Time " + str(total_time) + cc.ENDC)
                else:
                    print(cc.FAIL + "==> [RES] Status " +
                          str(res.status_code) + " Time " + str(total_time) + cc.ENDC)
                    print(str(res.content))

            self.output[arg] = res.status_code
            self.timings[arg] = total_time
            self.external[arg] = res.headers.get("X-PFog-Externally-Executed") != None

        def burst_requests():
            #self.total_requests = math.floor(self.l * self.sec)
            self.timings = [None] * self.total_requests
            self.output = [None] * self.total_requests
            self.external = [None] * self.total_requests

            if not debug_print:
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
            self.timings = [None] * self.total_requests
            self.output = [None] * self.total_requests
            self.external = [None] * self.total_requests

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
        # compute the jobs rates
        self.rejected_jobs = 0
        self.accepted_jobs = 0
        self.external_jobs = 0

        timings_sum = 0.0
        for i in range(len(self.output)):
            if self.output[i] == 200:
                self.accepted_jobs += 1
                timings_sum += self.timings[i]
            else:
                self.rejected_jobs += 1
            if self.external[i]:
                self.external_jobs += 1

        self.pb = self.rejected_jobs / self.total_requests
        self.pa = self.accepted_jobs / self.total_requests
        self.pe = self.external_jobs / float(self.total_requests)
        if self.accepted_jobs != 0:
            self.mean_time = timings_sum / float(self.accepted_jobs)
        else:
            self.mean_time = 0

        print("\n[TEST] Done. Of %d jobs, %d accepted, %d rejected." %
              (self.total_requests, self.accepted_jobs, self.rejected_jobs))
        print("[TEST] pB is %.6f, mean_time is %.6f" % (self.pb, self.mean_time))
        print("[TEST] %d jobs has been executed externally, %.6f%%\n" % (self.external_jobs, self.pe))

        # self.plot_timings()

    def plot_timings(self):
        plt.clf()
        plt.plot(self.timings)
        plt.ylabel('Response time')
        plt.xlabel('Request number')
        # plt.show()
        plt.savefig(self.dir_name + "/" + self.test_name + "_job_timings")

    def getPb(self):
        return self.pb

    def getPe(self):
        return self.pe

    def getMeanTime(self):
        return self.mean_time


def start_suite(url, payload, start_lambda, end_lambda, lambda_delta, poisson, k, requests):
    dir_name = "_test_" + url[url.rfind("/") + 1:] + "_" + str(uuid.uuid1())
    # os.makedirs(dir_name)

    print("======== Starting test suite ========")
    print("> url %s" % url)
    print("> payload %s" % payload)
    print("> lambda [%.2f,%.2f]" % (start_lambda, end_lambda))
    print("> lambda_delta %.2f" % (lambda_delta))
    print("> k %d" % (k))
    print("> requests %d" % (requests))
    print("> use poisson %s" % ("yes" if poisson else "no"))
    print("\n")

    pbs = []
    times = []
    pes = []
    l = start_lambda
    # test all ros
    while True:
        test = FunctionTest(url, payload, l, k, poisson, requests, dir_name)
        test.execute_test()
        pbs.append(test.getPb())
        pes.append(test.getPe())
        times.append(test.getMeanTime())

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
        print("%s %s %s %s" % ("lambda", "pB", "Mean Time", "pE"))
        for i in range(len(pbs)):
            print("%.2f %.6f %.6f %.6f" % (start_lambda + i*lambda_delta, pbs[i], times[i], pes[i]))

    print_res()


def main(argv):
    url = ""
    start_lambda = -1
    end_lambda = -1
    lambda_delta = 0.5
    k = -1
    debug = False
    payload = None
    poisson = False
    requests = 500

    usage = "multi_get.py"
    try:
        opts, args = getopt.getopt(
            argv, "hdm:u:p:k:rt:", ["url=", "lambda-delta=", "start-lambda=", "end-lambda=", "mi=", "debug=", "poisson=", "requests="])
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
        elif opt in ("-q", "--lambda-delta"):
            lambda_delta = float(arg)
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("--start-lambda"):
            start_lambda = float(arg)
        elif opt in ("--end-lambda"):
            end_lambda = float(arg)
        elif opt in ("-p", "--payload"):
            payload = arg
        elif opt in ("-r", "--poisson"):
            poisson = True
        elif opt in ("-k"):
            k = int(arg)
        elif opt in ("-t", "--requests"):
            requests = int(arg)

    if start_lambda < 0 or end_lambda < 0 or lambda_delta < 0 or url == "" or k < 0:
        print("Some needed parameter was not given")
        print(usage)
        sys.exit()

    start_suite(url, payload, start_lambda, end_lambda, lambda_delta, poisson, k, requests)


if __name__ == "__main__":
    main(sys.argv[1:])
