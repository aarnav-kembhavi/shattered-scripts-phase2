"""M1/M4 draft figure: per model, MDL compression (fraction of its maximum) by layer for English, native and ITRANS,
and FLORES+ retrieval accuracy@1 against English for native and ITRANS. Reads results/m14_full/gate2/verdicts.json
(curves copied there from the per-model result files)."""
from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np

from ..runlog import REPO
from . import style

NAMES = {"qwen2.5-1.5b": "Qwen2.5-1.5B", "qwen3.5-2b": "Qwen3.5-2B", "sarvam-1": "Sarvam-1", "gemma4-e2b": "Gemma 4 E2B"}
FORM_STYLE = {"english": (0, "-", "English"), "native": (1, "-", "Native Kannada"), "itrans": (2, "--", "ITRANS")}


def layer_curves(curves: dict | None = None) -> list:
    if curves is None:
        curves = json.load(open(REPO / "results" / "m14_full" / "gate2" / "verdicts.json"))["curves"]
    style.apply()
    models = list(curves)
    fig, axes = plt.subplots(len(models), 2, figsize=(7.2, 2.0 * len(models)), sharex="row")
    for r, m in enumerate(models):
        L = curves[m]["L"]
        for f, comp in curves[m]["mdl"].items():
            i, ls, lab = FORM_STYLE[f]
            c = np.asarray(comp)
            axes[r, 0].plot(range(L + 1), c / c.max(), ls, color=style.PALETTE[i], marker=style.MARKERS[i],
                            markevery=4, label=lab)
        for f, acc in curves[m]["retrieval"].items():
            i, ls, lab = FORM_STYLE[f]
            axes[r, 1].plot(range(L + 1), acc, ls, color=style.PALETTE[i], marker=style.MARKERS[i], markevery=4,
                            label=lab)
        axes[r, 0].set_ylabel(NAMES.get(m, m))
        axes[r, 1].set_ylim(0, 1)
    axes[0, 0].set_title("MDL compression / max (word identity)")
    axes[0, 1].set_title("FLORES+ retrieval acc@1 vs English")
    for a in axes[-1]:
        a.set_xlabel("layer")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    h, lab = axes[0, 0].get_legend_handles_labels()
    fig.legend(h, lab, loc="lower center", ncol=3, fontsize=8)
    return style.save(fig, "F_m14_layer_curves_draft")


def accuracy_vs_mechanism() -> list:
    """Illustrative (n = 8: 4 models x {native, ITRANS}): E0 sentiment accuracy (Gate 1 primary, 95% CI) against
    tokens per word (E0 sentiment texts), best-layer FLORES+ retrieval vs English (unmapped, all 2,009 sentences) and
    best-layer mapped retrieval (M4b ridge map, test half). Reads Gate 1, Gate 2 and M4b result files."""
    import pandas as pd
    g1 = REPO / "results" / "e0b_familiarity" / "gate1"
    acc = pd.read_csv(g1 / "accuracy.csv")
    acc = acc[(acc.task == "sentiment")].set_index(["model", "form"])
    fert = pd.read_csv(g1 / "fertility.csv")
    fert = fert[fert.task == "sentiment"].set_index(["model", "form"]).tokens_per_word
    m4 = json.load(open(REPO / "results" / "m14_full" / "gate2" / "verdicts.json"))["curves"]
    mb = pd.read_csv(REPO / "results" / "m4b_mapping" / "summary.csv").set_index(["model", "form"])
    style.apply()
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.6), sharey=True)
    xs = [("tokens per word (E0 sentiment)", lambda m, f: fert[(m, f)]),
          ("best-layer retrieval vs English", lambda m, f: max(m4[m]["retrieval"][f])),
          ("best-layer retrieval, linear map", lambda m, f: mb.loc[(m, f), "mapped"])]
    for j, (lab, fx) in enumerate(xs):
        ax = axes[j]
        for i, m in enumerate(NAMES):
            pts = []
            for f, filled in (("native", True), ("itrans", False)):
                r = acc.loc[(m, f)]
                x, y = fx(m, f), 100 * r.acc_cal
                pts.append((x, y))
                ax.errorbar(x, y, yerr=[[y - 100 * r.acc_cal_ci_low], [100 * r.acc_cal_ci_high - y]], fmt=style.MARKERS[i],
                            color=style.PALETTE[i], mfc=style.PALETTE[i] if filled else style.SURFACE, mew=1.5,
                            elinewidth=0.8, capsize=0, label=f"{NAMES[m]}" if (j == 0 and filled) else None)
            ax.plot(*zip(*pts), ":", color=style.PALETTE[i], linewidth=1)
        ax.set_xlabel(lab)
    axes[0].set_ylabel("sentiment accuracy (%)")
    axes[1].set_xlim(0, 1)
    axes[2].set_xlim(0, 1)
    fig.suptitle("Illustrative only (n = 8). Filled = native script, hollow = ITRANS; dotted lines join a model's two forms",
                 fontsize=8, y=1.02)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, fontsize=8)
    return style.save(fig, "F_m14_accuracy_vs_mechanism_illustrative")
