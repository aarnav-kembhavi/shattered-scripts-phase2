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
