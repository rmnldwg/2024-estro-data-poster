"""
Figures and plots for 2024 ESTRO poster on Hypopharynx/Larynx dataset.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tueplots import figsizes, fontsizes

from shared import LNLS, COLORS, create_parser, COLS, WIDTH, OFFSET, lnls_for_, DPI


def main():
    """Run the main function."""
    parser = create_parser(file_name=Path(__file__).stem, description=__doc__)
    args = parser.parse_args()

    data = pd.read_csv(args.input, header=[0,1,2])
    side = "contra"

    involved = 100 * data.groupby(by=[COLS.midext, COLS.location]).sum()
    total = data.groupby(by=[COLS.location]).count()

    # configure figure
    plt.rcParams.update(figsizes.aaai2024_half(height_to_width_ratio=1.))
    plt.rcParams.update(fontsizes.aaai2024())

    # configure hatch
    linewidth = 1.5
    plt.rcParams["hatch.linewidth"] = linewidth
    plt.rcParams["hatch.color"] = COLORS["red"]

    fig, axes = plt.subplots(nrows=1, ncols=1)

    positions = np.arange(len(LNLS))
    barplot_config = {"width": WIDTH, "zorder": 10}

    for j, location in enumerate(["hypopharynx", "larynx"]):
        color = COLORS["blue" if location == "larynx" else "orange"]
        edgecolor = COLORS["green" if location == "larynx" else "red"]
        axes.bar(
            x=positions - (1 - j) * OFFSET,
            height=(
                involved.loc[(False, location), lnls_for_(side)]
                / total.loc[location, lnls_for_(side)]
            ),
            color=color,
            edgecolor=color,
            linewidth=linewidth,
            label=f"{location} (without midline extension)",
            **barplot_config,
        )
        axes.bar(
            x=positions - (1 - j) * OFFSET,
            height=(
                involved.loc[(True, location), lnls_for_(side)]
                / total.loc[location, lnls_for_(side)]
            ),
            bottom=(
                involved.loc[(False, location), lnls_for_(side)]
                / total.loc[location, lnls_for_(side)]
            ),
            color=color,
            hatch="////",
            edgecolor=edgecolor,
            linewidth=linewidth,
            label=f"{location} (with midline extension)",
            **barplot_config,
        )

    xlims = axes.get_xlim()
    axes.set_xlim(xlims[::-1])
    axes.set_xticks(np.arange(len(LNLS)))
    axes.set_xticklabels(LNLS)
    axes.set_xlabel("Lymph Node Level")

    axes.set_yticks(np.linspace(0, 30, 7))
    axes.set_ylabel("Prevalence of Involvement [%]")
    axes.grid(visible=True, axis="y", alpha=0.5, color=COLORS["gray"])

    axes.set_title("Contralateral Involvement by Midline Extension")
    axes.legend(labelspacing=0.15, fontsize="small")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(args.output, dpi=DPI)


if __name__ == "__main__":
    main()
