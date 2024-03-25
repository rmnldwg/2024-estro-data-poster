"""
Figures and plots for 2024 ESTRO poster on Hypopharynx/Larynx dataset.
"""
from pathlib import Path

from matplotlib import gridspec
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from shared import LNLS, COLORS, COLS, lnls_for_, create_parser, make_invisible


COLORS_LIST = list(COLORS.values())[::-1]

def merge_c13(val: str):
    """Merge C13.8 and C13.9 into one category."""
    if val in ["C13.8", "C13.9"]:
        return "C13.8/9"
    return val


if __name__ == "__main__":
    parser = create_parser(file_name=Path(__file__).stem, description=__doc__)
    args = parser.parse_args()

    data = pd.read_csv(args.input, header=[0,1,2])
    data[COLS.t_stage] = data[COLS.t_stage].apply(lambda x: "early" if x <= 2 else "late")
    data[COLS.subsite] = data[COLS.subsite].apply(merge_c13)
    is_hypopharynx = data["tumor", "1", "location"] == "hypopharynx"
    data = data.loc[is_hypopharynx]

    _grouped = data.groupby(by=[COLS.subsite])
    involved = 100 * _grouped.sum()
    total = _grouped.count()

    fig = plt.figure()
    gs = gridspec.GridSpec(nrows=1, ncols=2, width_ratios=[1, 1], wspace=0.15)
    both_axes = fig.add_subplot(gs[:])
    left_axes = fig.add_subplot(gs[0])
    right_axes = fig.add_subplot(gs[1], sharey=left_axes)
    axes = [left_axes, right_axes]

    for i, side in enumerate(["contra", "ipsi"]):
        for j, subsite in enumerate(['C13.0', 'C12', 'C13.2', 'C13.8/9', 'C13.1']):
            axes[i].barh(
                np.arange(len(LNLS)) - (4 - j) * 0.125,
                width=(
                    involved.loc[subsite, lnls_for_(side)]
                    / total.loc[subsite, lnls_for_(side)]
                ),
                height=0.325,
                color=COLORS_LIST[(j + 0) % 5],
                label=subsite,
                zorder=10,
            )

        axes[i].set_yticks(np.arange(len(LNLS)))
        axes[i].set_yticklabels(LNLS)
        axes[i].set_xticks(np.linspace(0, 70, 8))
        axes[i].grid(visible=True, axis="x", alpha=0.5, color=COLORS["gray"])

    left_axes.legend(
        title="subsite (ICD 10)",
        loc="lower left",
        labelspacing=0.15,
        fontsize="small",
    )
    left_axes.yaxis.tick_right()
    plt.setp(right_axes.get_yticklabels(), visible=False)
    xlim = right_axes.get_xlim()
    left_axes.set_xlim(xlim[::-1])
    both_axes.set_xlabel("Prevalence of Involvement [%]")
    left_axes.set_title("contralateral")
    right_axes.set_title("ipsilateral")

    make_invisible(both_axes)
    plt.savefig(args.output, dpi=300)
