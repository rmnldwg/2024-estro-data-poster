"""
Venn diagram.
"""
from itertools import product
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
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


def prepare_venn_data(ipsi: pd.DataFrame):
    """Prepare data for Venn diagram."""
    venn_data = {}
    for lnl_II, lnl_III, lnl_IV in product([True, False], repeat=3):
        venn_data[(lnl_II, lnl_III, lnl_IV)] = len(
            ipsi.loc[
                (ipsi["II"] == lnl_II) & (ipsi["III"] == lnl_III) & (ipsi["IV"] == lnl_IV)
            ]
        )

    return venn_data


def plot_venn_diagram(ipsi, venn, venn_data):
    """Plot Venn diagram."""
    return venn3(
        subsets=(
            venn_data[(True, False, False)],
            venn_data[(False, True, False)],
            venn_data[(True, True, False)],
            venn_data[(False, False, True)],
            venn_data[(True, False, True)],
            venn_data[(False, True, True)],
            venn_data[(True, True, True)],
        ),
        set_labels=("LNL II\ninvolved", "LNL III\ninvolved", "LNL IV\ninvolved"),
        set_colors=(COLORS["orange"], COLORS["red"], COLORS["blue"]),
        alpha=0.6,
        subset_label_formatter=lambda x: f"{x}\n({x/len(ipsi):.0%})",
        ax=venn,
    )


if __name__ == "__main__":
    data = pd.read_csv("enhanced.csv", header=[0,1,2])
    side = "ipsi"
    location = "larynx"

    subdata = data.loc[
        data["tumor", "1", "location"] == location,
        ("max_llh", side)
    ]
    venn_data = prepare_venn_data(subdata)
    venn_plot = plot_venn_diagram(subdata, plt.gca(), venn_data)
    plt.savefig("venn_larynx.png", dpi=300)
