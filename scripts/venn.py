"""
Create a Venn diagram of co-involvement in the LNLs II, III, and IV.
"""
from itertools import product
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import pandas as pd

from shared import LNLS, COLORS, create_parser


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
    parser = create_parser(file_name=Path(__file__).stem, description=__doc__)
    args = parser.parse_args()

    data = pd.read_csv(args.input, header=[0,1,2])

    for side in ["ipsi", "contra"]:
        for location in ["hypopharynx", "larynx"]:
            subdata = data.loc[
                data["tumor", "1", "location"] == location,
                ("max_llh", side)
            ]
            venn_data = prepare_venn_data(subdata)
            venn_plot = plot_venn_diagram(subdata, plt.gca(), venn_data)
            output = args.output.with_name(f"venn_{location}_{side}.png")
            plt.savefig(output, dpi=300)
            plt.clf()
