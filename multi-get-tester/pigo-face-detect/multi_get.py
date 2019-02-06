import requests
from threading import Thread
import time
from common import cc
from common import read_binary
import math
import os

url = "http://192.168.99.100:18080/function/pigo-face-detector"
image_uri = os.path.dirname(os.path.abspath(__file__)) + "/blobs/family.jpg"

average_execution_time = 0.26
l = 0.1

req_per_seq = 1 / (0.8*0.26)
total_sec = 30

wait_time = 1 / req_per_seq
total_req = math.floor(req_per_seq * total_sec)

threads = []
output = [None] * total_req


def get_request(arg):
    start_time = time.time()

    print("==> [GET] Number #" + str(arg))
    res = requests.post(url, data=read_binary(image_uri))

    end_time = time.time()
    total_time = end_time - start_time

    if res.status_code == 200:
        print(cc.OKGREEN + "==> [RES] Status to #" + str(arg) + " is " +
              str(res.status_code) + " Time " + str(total_time) + cc.ENDC)
    else:
        print(cc.FAIL + "==> [RES] Status " +
              str(res.status_code) + " Time " + str(total_time) + cc.ENDC)

    output[arg] = [res.status_code, total_time]


if __name__ == "__main__":
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

    print("\n")
    print("By using l=%f for an average execution time of %f" %
          (l, average_execution_time))
    print("Total %d jobs, %d accepted and %d rejected" %
          (total_req, accepted_jobs, rejected_jobs))
    print("%.2f%% rejected, %.2f%% accepted" % (accepted_jobs * 100 /
                                                total_req, rejected_jobs * 100/total_req))
    print("\n")
