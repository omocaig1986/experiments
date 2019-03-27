from threading import Thread
import sys
import getopt
import os
from pathlib import Path
import time
import matplotlib.pyplot as plt
import model_mm1k
import numpy as np

DICT_LAMBDA = "lambda"
DICT_PB = "pb"
DICT_DELAY = "delay"
DICT_PE = "pe"
DICT_QUEUE_TIME = "queueTime"
DICT_EXEC_TIME = "execTime"
DICT_FAAS_EXEC_TIME = "faasExecTime"
DICT_PROBE_TIME = "probingTime"
DICT_FORWARDING_TIME = "forwardingTime"


def parseLogFile(file_path):
    in_file = open(file_path, "r")
    d = {DICT_LAMBDA: [], DICT_PB: [], DICT_DELAY: [], DICT_PE: [],
         DICT_QUEUE_TIME: [], DICT_EXEC_TIME: [], DICT_FAAS_EXEC_TIME: [],
         DICT_PROBE_TIME: [], DICT_FORWARDING_TIME: []}

    for line in in_file:
        comps = line.split()
        d[DICT_LAMBDA].append(float(comps[0]))
        d[DICT_PB].append(float(comps[1]))
        d[DICT_DELAY].append(float(comps[2]))
        d[DICT_PE].append(float(comps[3]))
        if len(comps) == 9:
            d[DICT_QUEUE_TIME].append(float(comps[4]))
            d[DICT_EXEC_TIME].append(float(comps[5]))
            d[DICT_FAAS_EXEC_TIME].append(float(comps[6]))
            d[DICT_PROBE_TIME].append(float(comps[7]))
            d[DICT_FORWARDING_TIME].append(float(comps[8]))

    in_file.close()
    return d


def start_plot(files_path, files_prefix, files_number, out_dir, k, f, t, mi, function, with_model, model_name):

    def plotData(i, d, feature, model=None):
        print("[MACHINE#%02d] Plotting %s to \"%s-machine%02d-k%d\"" % (i, feature, feature, i, k))
        plt.clf()
        line_experimental, = plt.plot(d[DICT_LAMBDA], d[feature])
        if model != None:
            lines_model, = plt.plot(d[DICT_LAMBDA], model)
            plt.legend([line_experimental, lines_model], ['Experiment', "Model " + model_name])

        plt.title("{0} - LL({1}, K-{2}) - (K={3},μ={4:.4f}) - Machine#{5}".format(function, f, t, k, mi, i))
        plt.xlabel("λ")
        plt.ylabel(feature)
        plt.savefig("{0}/{1}-machine{2:02}-k{3}.pdf".format(out_dir, feature, i, k))

    def plotStackedTimings(i, d):
        filetitle = "stackedTimings"
        filename = "{0}/{1}-machine{2:02}-k{3}.pdf".format(out_dir, filetitle, i, k)
        print("[MACHINE#%02d] Plotting %s to \"%s\"" % (i, filetitle, filetitle))

        plt.clf()
        y00 = [0]*len(d[DICT_LAMBDA])
        y0 = d[DICT_PROBE_TIME]
        y1 = sumArrays(y0, d[DICT_FORWARDING_TIME])
        y2 = sumArrays(y1, diffArrays(d[DICT_EXEC_TIME], d[DICT_FAAS_EXEC_TIME]))
        y3 = sumArrays(y2, d[DICT_FAAS_EXEC_TIME])
        y9 = d[DICT_DELAY]
        y0p, = plt.plot(d[DICT_LAMBDA], y0, linewidth=0.5)
        y1p, = plt.plot(d[DICT_LAMBDA], y1, linewidth=0.5)
        y2p, = plt.plot(d[DICT_LAMBDA], y2, linewidth=0.5)
        y3p, = plt.plot(d[DICT_LAMBDA], y3, linewidth=0.5)
        y9p, = plt.plot(d[DICT_LAMBDA], y9, linewidth=0.5)
        plt.legend([y0p, y1p, y2p, y3p, y9p], [DICT_PROBE_TIME, DICT_FORWARDING_TIME,
                                               DICT_EXEC_TIME, DICT_FAAS_EXEC_TIME, DICT_DELAY])
        plt.fill_between(d[DICT_LAMBDA], y0, y00, where=y0 >= y00, facecolor='C0')
        plt.fill_between(d[DICT_LAMBDA], y1, y0, where=y1 >= y0, facecolor='C1')
        plt.fill_between(d[DICT_LAMBDA], y2, y1, where=y1 >= y0, facecolor='C2')
        plt.fill_between(d[DICT_LAMBDA], y3, y2, where=y3 >= y3, facecolor='C3')
        plt.fill_between(d[DICT_LAMBDA], y9, y3, where=y9 >= y3, facecolor='C4')
        plt.savefig(filename)

    # create plot dirs
    os.makedirs(out_dir, exist_ok=True)
    for i in range(files_number):
        d = parseLogFile("{0}/{1}{2:02}.txt".format(files_path, files_prefix, i))
        if with_model:
            plotData(i, d, DICT_PB, model_mm1k.generatePbArray(d[DICT_LAMBDA], k, mi))
            plotData(i, d, DICT_DELAY, model_mm1k.generateDelayArray(d[DICT_LAMBDA], k, mi))
        else:
            plotData(i, d, DICT_PB)
            plotData(i, d, DICT_DELAY)
        plotData(i, d, DICT_PE)
        plotData(i, d, DICT_QUEUE_TIME)
        plotData(i, d, DICT_EXEC_TIME)
        plotData(i, d, DICT_FAAS_EXEC_TIME)
        plotData(i, d, DICT_PROBE_TIME)
        plotData(i, d, DICT_FORWARDING_TIME)
        plotStackedTimings(i, d)

#
# Utils
#


def sumArrays(array1, array2):
    out = []
    if len(array1) != len(array2):
        return out
    for i in range(len(array1)):
        out.append(array1[i] + array2[i])
    return out


def diffArrays(array1, array2):
    out = []
    if len(array1) != len(array2):
        return out
    for i in range(len(array1)):
        out.append(array1[i] - array2[i])
    return out

#
# Entrypoint
#


def main(argv):
    files_path = ""
    files_prefix = "res-line-"
    files_number = 1
    function = ""
    fanout = 1
    threshold = 1
    job_duration = 1
    k = 10
    with_model = False
    model_name = ""

    usage = "utils_plot_times.py"
    try:
        opts, args = getopt.getopt(
            argv, "hk:p:", ["files-prefix=", "files-n=", "path=", "function=", "fanout=", "threshold=", "job-duration=", "with-model", "model-name="])
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
        elif opt in ("--job-duration"):
            job_duration = float(arg)
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
        mfile = Path("{0}/{1}{2:02}.txt".format(files_path, files_prefix, i))
        if not mfile.is_file():
            print("File {0}/{1}{2:02}.txt does not exist".format(files_path, files_prefix, i))
            sys.exit()

    out_dir = "{0}/{1}".format(files_path, "_plots")

    print("====== P2P-FOG Plot Utilities ======")
    print("> files_path %s" % files_path)
    print("> files_prefix %s" % files_prefix)
    print("> files_number %d" % files_number)
    print("> job_duration %f => mi %f" % (job_duration, 1.0/job_duration))
    print("> k %d" % k)
    print("> with model %s" % with_model)
    print("> model name %s" % model_name)
    print("----")
    print("> out_dir %s" % out_dir)
    print("")

    mi = 1.0/job_duration
    start_plot(files_path, files_prefix, files_number, out_dir, k, fanout, threshold, mi,
               function, with_model, model_name)
    # startSuite(cmd_lines, start_lambda, end_lambda, lambda_delta)


if __name__ == "__main__":
    main(sys.argv[1:])
