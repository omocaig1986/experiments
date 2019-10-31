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

from scipy import stats
import math
from matplotlib import pyplot as plt

markers = [r"$\triangle$", r"$\square$", r"$\diamondsuit$", r"$\otimes$", r"$\oslash$"]
USE_TEX = True

if USE_TEX:
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['text.usetex'] = True
    plt.rcParams['text.latex.preamble'] = [
        r"\DeclareUnicodeCharacter{03BB}{$\lambda$}"
        + r"\DeclareUnicodeCharacter{03BC}{$\mu$}"
        + r"\usepackage[utf8]{inputenc}"
        + r"\usepackage{amssymb}"
        # + r"\usepackage{libertine}\usepackage[libertine]{newtxmath}\usepackage[T1]{fontenc}"
        + ""]

WORKING_DIR = "/Users/gabrielepmattia/Coding/p2p-faas/experiments-data/BladeServers/PigoFaceDetectF/LL-PS(1,K)"
DIR_PREFIX = "20000reqs"

N_TESTS = 5
N_THRESHOLDS = 12

ALFA_VALUE = 0.05


def arr_average(arr):
    total = 0.0
    for v in arr:
        total += v
    return total / len(arr)


def arr_variance(arr, avg):
    total = 0.0
    for v in arr:
        total += pow(v - avg, 2)
    return total / (len(arr) - 1)


def plot_confidence(x_arr, y_arr, x_label, y_label, filename):
    plt.clf()
    fig, ax = plt.subplots()

    # for i in range(len(y_arr)):
    ax.plot(x_arr, y_arr[1], marker=markers[0 % len(markers)], markersize=3.0, markeredgewidth=1, linewidth=0.7,
            color='C0')
    ax.fill_between(x_arr, y_arr[0], y_arr[1], where=y_arr[0] >= y_arr[1], facecolor='C0', alpha=0.2)
    ax.fill_between(x_arr, y_arr[0], y_arr[2], where=y_arr[0] <= y_arr[2], facecolor='C0', alpha=0.2)

    # ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    fig.tight_layout()
    plt.savefig("{}/{}.pdf".format(WORKING_DIR, filename))
    plt.close(fig)


pbs = [[] for i in range(N_THRESHOLDS)]
delays = [[] for i in range(N_THRESHOLDS)]

for i in range(1, N_TESTS):
    values_file = open("{}/{}-{}/multi_t.txt".format(WORKING_DIR, DIR_PREFIX, i), "r")
    line_n = 0
    for line in values_file:
        values = line.split(" ")
        pbs[line_n].append(float(values[1]))
        delays[line_n].append(float(values[2]))
        line_n += 1
    values_file.close()

pbs_avgs = []
pbs_vars = []
pbs_upper = []
pbs_lower = []

delays_avgs = []
delays_vars = []
delays_upper = []
delays_lower = []

for i in range(N_THRESHOLDS):
    pbs_avgs.append(arr_average(pbs[i]))
    pbs_vars.append(arr_variance(pbs[i], pbs_avgs[i]))
    tValuePb = stats.t.ppf(1 - (ALFA_VALUE / 2), N_TESTS - 1) * math.sqrt(pbs_vars[i] / N_TESTS)

    pbs_upper.append(pbs_avgs[i] + tValuePb)
    pbs_lower.append(pbs_avgs[i] - tValuePb)

    delays_avgs.append(arr_average(delays[i]))
    delays_vars.append(arr_variance(delays[i], delays_avgs[i]))
    tValueDelay = stats.t.ppf(1 - ALFA_VALUE / 2, N_TESTS - 1) * math.sqrt(delays_vars[i] / N_TESTS)

    delays_upper.append(delays_avgs[i] + tValueDelay)
    delays_lower.append(delays_avgs[i] - tValueDelay)

plot_confidence([i for i in range(N_THRESHOLDS)], [pbs_lower, pbs_avgs, pbs_upper], "T", "$P_B$", "pbs_confidence")
plot_confidence([i for i in range(N_THRESHOLDS)], [delays_lower, delays_avgs, delays_upper], "T", "Delay (s)",
                "delay_confidence")
