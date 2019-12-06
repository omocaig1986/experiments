import matplotlib.pyplot as plt
import os

PLOT_DIRECTORY = "plot"

markers = [r"$\triangle$", r"$\square$", r"$\diamondsuit$", r"$\otimes$", r"$\star$"]


class PlotUtils:
    """Plot utilities"""

    @staticmethod
    def use_tex():
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['text.usetex'] = True
        plt.rcParams['text.latex.preamble'] = [
            r"\DeclareUnicodeCharacter{03BB}{$\lambda$}"
            + r"\DeclareUnicodeCharacter{03BC}{$\mu$}"
            # + r"\usepackage[utf8]{inputenc}"
            + r"\usepackage{amssymb}"
            # + r"\usepackage[libertine]{newtxmath}"  # \usepackage[libertine]{newtxmath}\usepackage[T1]{fontenc}"
            # + r"\usepackage{mathptmx}"
            # + r"\usepackage[T1]{fontenc}"
            + ""]
        return True


class Plot:
    @staticmethod
    def plot(x_arr, y_arr, x_label, y_label, filename, title=None):
        plt.clf()
        fig, ax = plt.subplots()
        line_experimental, = ax.plot(x_arr, y_arr, marker="x", markersize=3.0, markeredgewidth=1, linewidth=0.7)

        if title is not None:
            ax.set_title(title)

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        fig.tight_layout()
        os.makedirs(PLOT_DIRECTORY, exist_ok=True)
        plt.savefig("{}/{}.pdf".format(PLOT_DIRECTORY, filename))
        plt.close(fig)

    @staticmethod
    def multi_plot(x_arr, y_arr, x_label, y_label, filename, legend=None, title=None, log=False):
        if len(x_arr) != len(y_arr):
            print("Error, size mismatch")
            return

        plt.clf()
        fig, ax = plt.subplots()
        legend_arr = []

        for i in range(len(y_arr)):
            line, = ax.plot(x_arr[i], y_arr[i], markerfacecolor='None', linewidth=0.6, marker=markers[i % len(markers)],
                            markersize=5, markeredgewidth=0.6)
            if log:
                ax.set_yscale('log')
            if legend is not None:
                legend_arr.append(line)

        if legend is not None and len(legend) == len(legend_arr):
            plt.legend(legend_arr, legend)

        if title is not None:
            ax.set_title(title)

        # ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        fig.tight_layout()
        os.makedirs(PLOT_DIRECTORY, exist_ok=True)
        plt.savefig("{}/{}.pdf".format(PLOT_DIRECTORY, filename))
        plt.close(fig)
