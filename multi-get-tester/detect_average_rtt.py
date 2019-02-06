# This module computes the average response time of a get

import requests
from threading import Thread
import time
from common import cc

url = "http://192.168.99.100:8080/function/nodeinfo"
total_req = 100
times = []


def get_request(arg):
    start_time = time.time()

    print("==> [GET] Number #" + str(arg + 1))
    res = requests.get(url)

    end_time = time.time()
    total_time = end_time - start_time

    if res.status_code == 200:
        print(cc.OKGREEN + "==> [RES] Status to #" + str(arg) + " is " +
              str(res.status_code) + " Time " + str(total_time) + cc.ENDC)
    else:
        print(cc.FAIL + "==> [RES] Status " +
              str(res.status_code) + " Time " + str(total_time) + cc.ENDC)

    return total_time


if __name__ == "__main__":
    for i in range(total_req):
        res_time = get_request(i)
        times.append(res_time)

    total_time = 0
    for n in times:
        total_time += n

    avg = total_time / total_req

    print("\nAverage response time is "+str(avg) + "ms")
