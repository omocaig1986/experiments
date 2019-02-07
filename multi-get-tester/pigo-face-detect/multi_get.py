import requests
from threading import Thread
import time
from common import cc
from common import read_binary
import math
import os
import matplotlib.pyplot as plt

url = "http://192.168.99.100:18080/function/pigo-face-detector"
image_uri = os.path.dirname(os.path.abspath(__file__)) + "/blobs/family.jpg"

debug_print = False


def execute_test(ro):
    mean_execution_time = 0.25294546
    #l = 0.55

    req_per_seq = 1 / (ro*mean_execution_time)
    total_sec = 30

    wait_time = 1 / req_per_seq
    total_req = math.floor(req_per_seq * total_sec)

    threads = []
    output = [None] * total_req

    def get_request(arg):
        start_time = time.time()

        if debug_print:
            print("==> [GET] Number #" + str(arg))

        res = requests.post(url, data=read_binary(image_uri))

        end_time = time.time()
        total_time = end_time - start_time

        if debug_print:
            if res.status_code == 200:
                print(cc.OKGREEN + "==> [RES] Status to #" + str(arg) + " is " +
                      str(res.status_code) + " Time " + str(total_time) + cc.ENDC)
            else:
                print(cc.FAIL + "==> [RES] Status " +
                      str(res.status_code) + " Time " + str(total_time) + cc.ENDC)

        output[arg] = [res.status_code, total_time]

    def plot_timings():
        times = []
        for arr in output:
            if arr == None:
                continue
            times.append(arr[1])

        plt.plot(times)
        plt.ylabel('Response times')
        plt.xlabel('Request number')
        plt.show()

    for i in range(total_req):
        thread = Thread(target=get_request, args=(i,))
        thread.start()
        threads.append(thread)
        time.sleep(wait_time)

    for t in threads:
        output.append(t.join())

    rejected_jobs = 0
    accepted_jobs = 0

    for arr in output:
        if arr == None:
            continue
        if arr[0] == 200:
            accepted_jobs += 1
        else:
            rejected_jobs += 1

    if debug_print:
        print("\n")
        print("By using l=%f for an mean execution time of %f" %
              (ro, mean_execution_time))
        print("Requests frequency %f, request period %f\n" %
              (req_per_seq, ro*mean_execution_time))
        print("Total %d jobs, %d accepted and %d rejected" %
              (total_req, accepted_jobs, rejected_jobs))
        print("%.2f%% accepted, %.2f%% rejected" % (accepted_jobs * 100 /
                                                    total_req, rejected_jobs * 100/total_req))
        print("\n")

    return rejected_jobs * 100/total_req


if __name__ == "__main__":
    pbs = []
    ro = 1
    # test all ros
    while True:
        print("Executing test with ro = %.2f ..." % (ro))
        pb = execute_test(ro)
        pbs.append(pb)
        print("done. pB is %f" % pb)
        ro -= 0.05
        if ro < 0.15:
            break

    def print_ros():
        print("\nResult:")
        for pb in pbs:
            print(pb)

    print_ros()
