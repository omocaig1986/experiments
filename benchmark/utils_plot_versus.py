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


def start_plot(first_file, second_file, first_title, second_title, x_axis, y_axis, out_dir):
    file_1 = parseLogFile(first_file)
    file_2 = parseLogFile(second_file)

    def plotData(feature, dict_1, dict_2):
        print("{}-{}-vs-{}".format(feature, first_title, second_title))
        plt.clf()
        line_1, = plt.plot(dict_1[DICT_LAMBDA], dict_1[feature])
        line_2, = plt.plot(dict_2[DICT_LAMBDA], dict_2[feature])
        plt.legend([line_1, line_2], [first_title, second_title])

        # plt.title("{0} - LL({1}, K-{2}) - (K={3},μ={4:.4f}) - Machine#{5}".format(function, f, t, k, mi, i))
        plt.xlabel(x_axis)
        plt.ylabel(feature)
        plt.savefig("{}/{}-{}-vs-{}.pdf".format(out_dir, feature, first_title, second_title))

    os.makedirs(out_dir, exist_ok=True)
    plotData(DICT_DELAY, file_1, file_2)
    plotData(DICT_PB, file_1, file_2)
    plotData(DICT_PE, file_1, file_2)


def main(argv):
    first_file = ""
    second_file = ""
    first_title = ""
    second_title = ""
    x_axis = ""
    y_axis = ""
    out_dir = ""

    usage = "utils_plot_versus.py"
    try:
        opts, args = getopt.getopt(
            argv, "h", ["first-file=", "second-file=", "first-title=", "second-title=", "x-axis=", "y-axis=", "out-dir="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        # print(opt + " -> " + arg)
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("--first-file"):
            first_file = arg
        elif opt in ("--second-file"):
            second_file = arg
        elif opt in ("--first-title"):
            first_title = arg
        elif opt in ("--second-title"):
            second_title = arg
        elif opt in ("--x-axis"):
            x_axis = arg
        elif opt in ("--y-axis"):
            y_axis = arg
        elif opt in ("--out-dir"):
            out_dir = arg

    if first_file == "":
        print("Some needed parameter was not given")
        print(usage)
        sys.exit()

    print("====== P2P-FOG Plot Utilities ======")
    print("> first_file %s" % first_file)
    print("> second_file %s" % second_file)
    print("> first_title %s" % first_title)
    print("> second_title %s" % second_title)
    print("> x_axis %s" % x_axis)
    print("> y_axis %s" % y_axis)
    print("----")
    print("> out_dir %s" % out_dir)
    print("")

    start_plot(first_file, second_file, first_title, second_title, x_axis, y_axis, out_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
