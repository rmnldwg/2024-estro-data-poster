"""
Variables and other stuff used accross the project.
"""
import argparse
from collections import namedtuple
from pathlib import Path

FIGURES = Path("figures")
DATA = Path("data")

LNLS = ["I", "II", "III", "IV", "V", "VI", "VII"][::-1]
COLORS = {
    "green": "#00afa5",
    "blue": "#005ea8", 
    "gray": "#c5d5db",
    "orange": "#f17900",
    "red": "#ae0060",
}
lyDataColumns = namedtuple("lyDataColumns", ["t_stage", "location", "midext", "subsite"])
COLS = lyDataColumns(
    t_stage=("tumor", "1", "t_stage"),
    location=("tumor", "1", "location"),
    midext=("tumor", "1", "extension"),
    subsite=("tumor", "1", "subsite"),
)

def lnls_for_(side: str) -> tuple[str, str, list[str]]:
    """Return a pandas multiindex tuple for the given side."""
    return ("max_llh", side, LNLS)


def create_parser(file_name: str, description: str) -> argparse.ArgumentParser:
    """Create a simple parser for in- and output files."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=DATA / "enhanced.csv",
        help="Input file with the data.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=(FIGURES / file_name).with_suffix(".png"),
        help="Output file for the plot.",
    )
    return parser


WIDTH = 0.5
OFFSET = WIDTH / 2


def make_invisible(both_axes):
    """Make the axes invisible."""
    for loc in ["top", "bottom", "left", "right"]:
        both_axes.spines[loc].set_visible(False)
    both_axes.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)
