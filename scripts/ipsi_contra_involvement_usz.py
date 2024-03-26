"""
Figures and plots for 2024 ESTRO poster on Hypopharynx/Larynx dataset.
"""
from pathlib import Path
from matplotlib import gridspec
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tueplots import figsizes, fontsizes

from shared import (
    COLORS, LNLS, create_parser, OFFSET, WIDTH, COLS, make_invisible, lnls_for_, DPI
)


def main():
    """Run the main function."""
    parser = create_parser(file_name=Path(__file__).stem, description=__doc__)
    args = parser.parse_args()

    data = pd.read_csv(args.input, header=[0,1,2])
    data[COLS.t_stage] = data[COLS.t_stage].apply(lambda x: "early" if x <= 2 else "late")

    involved = 100 * data.groupby(by=[COLS.t_stage, COLS.location]).sum()
    total = data.groupby(by=[COLS.location]).count()

    # configure hatch
    linewidth = 1.5
    plt.rcParams["hatch.linewidth"] = linewidth
    plt.rcParams["hatch.color"] = COLORS["red"]

    # configure figure
    plt.rcParams.update(figsizes.aaai2024_full(nrows=1, ncols=2, height_to_width_ratio=1.))
    plt.rcParams.update(fontsizes.aaai2024())

    fig = plt.figure()
    gs = gridspec.GridSpec(nrows=1, ncols=2, width_ratios=[1, 1], wspace=0.125)
    both_axes = fig.add_subplot(gs[:])
    left_axes = fig.add_subplot(gs[0])
    right_axes = fig.add_subplot(gs[1], sharey=left_axes)
    axes = [left_axes, right_axes]


    positions = np.arange(len(LNLS))
    barplot_config = {"height": WIDTH, "zorder": 10}

    for j, location in enumerate(["hypopharynx", "larynx"]):
        color = COLORS["blue" if location == "larynx" else "orange"]
        edgecolor = COLORS["green" if location == "larynx" else "red"]
        for i, side in enumerate(["contra", "ipsi"]):
            left = [0] * len(LNLS)
            for t_stage in ["early", "late"]:
                axes[i].barh(
                    y=positions - (1 - j) * OFFSET,
                    width=(
                        involved.loc[(t_stage, location), lnls_for_(side)]
                        / total.loc[location, lnls_for_(side)]
                    ),
                    left=left,
                    color=color,
                    hatch="////" if t_stage == "late" else None,
                    edgecolor=edgecolor if t_stage == "late" else color,
                    linewidth=linewidth,
                    label=f"{location} ({t_stage})",
                    **barplot_config,
                )
                left=(
                    involved.loc[(t_stage, location), lnls_for_(side)]
                    / total.loc[location, lnls_for_(side)]
                )
            axes[i].set_xticks(np.linspace(0, 60, 7))
            axes[i].grid(visible=True, axis="x", alpha=0.5, color=COLORS["gray"])

    left_axes.set_yticklabels(LNLS)
    left_axes.set_yticks(positions)
    left_axes.yaxis.tick_right()
    plt.setp(right_axes.get_yticklabels(), visible=False)

    right_axes.set_xlim(0., 60.)
    left_axes.set_xlim(60., 0.)

    both_axes.set_xlabel("Prevalence of Involvement [%]")
    left_axes.set_title("contralateral")
    right_axes.set_title("ipsilateral")
    left_axes.legend(loc="lower left", labelspacing=0.15, fontsize="small")

    make_invisible(both_axes)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(args.output, dpi=DPI)


if __name__ == "__main__":
    main()
