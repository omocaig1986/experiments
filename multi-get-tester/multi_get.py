import requests
from threading import Thread
import time

url = "http://localhost:8080/function/nodeinfo"
req_per_seq = 10
total_sec = 100

wait_time = 1 / req_per_seq
threads = []


class cc:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_request(arg):
    start_time = time.time()

    print("==> [GET] Number #" + str(arg))
    res = requests.get(url)

    end_time = time.time()
    total_time = end_time - start_time

    if res.status_code == 200:
        print(cc.OKGREEN + "==> [RES] Status to #" + str(arg) + " is " +
              str(res.status_code) + " Time " + str(total_time) + cc.ENDC)
    else:
        print(cc.FAIL + "==> [RES] Status " +
              str(res.status_code) + " Time " + str(total_time) + cc.ENDC)


if __name__ == "__main__":
    for i in range(req_per_seq * total_sec):
        thread = Thread(target=get_request, args=(i,))
        thread.start()
        threads.append(thread)
        time.sleep(wait_time)

    for t in threads:
        t.join()
