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

#url = "http://192.168.99.100:18080/function/pigo-face-detector"
#image_uri = os.path.dirname(os.path.abspath(__file__)) + "/blobs/family.jpg"

debug_print = False


class FunctionTest():
    def __init__(self, url, payload, ro, mi, k):
        self.url = url
        self.payload = payload
        self.ro = ro
        self.mi = mi
        self.k = k
        self.dir = "_test_" + url[url.rfind("/"):]
        self.test_name = "k" + str(k) + "_ro" + str(ro).replace(".", "_") + "_mi" + str(mi).replace(".", "_")

        # prepare suite parameters
        self.l = self.ro*(self.k/self.mi)  # job rate
        self.sec = 30  # total running time for test, in seconds
        self.total_requests = math.floor(self.l * self.sec)
        self.wait_time = 1 / self.l

        self.output = []
        self.threads = []
        self.output = [None] * self.total_requests
        self.pa = 0.0
        self.pb = 0.0

    def execute_test(self):
        """ Execute test by passing ro and mi as average execution time """

        print("[TEST] Starting with ro = %.2f, l = %.2f, k = %d" % (self.ro, self.l, self.k))
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

            self.output[arg] = [res.status_code, total_time]

        for i in range(self.total_requests):
            print("\r[TEST] Request %d/%d" % (i, self.total_requests), end='')
            thread = Thread(target=get_request, args=(i,))
            thread.start()
            self.threads.append(thread)
            time.sleep(self.wait_time)

        for t in self.threads:
            t.join()

        rejected_jobs = 0
        accepted_jobs = 0

        for arr in self.output:
            if arr == None:
                continue
            if arr[0] == 200:
                accepted_jobs += 1
            else:
                rejected_jobs += 1

        self.pb = rejected_jobs * 100/self.total_requests
        self.pa = accepted_jobs * 100/self.total_requests

        print("\n[TEST] Done. Of %d jobs, %d accepted, %d rejected. pB is %.6f\n" %
              (self.total_requests, accepted_jobs, rejected_jobs, self.pb))

    def plot_timings(self):
        times = []
        for arr in self.output:
            if arr == None:
                continue
            times.append(arr[1])

        plt.plot(times)
        plt.ylabel('Response times')
        plt.xlabel('Request number')
        plt.show()

    def getPb(self):
        return self.pb


def start_suite(url, payload, start_ro, end_ro, mi, k):
    print("======== Starting test suite ========")
    print("> url " + url)
    print("> payload " + payload)
    print("> ro [%.2f,%.2f]" % (start_ro, end_ro))
    print("> mi %.2f" % (mi))
    print("> k %d" % (k))
    print("\n")

    pbs = []
    ro = start_ro
    # test all ros
    while True:
        test = FunctionTest(url, payload, ro, mi, k)
        test.execute_test()
        pbs.append(test.getPb())

        ro -= 0.05
        if ro < end_ro:
            break

    def print_ros():
        print("\nResults from ro = %.2f to ro = %.2f:" % (start_ro, end_ro))
        for pb in pbs:
            print(pb)

    print_ros()


def main(argv):
    url = ""
    start_ro = -1
    end_ro = -1
    mi = -1
    k = -1
    debug = False
    payload = ""

    usage = "multi_get.py"
    try:
        opts, args = getopt.getopt(argv, "hdm:u:p:k:", ["url=", "start-ro=", "end-ro=", "mi=", "debug="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        # print(opt + " -> " + arg)
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-d", "--debug"):
            debug_print = True
            debug = True
        elif opt in ("-m", "--mi"):
            mi = float(arg)
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("--start-ro"):
            start_ro = float(arg)
        elif opt in ("--end-ro"):
            end_ro = float(arg)
        elif opt in ("-p", "--payload"):
            payload = arg
        elif opt in ("-k"):
            k = int(arg)

    if start_ro < 0 or end_ro < 0 or mi < 0 or url == "" or k < 0:
        print("Some needed parameter was not given")
        print(usage)
        sys.exit()

    start_suite(url, payload, start_ro, end_ro, mi, k)


if __name__ == "__main__":
    main(sys.argv[1:])
