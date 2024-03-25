"""
Figures and plots for 2024 ESTRO poster on Hypopharynx/Larynx dataset.
"""
from matplotlib import gridspec
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
    data["tumor", "1", "t_stage"] = data["tumor", "1", "t_stage"].apply(
        lambda x: "early" if x <= 2 else "late"
    )

    by_level = 100 * data.groupby(
        by=[("tumor", "1", "t_stage"), ("tumor", "1", "location")]
    ).sum()
    totals = data.groupby(
        by=[("tumor", "1", "location")],
    ).count()

    fig = plt.figure()
    gs = gridspec.GridSpec(nrows=1, ncols=2, width_ratios=[1, 1], wspace=0.15)
    both_axes = fig.add_subplot(gs[:])
    left_axes = fig.add_subplot(gs[0])
    right_axes = fig.add_subplot(gs[1], sharey=left_axes)
    axes = [left_axes, right_axes]

    for j, location in enumerate(["hypopharynx", "larynx"]):
        for i, side in enumerate(["contra", "ipsi"]):
            axes[i].barh(
                np.arange(len(LABELS)) - 0.2 + j * 0.4,
                width=(
                    by_level.loc[("early", location), ("max_llh", side, LABELS)]
                    / totals.loc[location, ("max_llh", side, LABELS)]
                ),
                height=0.4,
                color=COLORS["blue" if location == "larynx" else "orange"],
                label=f"{location} (early)",
                zorder=10,
            )
            axes[i].barh(
                np.arange(len(LABELS)) - 0.2 + j * 0.4,
                width=(
                    by_level.loc[("late", location), ("max_llh", side, LABELS)]
                    / totals.loc[location, ("max_llh", side, LABELS)]
                ),
                left=(
                    by_level.loc[("early", location), ("max_llh", side, LABELS)]
                    / totals.loc[location, ("max_llh", side, LABELS)]
                ),
                height=0.4,
                color=COLORS["blue" if location == "larynx" else "orange"],
                hatch="///",
                label=f"{location} (late)",
                zorder=10,
            )
            axes[i].set_yticks(np.arange(len(LABELS)))
            axes[i].set_yticklabels(LABELS)
            axes[i].set_xticks(np.linspace(0, 60, 7))
            axes[i].legend(labelspacing=0.15, fontsize="small")
            axes[i].grid(visible=True, axis="x", alpha=0.5, color=COLORS["gray"])

    axes[0].yaxis.tick_right()
    plt.setp(axes[1].get_yticklabels(), visible=False)
    xlim = axes[1].get_xlim()
    axes[0].set_xlim(xlim[::-1])
    both_axes.set_xlabel("Prevalence of Involvement [%]")
    both_axes.spines['top'].set_color('none')
    both_axes.spines['bottom'].set_color('none')
    both_axes.spines['left'].set_color('none')
    both_axes.spines['right'].set_color('none')
    both_axes.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)
    left_axes.set_title("contralateral")
    right_axes.set_title("ipsilateral")

    plt.savefig("ipsi_contra_involvement.png")
