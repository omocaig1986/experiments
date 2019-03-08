import subprocess
from threading import Thread
import re
import sys
import uuid
import getopt
import os
from pathlib import Path
import time
import matplotlib.pyplot as plt
import model_mm1k

DICT_LAMBDA = "lambda"
DICT_PB = "pb"
DICT_DELAY = "delay"
DICT_PE = "pe"


def parseLogFile(file_path):
    in_file = open(file_path, "r")
    d = {"lambda": [], "pb": [], "delay": [], "pe": []}

    for line in in_file:
        comps = line.split()
        d[DICT_LAMBDA].append(float(comps[0]))
        d[DICT_PB].append(float(comps[1]))
        d[DICT_DELAY].append(float(comps[2]))
        d[DICT_PE].append(float(comps[3]))

    in_file.close()
    return d


def start_plot(files_path, files_prefix, files_number, out_dir, k, f, t, mi, function, with_model, model_name):
    def plotData(i, feature, model=None):
        print("Plotting %s-machine%s-k%d" % (feature, i, k))
        plt.clf()
        line_sperimental, = plt.plot(d[DICT_LAMBDA], d[feature])
        if model != None:
            lines_model, = plt.plot(d[DICT_LAMBDA], model)
            plt.legend([line_sperimental, lines_model], ['Experiment', "Model " + model_name])

        plt.title("{0} - LL({1}, K-{2}) - (K={3},μ={4}) - Machine#{5}".format(function, f, t, k, mi, i))
        plt.xlabel("λ")
        plt.ylabel(feature)
        plt.savefig("{0}/{1}-machine{2}-k{3}.pdf".format(out_dir, feature, i, k))

    # create plot dirs
    os.makedirs(out_dir, exist_ok=True)
    for i in range(files_number):
        d = parseLogFile("{0}/{1}{2}.txt".format(files_path, files_prefix, i))
        if with_model:
            plotData(i, DICT_PB, model_mm1k.generatePbArray(d[DICT_LAMBDA], k, mi))
            plotData(i, DICT_DELAY, model_mm1k.generateDelayArray(d[DICT_LAMBDA], k, mi))
            plotData(i, DICT_PE)
        else:
            plotData(i, DICT_PB)
            plotData(i, DICT_PE)
            plotData(i, DICT_DELAY)


def main(argv):
    files_path = ""
    files_prefix = "res-line-"
    files_number = 1
    function = ""
    fanout = 1
    threshold = 1
    mi = 1
    k = 10
    with_model = False
    model_name = ""

    usage = "utils_plot_times.py"
    try:
        opts, args = getopt.getopt(
            argv, "hk:p:", ["files-prefix=", "files-n=", "path=", "function=", "fanout=", "threshold=", "mi=", "with-model", "model-name="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        # print(opt + " -> " + arg)
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-p", "--path"):
            files_path = arg
        elif opt in ("--files-prefix"):
            files_prefix = arg
        elif opt in ("--function"):
            function = arg
        elif opt in ("--files-n"):
            files_number = int(arg)
        elif opt in ("--fanout"):
            fanout = int(arg)
        elif opt in ("--threshold"):
            threshold = int(arg)
        elif opt in ("--mi"):
            mi = float(arg)
        elif opt in ("-k"):
            k = int(arg)
        elif opt in ("--with-model"):
            with_model = True
        elif opt in ("--model-name"):
            model_name = arg

    if files_path == "":
        print("Some needed parameter was not given")
        print(usage)
        sys.exit()

    for i in range(files_number):
        mfile = Path("{0}/{1}{2}.txt".format(files_path, files_prefix, i))
        if not mfile.is_file():
            print("File {0}/{1}{2}.txt does not exist".format(files_path, files_prefix, i))
            sys.exit()

    out_dir = "{0}/{1}".format(files_path, "_plots")

    print("====== P2P-FOG Plot Utilities ======")
    print("> files_path %s" % files_path)
    print("> files_prefix %s" % files_prefix)
    print("> files_number %d" % files_number)
    print("> mi %f" % mi)
    print("> k %d" % k)
    print("> with model %s" % with_model)
    print("> model name %s" % model_name)
    print("----")
    print("> out_dir %s" % out_dir)
    print("")

    start_plot(files_path, files_prefix, files_number, out_dir, k, fanout, threshold, mi,
               function, with_model, model_name)
    # startSuite(cmd_lines, start_lambda, end_lambda, lambda_delta)


if __name__ == "__main__":
    main(sys.argv[1:])
