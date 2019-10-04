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

from functools import reduce


def p_i(l, mi, i, k):
    """Compute the probability of the system to be in the state i"""
    ro = float(l) / float(mi)
    k = int(k)
    if ro == 1.0:
        ro -= 0.00001
    return ((1 - ro) / (1 - pow(ro, k + 1))) * pow(ro, i)


def P_B(l, mi, k):
    """Compute the blocking probability"""
    return p_i(l, mi, k, k)


def delay(l, mi, k):
    k = int(k)

    num = reduce(lambda x, y: x + y, [i * p_i(l, mi, i, k) for i in range(0, k + 1)])
    den = l * (1 - P_B(l, mi, k))
    return num / den


def newDelay(l, mi, k):
    ro = float(l) / float(mi)
    k = int(k)

    return ((1) / (mi - l)) - ((k * pow(ro, k + 1)) / (l * (1 - pow(ro, k))))


def generatePbArray(lambda_array, k, mi):
    out = []
    for l in lambda_array:
        out.append(P_B(l, mi, k))
    return out


def generateDelayArray(lambda_array, k, mi):
    out = []
    for l in lambda_array:
        out.append(delay(l, mi, k))
    return out


def generateDelayArrayNew(lambda_array, k, mi):
    out = []
    for l in lambda_array:
        out.append(newDelay(l, mi, k))
    return out

#  print(P_B(0.8, 1, 10))
