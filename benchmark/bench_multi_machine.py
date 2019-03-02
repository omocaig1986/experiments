import subprocess
from threading import Thread
import re
import sys
import uuid
import getopt
import os
from pathlib import Path
import time

def start_suite(cmd_lines):
    print("[START] Starting test suite")
    processes = []
    threads = []

    dir_path = "./_test_multi_machine-" + str(time.time()).replace(".", "-")
    os.makedirs(dir_path, exist_ok=True)

    def threaded_fun(i, process):
        print("[TEST] Starting thread#%d" % i)
        out, err = process.communicate()
        print("[TEST] Terminated thread#%d" % i)

        out_f = open(dir_path + "/line-" + str(i) + ".txt", "w")
        #print(str(out), file=out_f)
        out_f.write(str(out))
        out_f.close()

    i = 0
    for line in cmd_lines:
        processes.append(subprocess.Popen(line, stdout=subprocess.PIPE, text=True, shell=True))
        threads.append(Thread(target=threaded_fun, args=[i, processes[i]]))
        i += 1
    
    # start threads
    for i in range(len(cmd_lines)):
        threads[i].start()
    for i in range(len(cmd_lines)):
        threads[i].join()


def main(argv):
    cmd_lines_path = ""
    start_lambda = 1.0
    end_lambda = 1.1
    lambda_delta = 0.1

    usage = "bench_multi_machine.py"
    try:
        opts, args = getopt.getopt(
            argv, "hf:", ["cmd-file="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        # print(opt + " -> " + arg)
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


    start_suite(cmd_lines)

if __name__ == "__main__":
    main(sys.argv[1:])
