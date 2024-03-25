"""
Create a plot of contralateral involvement stratified by midline extension.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from shared import COLORS, LNLS, COLS, lnls_for_, create_parser, WIDTH, OFFSET


def main():
    """Run the main function."""
    parser = create_parser(file_name=Path(__file__).stem, description=__doc__)
    args = parser.parse_args()

    # prepare data
    data = pd.read_csv(args.input, header=[0,1,2])
    is_hypopharynx = data[COLS.location] == "hypopharynx"
    data = data.loc[is_hypopharynx]
    side = "contra"

    _grouped = data.groupby(by=[COLS.midext])
    involved = 100 * _grouped.sum()
    total = _grouped.count()

    # create figure
    fig, axes = plt.subplots(nrows=1, ncols=1)

    positions = np.arange(len(LNLS))
    barplot_config = {"width": WIDTH, "zorder": 10}

    # plot
    axes.bar(
        x=positions - OFFSET,
        height=involved.loc[True, lnls_for_(side)] / total.loc[True, lnls_for_(side)],
        color=COLORS["blue"],
        label="with midline extension",
        **barplot_config,
    )
    axes.bar(
        x=positions,
        height=involved.loc[False, lnls_for_(side)] / total.loc[False, lnls_for_(side)],
        color=COLORS["orange"],
        label="without midline extension",
        **barplot_config,
    )

    # reverse x-axis
    xlims = axes.get_xlim()
    axes.set_xlim(xlims[::-1])

    axes.set_xlabel("Lymph Node Level")
    axes.set_xticks(positions)
    axes.set_xticklabels(LNLS)

    axes.set_yticks(np.linspace(0, 20, 5))
    axes.set_ylabel("Prevalence of Involvement [%]")
    axes.grid(visible=True, axis="y", alpha=0.5, color=COLORS["gray"])

    axes.set_title("Contralateral Involvement by Midline Extension")
    axes.legend(labelspacing=0.15, fontsize="small")

    # save the figure
    plt.savefig(args.output, dpi=300)


if __name__ == "__main__":
    main()
