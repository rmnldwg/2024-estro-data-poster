"""
Figures and plots for 2024 ESTRO poster on Hypopharynx/Larynx dataset.
"""
from pathlib import Path
from matplotlib import gridspec
import matplotlib.pyplot as plt
from itertools import cycle
import pandas as pd
import numpy as np
from tueplots import figsizes, fontsizes

from shared import (
    COLORS,
    LNLS,
    create_parser,
    OFFSET,
    WIDTH,
    COLS,
    lnls_for_,
    DPI,
)
COLOR_CYCLE = cycle([COLORS["red"], COLORS["orange"], COLORS["blue"], COLORS["green"]])


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

    fig, axes = plt.subplots(nrows=1, ncols=2, sharey=True)
    left_axes = axes[0]
    right_axes = axes[1]

    positions = np.arange(len(LNLS))[::-1]
    barplot_config = {"width": WIDTH, "zorder": 10}

    for j, location in enumerate(["hypopharynx", "larynx"]):
        for i, t_stage in enumerate(["late", "early"]):
            color = next(COLOR_CYCLE)
            axes[j].bar(
                x=positions + (1 - i) * OFFSET,
                height=(
                    involved.loc[(t_stage, location), lnls_for_("ipsi")]
                    / total.loc[location, lnls_for_("ipsi")]
                ),
                color=color,
                linewidth=linewidth,
                label=f"{t_stage} T-stage",
                **barplot_config,
            )
        axes[j].set_title(location.capitalize())
        axes[j].grid(visible=True, axis="y", alpha=0.5, color=COLORS["gray"])

    left_axes.set_xticklabels(LNLS)
    left_axes.set_xticks(positions)
    left_axes.set_xlabel("Lymph Node Level")
    right_axes.set_xticklabels(LNLS)
    right_axes.set_xticks(positions)
    right_axes.set_xlabel("Lymph Node Level")
    left_axes.set_ylabel("Prevalence of involvement [%]")

    left_axes.legend(labelspacing=0.15, fontsize="small")
    right_axes.legend(labelspacing=0.15, fontsize="small")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(args.output, dpi=DPI)


if __name__ == "__main__":
    main()
