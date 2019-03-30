import sys
import getopt
import os
from pathlib import Path
import time
import matplotlib.pyplot as plt
import model_mm1k
import numpy as np


def parseAllFiles(path, prefix, start_lambda, end_lambda, lambda_delta, k, machine_id):
    d = {}
    all_values = []

    current_lambda = start_lambda
    while True:
        d[str(current_lambda)] = []
        infile = open("{}/{}l{}-machine{:02}.txt".format(path, prefix,
                                                         str(round(current_lambda, 3)).replace(".", "_"), machine_id))
        for line in infile:
            if line[0] == "#":
                continue
            all_values.append(float(line))
            d[str(current_lambda)].append(float(line))

        infile.close()
        current_lambda = round(lambda_delta + current_lambda, 2)
        if current_lambda > end_lambda:
            break

    return d, all_values


def start_plot(path, prefix, start_lambda, end_lambda, lambda_delta, k, machine_id, bins):
    out_plots_dir = "{0}/{1}".format(path, "_plots_distribution")
    os.makedirs(out_plots_dir, exist_ok=True)
    d, all_values = parseAllFiles(path, prefix, start_lambda, end_lambda, lambda_delta, k, machine_id)
    histogram_data, bins_edges = np.histogram(all_values, bins=bins)
    print(histogram_data, bins_edges)

    def plotAllValuesHist(histogram_data, bins_edges):
        filename = "all-values-hist-machine{:02}.pdf".format(machine_id)
        print("Plotting %s" % filename)
        plt.clf()
        plt.hist(histogram_data, bins=bins_edges)
        plt.show()
        plt.savefig("{}/{}".format(out_plots_dir, filename))

    def plotHeatMap(histogram_data, bins_edges):
        filename = "heatmap-hist-machine{:02}.pdf".format(machine_id)
        print("Plotting %s" % filename)
        plt.clf()
        heat_matrix = []
        l = start_lambda
        while True:
            heat_matrix.append(d[str(l)])
            l = round(lambda_delta + l, 2)
            if l > end_lambda:
                break
        fig, ax = plt.subplots()
        im = ax.imshow(np.array(heat_matrix))
        fig.tight_layout()
        plt.savefig("{}/{}".format(out_plots_dir, filename))

    plotAllValuesHist(histogram_data, bins_edges)
    plotHeatMap(histogram_data, bins_edges)

#
# Entrypoint
#


def main(argv):
    files_path = ""
    files_prefix = "res-line-"
    start_lambda = 1.0
    end_lambda = 3.0
    lambda_delta = 0.1

    function = ""
    fanout = 1
    threshold = 1
    job_duration = 1
    k = 10
    machine_id = 0
    bins = 10

    usage = "utils_plot_times_distribution.py"
    try:
        opts, args = getopt.getopt(
            argv, "hk:p:", ["files-prefix=", "start-lambda=", "end-lambda=", "lambda-delta=", "path=", "function=", "fanout=", "threshold=", "job-duration=", "machine-id="])
    except getopt.GetoptError as e:
        print(e)
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        print(opt + " -> " + arg)
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-p", "--path"):
            files_path = arg
        elif opt in ("--files-prefix"):
            files_prefix = arg
        elif opt in ("--function"):
            function = arg
        elif opt in ("--fanout"):
            fanout = int(arg)
        elif opt in ("--threshold"):
            threshold = int(arg)
        elif opt in ("--job-duration"):
            job_duration = float(arg)
        elif opt in ("-k"):
            k = int(arg)
        elif opt in ("--start-lambda"):
            start_lambda = float(arg)
        elif opt in ("--end-lambda"):
            end_lambda = float(arg)
        elif opt in ("--lambda-delta"):
            lambda_delta = float(arg)
        elif opt in ("--machine-id"):
            machine_id = int(arg)
        elif opt in ("--bins"):
            bins = int(arg)

    if files_path == "":
        print("Some needed parameter was not given")
        print(usage)
        sys.exit()

    print("====== P2P-FOG Plot Distribution Utility ======")
    print("> files_path %s" % files_path)
    print("> files_prefix %s" % files_prefix)
    print("> start_lambda %.2f" % start_lambda)
    print("> end_lambda %.2f" % end_lambda)
    print("> function %s" % function)
    print("> fanout %d" % fanout)
    print("> threshold %d" % threshold)
    print("> job_duration %.6f" % job_duration)
    print("> k %d" % k)
    print("> machine_id %d" % machine_id)
    print("> bins %d" % bins)
    print("")

    mi = 1.0 / job_duration
    start_plot(files_path, files_prefix, start_lambda, end_lambda, lambda_delta, k, machine_id, bins)


if __name__ == "__main__":
    main(sys.argv[1:])
