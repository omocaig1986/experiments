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

# url = "http://192.168.99.100:18080/function/pigo-face-detector"
# image_uri = os.path.dirname(os.path.abspath(__file__)) + "/blobs/family.jpg"

debug_print = False


class FunctionTest():
    def __init__(self, url, payload, l, k, dir_name):
        self.url = url
        self.payload = payload
        self.l = l
        self.k = k
        self.dir_name = dir_name
        self.test_name = "k" + str(k) + "_lambda" + str(round(l, 3)).replace(".", "_")

        # prepare suite parameters
        self.sec = 30  # total running time for test, in seconds
        self.total_requests = math.floor(self.l * self.sec)
        self.wait_time = 1 / self.l

        self.threads = []
        self.accepted_jobs = 0
        self.rejected_jobs = 0
        self.pa = 0.0
        self.pb = 0.0
        self.mean_time = 0.0
        # per-thread variables
        self.timings = [None] * self.total_requests
        self.output = [None] * self.total_requests

    def execute_test(self):
        """ Execute test by passing ro and mi as average execution time """

        print("[TEST] Starting with l = %.2f, k = %d" % (self.l, self.k))
        if not debug_print:
            print("[TEST] Request %d/%d" % (0, self.total_requests), end='')

        def get_request(arg):
            start_time = time.time()

            if debug_print:
                print("==> [GET] Number #" + str(arg))

            res = requests.post(self.url, data=read_binary(self.payload))

            end_time = time.time()
            total_time = end_time - start_time

            if debug_print:
                if res.status_code == 200:
                    print(cc.OKGREEN + "==> [RES] Status to #" + str(arg) + " is " +
                          str(res.status_code) + " Time " + str(total_time) + cc.ENDC)
                else:
                    print(cc.FAIL + "==> [RES] Status " +
                          str(res.status_code) + " Time " + str(total_time) + cc.ENDC)

            self.output[arg] = res.status_code
            self.timings[arg] = total_time

        for i in range(self.total_requests):
            print("\r[TEST] Request %d/%d" % (i + 1, self.total_requests), end='')
            thread = Thread(target=get_request, args=(i,))
            thread.start()
            self.threads.append(thread)
            time.sleep(self.wait_time)

        for t in self.threads:
            t.join()

        self.rejected_jobs = 0
        self.accepted_jobs = 0

        for arr in self.output:
            if arr == None:
                continue
            if arr == 200:
                self.accepted_jobs += 1
            else:
                self.rejected_jobs += 1

        self.pb = self.rejected_jobs * 100/self.total_requests
        self.pa = self.accepted_jobs * 100 / self.total_requests

        self.computeMeans()

        print("\n[TEST] Done. Of %d jobs, %d accepted, %d rejected." %
              (self.total_requests, self.accepted_jobs, self.rejected_jobs))
        print("[TEST] pB is %.6f, mean_time is %.6f\n" % (self.pb, self.mean_time))

        # self.plot_timings()

    def computeMeans(self):
        s = 0.0
        i = 0
        for v in self.timings:
            if self.output[i] == 200:
                s += v
            i += 1
        self.mean_time = s/float(self.accepted_jobs)

    def plot_timings(self):
        plt.clf()
        plt.plot(self.timings)
        plt.ylabel('Response time')
        plt.xlabel('Request number')
        # plt.show()
        plt.savefig(self.dir_name + "/" + self.test_name + "_job_timings")

    def getPb(self):
        return self.pb

    def getMeanTime(self):
        return self.mean_time


def start_suite(url, payload, start_lambda, end_lambda, lambda_delta, k):
    dir_name = "_test_" + url[url.rfind("/") + 1:] + "_" + str(uuid.uuid1())
    os.makedirs(dir_name)

    print("======== Starting test suite ========")
    print("> url " + url)
    print("> payload " + payload)
    print("> lambda [%.2f,%.2f]" % (start_lambda, end_lambda))
    print("> lambda_delta %.2f" % (lambda_delta))
    print("> k %d" % (k))
    print("\n")

    pbs = []
    times = []
    l = start_lambda
    # test all ros
    while True:
        test = FunctionTest(url, payload, l, k, dir_name)
        test.execute_test()
        pbs.append(test.getPb())
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
        for i in range(len(pbs)):
            print("%10.6f %10.6f" % (pbs[i], times[i]))

    print_res()


def main(argv):
    url = ""
    start_lambda = -1
    end_lambda = -1
    lambda_delta = 0.5
    k = -1
    debug = False
    payload = ""

    usage = "multi_get.py"
    try:
        opts, args = getopt.getopt(
            argv, "hdm:u:p:k:", ["url=", "lambda-delta=", "start-lambda=", "end-lambda=", "mi=", "debug="])
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
        elif opt in ("-k"):
            k = int(arg)

    if start_lambda < 0 or end_lambda < 0 or lambda_delta < 0 or url == "" or k < 0:
        print("Some needed parameter was not given")
        print(usage)
        sys.exit()

    start_suite(url, payload, start_lambda, end_lambda, lambda_delta, k)


if __name__ == "__main__":
    main(sys.argv[1:])
