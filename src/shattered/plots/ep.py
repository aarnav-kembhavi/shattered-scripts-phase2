"""E-P1 / E-P2 recovery curves R(P) with bootstrap 95% CIs, read from results/ep{1,2}/curves.csv and predictions.json.

Rows: SIB primary items (the registered predictions; dashed line at the 0.5 threshold, dotted line at the
selection-half peak L*), SIB control items (reported), sentiment primary items (descriptive). Columns: models. Each
scheme has its own color, marker and line style, so identity never relies on color alone.
"""
from __future__ import annotations

import json

import pandas as pd

from ..runlog import REPO
from . import style
from .style import plt

MODEL_ORDER = ["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
LABEL = {"qwen3-1.7b": "Qwen3-1.7B", "qwen3.5-2b": "Qwen3.5-2B", "sarvam-1": "Sarvam-1", "gemma4-e2b": "Gemma 4 E2B"}
SCHEMES = {1: [("final", "word-final pieces"), ("all", "all pieces")],
           2: [("word", "word-final pieces"), ("read", "readout position")]}
ROWS = [("sib", "primary", "SIB, primary items"), ("sib", "control", "SIB, control items"),
        ("sentiment", "primary", "Sentiment, primary (descriptive)")]


def curves_figure(exp: int, base=None, name: str | None = None, rows=None, figsize=None, compact: bool = False) -> list:
    """rows: subset of ROWS (default all three); compact: one short row, for the paper body."""
    style.apply()
    rows = rows or ROWS
    base = base or REPO / "results" / f"ep{exp}"
    C = pd.read_csv(base / "curves.csv")
    P = json.load(open(base / "predictions.json"))["per_model"]
    fig, axes = plt.subplots(len(rows), len(MODEL_ORDER), figsize=figsize or (12, 8.2), sharey="row", squeeze=False)
    for r, (task, kind, title) in enumerate(rows):
        for c, m in enumerate(MODEL_ORDER):
            ax = axes[r][c]
            for k, (s, lab) in enumerate(SCHEMES[exp]):
                g = C[(C.model == m) & (C.task == task) & (C.kind == kind) & (C.scheme == s)].sort_values("point")
                if g.empty:
                    continue
                ax.fill_between(g.point, g.lo, g.hi, color=style.PALETTE[k], alpha=0.18, linewidth=0)
                ax.plot(g.point, g.R, color=style.PALETTE[k], marker=style.MARKERS[k], markersize=3.5,
                        linestyle="-" if k == 0 else "--", label=lab)
            for y in (0, 1):
                ax.axhline(y, color=style.INK_MUTED, linewidth=0.8)
            if r == 0:
                ax.axhline(0.5, color=style.INK_MUTED, linewidth=0.8, linestyle=":")
                ax.set_title(LABEL[m])
            if m in P:
                ax.axvline(P[m]["L_star"], color=style.INK_MUTED, linewidth=0.8, linestyle=":")
            n = int(g.n.iloc[0]) if not g.empty else 0
            ax.text(0.98, 0.04, f"n = {n}", transform=ax.transAxes, ha="right", va="bottom", fontsize=8,
                    color=style.INK_MUTED, bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=1.5))
            if c == 0:
                ax.set_ylabel(f"{title}\nrecovery R")
    h, lab = next((ax.get_legend_handles_labels() for ax in axes.flat if ax.get_legend_handles_labels()[0]), ([], []))
    fig.legend(h, lab, loc="upper center", bbox_to_anchor=(0.5, 0.97 if compact else 0.955), fontsize=8, ncol=len(h))
    fig.supxlabel("patch point (0 = embedding output; last = final residual stream before the final norm)", fontsize=9)
    if not compact:
        fig.suptitle(("E-P1: NC1 (a) canonical into (c) non-canonical" if exp == 1 else
                      "E-P2: native into lossy") + "; ratio-of-means recovery, bootstrap 95% CI; dotted vertical: L*",
                     fontsize=10, y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.84 if compact else 0.935))
    return style.save(fig, name or f"ep{exp}_recovery_curves")
