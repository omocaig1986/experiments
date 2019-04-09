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
DICT_DELAY = "timeDelay"
DICT_PE = "pe"
DICT_QUEUE_TIME = "timeQueue"
DICT_EXEC_TIME = "timeExec"
DICT_FAAS_EXEC_TIME = "timeFaasExec"
DICT_PROBE_TIME = "timeProbing"
DICT_FORWARDING_TIME = "timeForwarding"

PLOT_MARKERS = ".,ov^<>x12348s"
PLOT_LINES = ['-', '--', '-.', ':']


def getBaseDict():
    features = getFeaturesArray()
    d = {DICT_LAMBDA: []}
    for f in features:
        d[f] = []
    return d


def getFeaturesArray():
    return [DICT_PB,
            DICT_DELAY,
            DICT_PE,
            DICT_QUEUE_TIME,
            DICT_EXEC_TIME,
            DICT_FAAS_EXEC_TIME,
            DICT_PROBE_TIME,
            DICT_FORWARDING_TIME]


def parseResultFile(file_path):
    # check if file exists
    mfile = Path(file_path)
    if not mfile.is_file():
        print("> file %s does not exist" % file_path)
        return {}

    in_file = open(file_path, "r")
    d = getBaseDict()

    for line in in_file:
        if line[0] == "#":
            continue
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


def parseAllResultFiles(path, from_t, to_t, m, k, function):
    d_all = {}
    for t in range(from_t, to_t):
        filename = "{}-avg-k{}-t{}-m{}.txt".format(
            function.lower().replace(" ", ""), k, k - t, m)
        print("> Parsing file \"%s\"" % filename)
        d_t = parseResultFile("{}/{}".format(path, filename))
        d_all[t] = d_t
    return d_all


def plotFeaturesComparison(d_all, from_t, to_t, m, k, function, mi, f, from_l, to_l, l_delta, out_plots_dir):
    lambdas = int((to_l - from_l) / l_delta) + 2

    def plotData(x_plot, y_plots, y_labels, feature):
        title = "{} - LL({},T) - {}machines".format(function, f, m)
        filename = "comparison-{}.pdf".format(feature)
        print("> Plotting \"%s\"" % filename)

        plt.cla()
        plt.clf()
        plt.close()
        fig, ax = plt.subplots()

        i = 0
        for arr in y_plots:
            ax.plot(x_plot, arr, marker="x",
                    markersize=2.0, markeredgewidth=0.5, linewidth=0.3, label="T = {}".format(y_labels[i]))
            i += 1

        ax.set_xlabel("T")
        ax.set_ylabel(feature)
        ax.set_title(title)
        ax.legend()
        fig.tight_layout()
        plt.savefig("{}/{}".format(out_plots_dir, filename))

    def retrieveData(feature):
        x_plot = []
        y_plots = []
        y_labels = []
        for t in range(from_t, to_t):
            if feature in d_all[t].keys():
                y_plots.append(d_all[t][feature])
                y_labels.append(t)
                if len(x_plot) == 0:
                    x_plot = d_all[t][DICT_LAMBDA]
        return (x_plot, y_plots, y_labels)

    features = getFeaturesArray()
    for feature in features:
        x, y, y_labels = retrieveData(feature)
        plotData(x, y, y_labels, feature)


def plotFixedLambdaFeatures(d_all, from_t, to_t, m, k, function, mi, from_l, to_l, l_delta, f, out_plots_dir):
    lambdas = int((to_l - from_l) / l_delta) + 2

    def getLAtIndex(i):
        return l_delta * i + from_l

    def plotData(to_plot_x, to_plot_y, l, feature):
        title = "{} - LL({},T) - {}machines - λ = {:.2f}".format(function, f, m, l)
        filename = "{}-fixedl{}.pdf".format(feature, "{:.2f}".format(l).replace(".", "_"))
        print("> Plotting \"%s\"" % filename)

        plt.cla()
        plt.clf()
        plt.close()
        fig, ax = plt.subplots()
        ax.plot(to_plot_x, to_plot_y, marker="x", markersize=3.0, markeredgewidth=1.0, linewidth=0.8)
        ax.set_xlabel("T")
        ax.set_ylabel(feature)
        ax.set_title(title)
        fig.tight_layout()
        plt.savefig("{}/{}".format(out_plots_dir, filename))

    def plotAllData(x_plot, y_plots, y_labels, feature):
        title = "{} - LL({},T) - {}machines".format(function, f, m)
        filename = "allData-{}.pdf".format(feature)
        print("> Plotting \"%s\"" % filename)

        plt.cla()
        plt.clf()
        plt.close()
        fig, ax = plt.subplots()

        i = 0
        for arr in y_plots:
            ax.plot(x_plot, arr, marker="x",
                    markersize=2.0, markeredgewidth=0.5, linewidth=0.3, label="λ = {}".format(y_labels[i]))
            i += 1

        ax.set_xlabel("T")
        ax.set_ylabel(feature)
        ax.set_title(title)
        ax.legend()
        fig.tight_layout()
        plt.savefig("{}/{}".format(out_plots_dir, filename))

    def retrievePlotData(l_index, feature):
        to_plot_y = []
        to_plot_x = []

        for t in range(from_t, to_t):
            to_plot_x.append(t)
            if feature not in d_all[t].keys():
                to_plot_y.append(0)
            else:
                to_plot_y.append(d_all[t][feature][l_index])
        return (to_plot_x, to_plot_y)

    def retrieveAllData(feature):
        x_plot = []
        y_plots = []
        y_labels = []

        for l_index in range(lambdas):
            x, y = retrievePlotData(l_index, feature)
            y_plots.append(y)
            y_labels.append(getLAtIndex(l_index))
            if len(x_plot) == 0:
                x_plot = x

        return (x_plot, y_plots, y_labels)

    for l_index in range(lambdas):
        x, y = retrievePlotData(l_index, DICT_PB)
        plotData(x, y, getLAtIndex(l_index), DICT_PB)
        x, y = retrievePlotData(l_index, DICT_DELAY)
        plotData(x, y, getLAtIndex(l_index), DICT_DELAY)

    x, y, l = retrieveAllData(DICT_PB)
    plotAllData(x, y, l, DICT_PB)
    x, y, l = retrieveAllData(DICT_DELAY)
    plotAllData(x, y, l, DICT_DELAY)


def start_plot(path, function, f, from_t, to_t, mi, from_l, to_l, l_delta, k, m, out_plots_dir):
    d_all = parseAllResultFiles(path, from_t, to_t, m, k, function)
    plotFixedLambdaFeatures(d_all, from_t, to_t, m, k, function, mi, from_l, to_l, l_delta, f, out_plots_dir)
    #plotFeaturesComparison(d_all, from_t, to_t, m, k, function, mi, f, from_l, to_l, l_delta, out_plots_dir)


def main(argv):
    path = ""
    function = ""
    fanout = 1
    from_t = 1
    to_t = 10
    job_duration = 1.0
    start_lambda = 0.1
    end_lambda = 1.0
    lambda_delta = 0.05
    k = 10
    m = 8

    usage = "utils_plot_times.py"
    try:
        opts, args = getopt.getopt(
            argv, "hk:p:", ["path=", "function=", "fanout=", "from-threshold=", "to-threshold=", "job-duration=", "start-lambda=", "end-lambda=", "lambda-delta=", "n-machines="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        # print(opt + " -> " + arg)
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-p", "--path"):
            path = arg
        elif opt in ("-k"):
            k = int(arg)
        elif opt in ("--n-machines"):
            m = int(arg)
        elif opt in ("--function"):
            function = arg
        elif opt in ("--fanout"):
            fanout = int(arg)
        elif opt in ("--from-threshold"):
            from_t = int(arg)
        elif opt in ("--from-threshold"):
            to_t = int(arg)
        elif opt in ("--job-duration"):
            job_duration = float(arg)
        elif opt in ("--start-lambda"):
            start_lambda = float(arg)
        elif opt in ("--end-lambda"):
            end_lambda = float(arg)
        elif opt in ("--lambda-delta"):
            lambda_delta = float(arg)

    if path == "":
        print("Some needed parameter was not given")
        print(usage)
        sys.exit()

    out_plots_dir = "{0}/{1}".format(path, "_plots")
    os.makedirs(out_plots_dir, exist_ok=True)

    print("====== P2P-FOG Plot Utilities ======")
    print("> path %s" % path)
    print("> function %s" % function)
    print("> fanout %d" % fanout)
    print("> from_t %d" % from_t)
    print("> to_t %d" % to_t)
    print("> k %d" % k)
    print("> job_duration %f" % job_duration)
    print("> start_lambda %.2f" % start_lambda)
    print("> end_lambda %.2f" % end_lambda)
    print("> lambda_delta %.2f" % lambda_delta)
    print("> m %d" % m)
    print("----")
    print("> out_plots_dir %s" % out_plots_dir)
    print("")

    mi = 1.0 / job_duration

    start_plot(path, function, fanout, from_t, to_t, mi, start_lambda, end_lambda, lambda_delta, k, m, out_plots_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
