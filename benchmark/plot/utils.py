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

import matplotlib.pyplot as plt


class PlotUtils:
    """Plot utilities"""

    @staticmethod
    def use_tex():
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['text.usetex'] = True
        plt.rcParams['text.latex.preamble'] = [
            r"\DeclareUnicodeCharacter{03BB}{$\lambda$}"
            + r"\DeclareUnicodeCharacter{03BC}{$\mu$}"
            + r"\usepackage[utf8]{inputenc}"
            # + r"\usepackage{libertine}\usepackage[libertine]{newtxmath}\usepackage[T1]{fontenc}"
            + ""]
        return True
