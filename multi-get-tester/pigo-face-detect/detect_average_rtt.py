# This module computes the average response time of a get

import requests
from threading import Thread
import time
from common import cc
from common import read_binary
import os

import matplotlib.pyplot as plt

url = "http://192.168.99.100:18080/function/pigo-face-detector"
image_uri = os.path.dirname(os.path.abspath(__file__)) + "/blobs/family.jpg"
total_req = 500
times = []


def get_request(arg):
    start_time = time.time()

    print("==> [GET] Number #" + str(arg + 1))
    res = requests.post(url, data=read_binary(image_uri))

    end_time = time.time()
    total_time = end_time - start_time

    if res.status_code == 200:
        print(cc.OKGREEN + "==> [RES] Status to #" + str(arg) + " is " +
              str(res.status_code) + " Time " + str(total_time) + cc.ENDC)
    else:
        print(cc.FAIL + "==> [RES] Status " +
              str(res.status_code) + " Time " + str(total_time) + cc.ENDC)

    return total_time


def plot():
    plt.plot(times)
    plt.ylabel('Response times')
    plt.show()


if __name__ == "__main__":
    for i in range(total_req):
        res_time = get_request(i)
        times.append(res_time)

    total_time = 0
    for n in times:
        total_time += n

    avg = total_time / total_req

    print("\nAverage response time is " + str(avg) + "ms")
    plot()

# openfaas direct average is 0.24589629316329956
# our scheduler average is 0.25927630376815797
