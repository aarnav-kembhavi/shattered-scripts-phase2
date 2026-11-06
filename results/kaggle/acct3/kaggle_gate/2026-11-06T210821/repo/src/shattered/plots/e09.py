"""E9 figure F8: tokens relative to native Kannada, per tokenizer, for ITRANS and the best searched schemes.
Reads only results/e09_romanize/savings.csv."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..runlog import REPO
from . import style

RES = REPO / "results" / "e09_romanize"
FORMS = [("e09:universal|lower", "Searched, lowercase-only (universal)"),
         ("e09:universal|free", "Searched, free (universal)"), ("own", "Searched for this tokenizer (free)")]
OWN = {"o200k (GPT-4o)": "e09:o200k|free", "Gemma 4": "e09:gemma4|free", "Qwen 3.5-3.8": "e09:qwen3.5|free",
       "Qwen 1.5-3": "e09:qwen3|free"}


def f8_savings() -> list:
    d = pd.read_csv(RES / "savings.csv")
    toks = d[d.form == "e09:universal|free"].sort_values("vs_itrans").tokenizer.tolist()
    style.apply()
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    y = np.arange(len(toks))
    for j, (form, label) in enumerate(FORMS):
        xs, ys = [], []
        for i, tk in enumerate(toks):
            f = OWN.get(tk) if form == "own" else form
            row = d[(d.tokenizer == tk) & (d.form == f)] if f else None
            if row is not None and len(row):
                xs.append(float(row.vs_itrans.iloc[0]))
                ys.append(i)
        ax.plot(xs, ys, linestyle="none", marker=style.MARKERS[j], color=style.PALETTE[j], markersize=7,
                markeredgecolor=style.SURFACE, markeredgewidth=0.8, label=label, zorder=2)
    for x, lab in ((1.0, "ITRANS"), (0.95, "failure line (5% saving)"), (0.90, "predicted (10% saving)")):
        ax.axvline(x, color=style.INK_MUTED, linewidth=1, linestyle="--" if x == 1 else ":")
        ax.text(x - 0.002, len(toks) - 0.4, lab, color=style.INK_MUTED, fontsize=7, ha="right", va="bottom")
    ax.set_yticks(y, toks)
    ax.set_ylim(-0.6, len(toks) + 0.4)
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0.88, 1.09)
    ax.set_xlabel("Tokens relative to ITRANS (FLORES+ Kannada, held out; lower is cheaper)")
    ax.set_title("F8. Token savings of searched reversible romanizations over ITRANS", loc="left")
    ax.legend(ncol=2, loc="upper center", bbox_to_anchor=(0.45, -0.14), fontsize=8)
    return style.save(fig, "F8_e09_savings")
