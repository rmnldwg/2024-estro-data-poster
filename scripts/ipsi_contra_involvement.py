"""
Create plots of ipsilateral and contralateral involvement stratified by T-stage.
"""
from pathlib import Path

from matplotlib import gridspec
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tueplots import figsizes, fontsizes

from shared import (
    COLORS, LNLS, COLS, create_parser, lnls_for_, OFFSET, WIDTH, make_invisible, DPI
)


def main():
    """Run the main function."""
    parser = create_parser(file_name=Path(__file__).stem, description=__doc__)
    args = parser.parse_args()

    data = pd.read_csv(args.input, header=[0,1,2])
    data[COLS.t_stage] = data[COLS.t_stage].apply(lambda x: "early" if x <= 2 else "late")
    is_hypopharynx = data[COLS.location] == "hypopharynx"
    data = data.loc[is_hypopharynx]

    _grouped = data.groupby(by=[COLS.t_stage])
    involved = 100 * _grouped.sum()
    total = _grouped.count()

    # configure figure
    plt.rcParams.update(figsizes.aaai2024_full(nrows=1, ncols=2, height_to_width_ratio=1.))
    plt.rcParams.update(fontsizes.aaai2024())

    fig = plt.figure()
    gs = gridspec.GridSpec(nrows=1, ncols=2, width_ratios=[1, 1], wspace=0.15)
    both_axes = fig.add_subplot(gs[:])
    left_axes = fig.add_subplot(gs[0])
    right_axes = fig.add_subplot(gs[1], sharey=left_axes)
    axes = [left_axes, right_axes]

    positions = np.arange(len(LNLS))
    barplot_config = {"height": WIDTH, "zorder": 10}

    for i, side in enumerate(["contra", "ipsi"]):
        for j, t_stage in enumerate(["late", "early"]):
            axes[i].barh(
                y=positions - (1 - j) * OFFSET,
                width=(
                    involved.loc[t_stage, lnls_for_(side)]
                    / total.loc[t_stage, lnls_for_(side)]
                ),
                color=COLORS["red" if t_stage == "late" else "green"],
                label=f"{t_stage} T-stage",
                **barplot_config,
            )
        axes[i].scatter(
            x=(
                involved["max_llh", side][LNLS].sum(axis=0)
                / total["max_llh", side][LNLS].sum(axis=0)
            ),
            y=positions - OFFSET / 2,
            s=200,
            marker="|",
            color="black",
            label=f"total ({len(data)})",
            zorder=10,
        )
        axes[i].set_xticks(np.linspace(0, 70, 8))
        axes[i].grid(visible=True, axis="x", alpha=0.5, color=COLORS["gray"])

    left_axes.legend(loc="lower left", labelspacing=0.15, fontsize="small")
    left_axes.yaxis.tick_right()
    left_axes.set_yticks(positions)
    left_axes.set_yticklabels(LNLS)
    plt.setp(right_axes.get_yticklabels(), visible=False)

    xlim = right_axes.get_xlim()
    left_axes.set_xlim(xlim[::-1])
    both_axes.set_xlabel("Prevalence of Involvement [%]")
    left_axes.set_title("contralateral")
    right_axes.set_title("ipsilateral")

    make_invisible(both_axes)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(args.output, dpi=DPI)


if __name__ == "__main__":
    main()
