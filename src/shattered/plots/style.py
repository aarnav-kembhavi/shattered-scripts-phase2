"""Shared figure style: validated colorblind-safe categorical palette (fixed order) plus marker shapes, so identity
never relies on color alone. Palette checked with the dataviz validator (light surface): all hard gates pass; slots
3, 4, 5 are below 3:1 contrast, so every series also carries a distinct marker and a table view exists (summary CSVs).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from ..runlog import REPO  # noqa: E402

PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
MARKERS = ["o", "s", "^", "D", "v", "P", "X", "h"]
SURFACE = "#fcfcfb"
INK = "#1f1f1e"
INK_MUTED = "#6b6a63"
GRID = "#e4e3dc"
FIG_DIR = REPO / "paper2" / "figures"


def apply() -> None:
    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": INK_MUTED, "axes.labelcolor": INK, "text.color": INK,
        "xtick.color": INK_MUTED, "ytick.color": INK_MUTED, "axes.grid": True, "grid.color": GRID,
        "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False, "font.size": 9,
        "axes.titlesize": 10, "legend.frameon": False, "lines.linewidth": 2, "lines.markersize": 6,
    })


def save(fig, name: str) -> list[Path]:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    paths = [FIG_DIR / f"{name}.pdf", FIG_DIR / f"{name}.png"]
    for p in paths:
        fig.savefig(p, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return paths
