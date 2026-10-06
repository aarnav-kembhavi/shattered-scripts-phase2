"""E1 figures: F1 (tax ratio by language and tokenizer), F1b (drift across tokenizer generations),
F1c (Kannada native vs ITRANS vs lossy per tokenizer). Read only from results/e01_cost/."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

from ..runlog import REPO
from . import style

RES = REPO / "results" / "e01_cost"
LANG_NAMES = {"kan_Knda": "Kannada", "tam_Taml": "Tamil", "tel_Telu": "Telugu", "mal_Mlym": "Malayalam",
              "hin_Deva": "Hindi", "ben_Beng": "Bangla"}
# One representative per distinct tokenizer (identical tokenizers share counts; see results/e01_cost)
F1_TOKENIZERS = [
    ("r50k_base", "r50k (GPT-3)"), ("cl100k_base", "cl100k (GPT-4)"), ("o200k_base", "o200k (GPT-4o)"),
    ("TinyLlama/TinyLlama-1.1B-Chat-v1.0", "Llama 2"), ("Qwen/Qwen3-8B", "Qwen 1.5–3"),
    ("Qwen/Qwen3.5-9B", "Qwen 3.5–3.8"), ("google/gemma-4-E2B-it", "Gemma 4"), ("sarvamai/sarvam-1", "Sarvam-1"),
]
DRIFT_FAMILIES = ["OpenAI", "Qwen", "Sarvam", "Phi", "Mistral"]


def _log_ratio_axis(ax, axis="y", ticks=(1, 1.5, 2, 3, 5, 10, 15)) -> None:
    setter = ax.set_yscale if axis == "y" else ax.set_xscale
    setter("log")
    a = ax.yaxis if axis == "y" else ax.xaxis
    a.set_major_locator(FixedLocator(ticks))
    a.set_minor_locator(NullLocator())
    a.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}×"))


def f1_tax_by_language(summary: pd.DataFrame | None = None) -> list:
    s = pd.read_parquet(RES / "summary.parquet") if summary is None else summary
    s = s[s.form == "native"]
    style.apply()
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    langs = list(LANG_NAMES)
    width = 0.8 / len(F1_TOKENIZERS)
    for k, (tk, label) in enumerate(F1_TOKENIZERS):
        d = s[s.tokenizer == tk].set_index("lang").loc[langs]
        x = np.arange(len(langs)) - 0.4 + width * (k + 0.5)
        ax.errorbar(x, d.tax_ratio, yerr=[d.tax_ratio - d.tax_ci_low, d.tax_ci_high - d.tax_ratio], fmt="none",
                    ecolor=style.INK_MUTED, elinewidth=0.8)
        ax.plot(x, d.tax_ratio, linestyle="none", marker=style.MARKERS[k], color=style.PALETTE[k],
                markeredgecolor=style.SURFACE, markeredgewidth=0.8, markersize=7, label=label)
    ax.axhline(1, color=style.INK_MUTED, linewidth=1, linestyle="--")
    ax.text(-0.45, 1.03, "English parity", color=style.INK_MUTED, ha="left", va="bottom", fontsize=8)
    _log_ratio_axis(ax)
    ax.set_xticks(range(len(langs)), [LANG_NAMES[lang] for lang in langs])
    ax.grid(axis="x", visible=False)
    ax.set_ylabel("Tokens relative to English\n(same FLORES sentences)")
    ax.set_title("F1. The language tax: native-script token cost relative to English", loc="left")
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.12), fontsize=8, handletextpad=0.3)
    n = int(s.n_sentences.iloc[0])
    fig.text(0.01, -0.13, f"n = {n} FLORES-200 dev+devtest sentences per language; bars = paired bootstrap 95% CI "
             "(10,000 resamples; mostly narrower than markers).", fontsize=7, color=style.INK_MUTED)
    return style.save(fig, "F1_tax_by_language")


def f1b_drift(summary: pd.DataFrame | None = None) -> list:
    s = pd.read_parquet(RES / "summary.parquet") if summary is None else summary
    s = s[(s.form == "native") & s.family.isin(DRIFT_FAMILIES)].copy()
    s["date"] = pd.to_datetime(s.released.astype(str))
    style.apply()
    langs = list(LANG_NAMES)
    fig, axes = plt.subplots(2, 3, figsize=(7.4, 4.6), sharex=True, sharey=True)
    for ax, lang in zip(axes.flat, langs):
        for k, fam in enumerate(DRIFT_FAMILIES):
            d = s[(s.family == fam) & (s.lang == lang)].sort_values("date").drop_duplicates("date")
            ax.plot(d.date, d.tax_ratio, color=style.PALETTE[k], marker=style.MARKERS[k], markersize=5,
                    markeredgecolor=style.SURFACE, markeredgewidth=0.6, label=fam)
        ax.axhline(1, color=style.INK_MUTED, linewidth=1, linestyle="--")
        _log_ratio_axis(ax, ticks=(1, 2, 3, 5, 10, 15))
        ax.set_title(LANG_NAMES[lang], loc="left")
        ax.tick_params(axis="x", labelrotation=0, labelsize=7)
    for ax in axes[:, 0]:
        ax.set_ylabel("Tax vs English")
    fig.suptitle("F1b. Tokenizer drift: the tax across generations of each family (native script)", x=0.01,
                 ha="left", fontsize=10)
    handles, labels = axes.flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, ncol=5, loc="lower center", bbox_to_anchor=(0.5, -0.04), fontsize=8)
    fig.text(0.01, -0.08, "x = tokenizer release (repo creation month). Same-date duplicates dropped. "
             "Llama 3 / Gemma 2–3 tokenizers are gated and not yet included.", fontsize=7, color=style.INK_MUTED)
    fig.tight_layout(rect=(0, 0.04, 1, 0.97))
    return style.save(fig, "F1b_tax_drift")


def f1c_forms_kannada(summary: pd.DataFrame | None = None) -> list:
    s = pd.read_parquet(RES / "summary.parquet") if summary is None else summary
    keep = dict(F1_TOKENIZERS)
    k = s[(s.lang == "kan_Knda") & s.tokenizer.isin(keep)].pivot_table(index="tokenizer", columns="form",
                                                                        values="tax_ratio")
    k = k.sort_values("native")
    style.apply()
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    y = np.arange(len(k))
    for i, tk in enumerate(k.index):
        lo, hi = k.loc[tk].min(), k.loc[tk].max()
        ax.plot([lo, hi], [i, i], color=style.GRID, linewidth=2, zorder=1)
    forms = [("native", "Native Kannada script"), ("itrans", "ITRANS (lossless)"), ("lossy", "Lossy romanization")]
    for j, (f, label) in enumerate(forms):
        ax.plot(k[f], y, linestyle="none", marker=style.MARKERS[j], color=style.PALETTE[j], markersize=7,
                markeredgecolor=style.SURFACE, markeredgewidth=0.8, label=label, zorder=2)
    ax.set_yticks(y, [keep[t] for t in k.index])
    ax.grid(axis="y", visible=False)
    _log_ratio_axis(ax, axis="x", ticks=(1, 1.5, 2, 3, 5, 10, 15))
    ax.axvline(1, color=style.INK_MUTED, linewidth=1, linestyle="--")
    ax.set_xlabel("Tokens relative to English (same FLORES sentences)")
    ax.set_title("F1c. Romanization only saves tokens on older tokenizers (Kannada)", loc="left")
    ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.18), fontsize=8)
    return style.save(fig, "F1c_kannada_forms")


def all_figures() -> list:
    return f1_tax_by_language() + f1b_drift() + f1c_forms_kannada()
