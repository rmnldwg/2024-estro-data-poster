"""
Figures and plots for 2024 ESTRO poster on Hypopharynx/Larynx dataset.
"""
from pathlib import Path
from itertools import cycle
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tueplots import figsizes, fontsizes

from shared import LNLS, COLORS, create_parser, COLS, WIDTH, OFFSET, lnls_for_, DPI
COLOR_CYCLE = cycle([COLORS["red"], COLORS["orange"], COLORS["blue"], COLORS["green"]])

def main():
    """Run the main function."""
    parser = create_parser(file_name=Path(__file__).stem, description=__doc__)
    args = parser.parse_args()

    data = pd.read_csv(args.input, header=[0,1,2])
    side = "contra"

    involved = 100 * data.groupby(by=[COLS.midext, COLS.location]).sum()
    total = data.groupby(by=[COLS.location]).count()

    # configure figure
    nrows, ncols = 1, 2

    plt.rcParams.update(figsizes.aaai2024_full(nrows=nrows, ncols=ncols, height_to_width_ratio=1.))
    plt.rcParams.update(fontsizes.aaai2024())

    # configure hatch
    linewidth = 1.5
    plt.rcParams["hatch.linewidth"] = linewidth
    plt.rcParams["hatch.color"] = COLORS["red"]

    fig, axes = plt.subplots(nrows, ncols, sharey=True)

    positions = np.arange(len(LNLS))
    barplot_config = {"width": WIDTH, "zorder": 10}

    for j, location in enumerate(["hypopharynx", "larynx"]):
        for i, midext in enumerate([True, False]):
            color = next(COLOR_CYCLE)
            axes[j].bar(
                x=positions - (1 - i) * OFFSET,
                height=(
                    involved.loc[(midext, location), lnls_for_(side)]
                    / total.loc[location, lnls_for_(side)]
                ),
                color=color,
                label=("with" if midext else "without") + " midline extension",
                **barplot_config,
            )

        xlims = axes[j].get_xlim()
        axes[j].set_xlim(xlims[::-1])
        axes[j].set_xticks(np.arange(len(LNLS)))
        axes[j].set_xticklabels(LNLS)
        axes[j].set_xlabel("Lymph Node Level")

        axes[j].grid(visible=True, axis="y", alpha=0.5, color=COLORS["gray"])

        axes[j].set_title(location.capitalize())
        axes[j].legend(labelspacing=0.15, fontsize="small")

    axes[0].set_ylabel("Prevalence of involvement [%]")
    axes[0].set_yticks(np.linspace(0., 21., 8))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(args.output, dpi=DPI)


if __name__ == "__main__":
    main()
