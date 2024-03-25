"""
Figures and plots for 2024 ESTRO poster on Hypopharynx/Larynx dataset.
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

LABELS = ["I", "II", "III", "IV", "V", "VI", "VII"][::-1]
COLORS = {
    "green": "#00afa5",
    "red": "#ae0060",
    "blue": "#005ea8",
    "orange": "#f17900",
    "gray": "#c5d5db",
}


if __name__ == "__main__":
    data = pd.read_csv("enhanced.csv", header=[0,1,2])
    side = "contra"

    by_level = 100 * data.groupby(
        by=[("tumor", "1", "extension"), ("tumor", "1", "location")]
    ).sum()
    totals = data.groupby(
        by=[("tumor", "1", "location")],
    ).count()

    fig, axes = plt.subplots(nrows=1, ncols=1)

    for j, location in enumerate(["hypopharynx", "larynx"]):
        axes.bar(
            np.arange(len(LABELS)) - 0.2 + j * 0.4,
            height=(
                by_level.loc[(False, location), ("max_llh", side, LABELS)]
                / totals.loc[location, ("max_llh", side, LABELS)]
            ),
            width=0.4,
            color=COLORS["blue" if location == "larynx" else "orange"],
            label=f"{location} (without midline extension)",
            zorder=10,
        )
        axes.bar(
            np.arange(len(LABELS)) - 0.2 + j * 0.4,
            height=(
                by_level.loc[(True, location), ("max_llh", side, LABELS)]
                / totals.loc[location, ("max_llh", side, LABELS)]
            ),
            bottom=(
                by_level.loc[(False, location), ("max_llh", side, LABELS)]
                / totals.loc[location, ("max_llh", side, LABELS)]
            ),
            width=0.4,
            color=COLORS["blue" if location == "larynx" else "orange"],
            hatch="///",
            label=f"{location} (with midline extension)",
            zorder=10,
        )

    axes.set_xticks(np.arange(len(LABELS)))
    axes.set_xticklabels(LABELS)
    xlims = axes.get_xlim()
    axes.set_xlim(xlims[::-1])
    axes.set_yticks(np.linspace(0, 25, 6))
    axes.set_xlabel("Lymph Node Level")
    axes.set_ylabel("Prevalence of Involvement [%]")
    axes.set_title("Contralateral Involvement by Midline Extension")
    axes.legend(labelspacing=0.15, fontsize="small")
    axes.grid(visible=True, axis="y", alpha=0.5, color=COLORS["gray"])

    plt.savefig("contra_by_midext.png")
