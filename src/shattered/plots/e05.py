"""E5 figures: F6 (val BPB and minimal-pair accuracy vs tokens per word, seeds shown) and F6b (learning curves).
Reads only results/e05_pretrain/{analysis.json, curves.parquet}."""
from __future__ import annotations

import json

import matplotlib.pyplot as plt
import pandas as pd

from ..runlog import REPO
from . import style

RES = REPO / "results" / "e05_pretrain"
VOCABS = [256, 384, 512, 768, 1024, 4096]


def f6_final() -> list:
    a = json.load(open(RES / "analysis.json"))
    runs, t6 = pd.DataFrame(a["runs"]), pd.DataFrame(a["T6"])
    style.apply()
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0))
    for ax, col, mean, sd, lab in ((axes[0], "val_bpb", "val_bpb_mean", "val_bpb_sd", "Validation bits per byte"),
                                   (axes[1], "mp_all", "mp_all_mean", "mp_all_sd", "Minimal-pair accuracy (n = 472)")):
        ax.plot(t6.tokens_per_word, t6[mean], color=style.PALETTE[0], linewidth=1.5, zorder=1)
        ax.errorbar(t6.tokens_per_word, t6[mean], yerr=t6[sd], fmt="none", ecolor=style.INK_MUTED, elinewidth=1)
        for k, s in enumerate(sorted(runs.seed.unique())):
            r = runs[runs.seed == s]
            ax.plot(r.tokens_per_word, r[col], linestyle="none", marker=style.MARKERS[k + 1], markersize=5,
                    color=style.PALETTE[k + 1], markeredgecolor=style.SURFACE, markeredgewidth=0.6, label=f"seed {s}")
        for _, r in t6.iterrows():
            ax.annotate(f"{int(r.vocab)}", (r.tokens_per_word, r[mean]), textcoords="offset points", xytext=(4, 6),
                        fontsize=7, color=style.INK_MUTED)
        ax.set_xlabel("Tokens per word (TinyStories validation)")
        ax.set_title(lab, loc="left")
    axes[1].legend(fontsize=7, loc="lower left")
    fig.suptitle("F6. Same text, different fragmentation (labels: vocabulary size; bars: seed sd)", x=0.01,
                 ha="left", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    return style.save(fig, "F6_e05_fragmentation")


def f6b_curves() -> list:
    c = pd.read_parquet(RES / "curves.parquet")
    style.apply()
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.1), sharex=True)
    for k, v in enumerate(VOCABS):
        g = c[c.vocab == v].groupby("step").agg(bytes_seen=("bytes_seen", "mean"), bpb=("val_bpb_subset", "mean"),
                                                mp=("mp_all", "mean")).reset_index()
        for ax, col in ((axes[0], "bpb"), (axes[1], "mp")):
            ax.plot(g.bytes_seen / 1e6, g[col], color=style.PALETTE[k], linewidth=1.5, marker=style.MARKERS[k],
                    markevery=6, markersize=4, label=str(v))
    axes[0].set_ylim(0.5, 1.1)
    axes[0].set_ylabel("Validation BPB (2 MB subset)")
    axes[1].set_ylabel("Minimal-pair accuracy")
    for ax in axes:
        ax.set_xlabel("Training text seen (MB)")
    axes[1].legend(title="vocab", fontsize=7, title_fontsize=7, ncol=2, loc="lower right")
    fig.suptitle("F6b. Learning curves (mean of 3 seeds)", x=0.01, ha="left", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    return style.save(fig, "F6b_e05_curves")


def bpb_gap_table() -> pd.DataFrame:
    """BPB gap of each vocabulary vs vocab 4096 over training, at equal text seen and at equal training FLOPs. Each
    run's eval curve is interpolated onto a shared grid (linear in bytes; log-spaced in FLOPs) spanning the range every
    run covers. Seed means; the band is sqrt(sd_v^2 + sd_4096^2) across seeds. Written to results/e05_pretrain/."""
    import numpy as np
    c = pd.read_parquet(RES / "curves.parquet")
    runs = c.groupby(["vocab", "seed"])
    grids = {"bytes": np.linspace(runs.bytes_seen.min().max(), runs.bytes_seen.max().min(), 40),
             "flops": np.geomspace(runs.flops.min().max(), runs.flops.max().min(), 40)}
    rows = []
    for (v, s), g in runs:
        for axis, col in (("bytes", "bytes_seen"), ("flops", "flops")):
            g = g.sort_values(col)
            for x, y in zip(grids[axis], np.interp(grids[axis], g[col], g.val_bpb_subset)):
                rows.append({"vocab": v, "seed": s, "axis": axis, "x": x, "bpb": y})
    m = pd.DataFrame(rows).groupby(["axis", "vocab", "x"]).bpb.agg(["mean", "std"]).reset_index()
    ref = m[m.vocab == 4096].set_index(["axis", "x"])
    m = m.join(ref[["mean", "std"]], on=["axis", "x"], rsuffix="_4096")
    m["gap"] = m["mean"] - m["mean_4096"]
    m["gap_band"] = np.sqrt(m["std"] ** 2 + m["std_4096"] ** 2)
    m.to_csv(RES / "bpb_gap_over_training.csv", index=False)
    return m


def f6c_gap() -> list:
    m = bpb_gap_table()
    style.apply()
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.1), sharey=True)
    for k, v in enumerate(VOCABS[:-1]):
        for ax, axis, scale in ((axes[0], "bytes", 1e6), (axes[1], "flops", 1.0)):
            g = m[(m.vocab == v) & (m.axis == axis)].sort_values("x")
            ax.plot(g.x / scale, g.gap, color=style.PALETTE[k], linewidth=1.5, marker=style.MARKERS[k],
                    markevery=max(1, len(g) // 6), markersize=4, label=str(v))
            ax.fill_between(g.x / scale, g.gap - g.gap_band, g.gap + g.gap_band, color=style.PALETTE[k], alpha=0.15,
                            linewidth=0)
    for ax in axes:
        ax.set_yscale("log")
    axes[1].set_xscale("log")
    axes[0].set_xlabel("Training text seen (MB)")
    axes[1].set_xlabel("Training FLOPs (equal compute)")
    axes[0].set_ylabel("BPB gap vs vocab 4096")
    axes[0].set_title("Equal text", loc="left")
    axes[1].set_title("Equal compute", loc="left")
    axes[0].legend(title="vocab", fontsize=7, title_fontsize=7, ncol=3, loc="upper right")
    fig.suptitle("F6c. BPB gap to vocab 4096 over training (mean of 3 seeds; band: combined seed sd)", x=0.01,
                 ha="left", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    return style.save(fig, "F6c_e05_bpb_gap")
