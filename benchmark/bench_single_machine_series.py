#  P2PFaaS - A framework for FaaS Load Balancing
#  Copyright (c) 2019. Gabriele Proietti Mattia <pm.gabriele@outlook.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

#
# This module computes the average response time of a get, by sending requests in series.
#

import requests
import time
from common import cc
from common import read_binary
import os
import math
import getopt
import sys


def bench_rtt(host, function, payload, requests_num):
    url = "http://{}/{}".format(host, function)
    print("> function url is %s" % url)

    def get_request(arg):
        start_time = time.time()

        payload_bin = None
        if payload != "":
            payload_bin = read_binary(payload)

        print("==> [GET] Number #" + str(arg + 1))
        res = requests.post(url, data=payload_bin)

        end_time = time.time()
        total_time = end_time - start_time

        if res.status_code == 200:
            print(cc.OKGREEN + "==> [RES] Status to #" + str(arg) + " is " +
                  str(res.status_code) + " Time " + str(total_time) + cc.ENDC)
        else:
            print(cc.FAIL + "==> [RES] Status " +
                  str(res.status_code) + " Time " + str(total_time) + cc.ENDC)

        return total_time

    times = []

    for i in range(requests_num):
        res_time = get_request(i)
        times.append(res_time)

    total_time = 0
    for n in times:
        total_time += n

    avg = total_time / requests_num

    print("\nMean response time is " + str(avg) + "ms")
    print("Max is %f and min is %f" % (max(times), min(times)))


#
# Entrypoint
#


def main(argv):
    host = ""
    function = ""
    payload = ""
    requests = 200

    usage = "utils_plot_times.py"
    try:
        opts, args = getopt.getopt(
            argv, "h", ["host=", "function=", "payload=", "requests="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        # print(opt + " -> " + arg)
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("--host"):
            host = arg
        elif opt in ("--function"):
            function = arg
        elif opt in ("--payload"):
            payload = arg
        elif opt in ("--requests"):
            requests = int(arg)

    print("====== P2P-FOG Compute mean delay of function ======")
    print("> host %s" % host)
    print("> function %s" % function)
    print("> payload %s" % payload)
    print("> requests %d" % requests)
    print("")

    if host == "" or function == "":
        print("Some needed parameter was not given")
        print(usage)
        sys.exit()

    bench_rtt(host, function, payload, requests)


if __name__ == "__main__":
    main(sys.argv[1:])
