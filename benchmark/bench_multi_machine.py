import subprocess
from threading import Thread
import re
import sys
import uuid
import getopt
import os
from pathlib import Path
from time import localtime, strftime

#r_mean_time = r"mean_time is [0-9 ^\.]*\.[0-9]*"
#r_pb = r"pB is [0-9 ^\.]*\.[0-9]*"


def getTxtOutput(num_thread, l, dir_path):
    return "{0}/l{1}-line-{2}.txt".format(dir_path, round(l, 2), num_thread)


def getResTxtOutput(num_thread, dir_path):
    return "{0}/res-line-{1}.txt".format(dir_path, num_thread)


def doBenchmark(l, cmd_lines, dir_path):
    print("[START] Starting test suite with l = %.2f" % l)
    processes = []
    threads = []
    output = ["" for i in range(len(cmd_lines))]

    def threaded_fun(i, process):
        print("[TEST] Starting thread#%d" % i)
        out, err = process.communicate()
        print("[TEST] Terminated thread#%d" % i)

        out_f = open(getTxtOutput(i, l, dir_path), "w")
        out_f.write(str(out))
        out_f.close()

        out_f = open(getTxtOutput(i, l, dir_path), "r")
        last_line = out_f.readlines()[-1]
        out_f.close()
        output[i] = last_line

    i = 0
    cmd_adding = "--start-lambda \"{0}\" --end-lambda \"{1}\" --lambda-delta \"{2}\"".format(l, l, 0.1)
    for line in cmd_lines:
        processes.append(subprocess.Popen(line.strip() + " " + cmd_adding,
                                          stdout=subprocess.PIPE, text=True, shell=True))
        threads.append(Thread(target=threaded_fun, args=[i, processes[i]]))
        i += 1

    # start threads
    for i in range(len(cmd_lines)):
        threads[i].start()
    for i in range(len(cmd_lines)):
        threads[i].join()

    print("[END] Ending test suite with l = %.2f" % l)
    print()
    return output


def startSuite(cmd_lines, start_lambda, end_lambda, lambda_delta):
    time_str = strftime("%m%d%Y-%H%M%S", localtime())
    dir_path = "./_test_multi_machine-" + time_str
    os.makedirs(dir_path, exist_ok=True)

    l = start_lambda
    results = ["" for i in range(len(cmd_lines))]

    while True:
        lines = doBenchmark(l, cmd_lines, dir_path)
        i = 0
        for line in lines:
            results[i] += line
            i += 1

        l += lambda_delta

        if l > end_lambda:
            break

    # save results
    i = 0
    for result in results:
        out_f = open(getResTxtOutput(i, dir_path), "w")
        out_f.write(result)
        out_f.close()
        i += 1


def main(argv):
    cmd_lines_path = ""
    start_lambda = 1.0
    end_lambda = 1.1
    lambda_delta = 0.1

    usage = "bench_multi_machine.py"
    try:
        opts, args = getopt.getopt(
            argv, "hf:", ["cmd-file=", "start-lambda=", "end-lambda=", "lambda-delta="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        #print(opt + " -> " + arg)
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-f", "--cmd-file"):
            cmd_lines_path = arg
        elif opt in ("-q", "--lambda-delta"):
            lambda_delta = float(arg)
        elif opt in ("--start-lambda"):
            start_lambda = float(arg)
        elif opt in ("--end-lambda"):
            end_lambda = float(arg)

    my_file = Path(cmd_lines_path)
    if not my_file.is_file():
        print("Some needed parameter was not given")
        print(usage)
        sys.exit()

    cmd_lines_f = open(cmd_lines_path, "r")
    cmd_lines = []
    for line in cmd_lines_f:
        cmd_lines.append(line)
    cmd_lines_f.close()

    print("====== P2P-FOG Multimachine benchmark ======")
    print("> file %s" % cmd_lines_path)
    print("> lines %d" % len(cmd_lines))
    print("> lambda [%.2f,%.2f]" % (start_lambda, end_lambda))
    print("> lambda_delta %.2f" % (lambda_delta))
    print("")

    if len(cmd_lines) == 0:
        print("No line passed!")
        sys.exit()

    startSuite(cmd_lines, start_lambda, end_lambda, lambda_delta)


if __name__ == "__main__":
    main(sys.argv[1:])
