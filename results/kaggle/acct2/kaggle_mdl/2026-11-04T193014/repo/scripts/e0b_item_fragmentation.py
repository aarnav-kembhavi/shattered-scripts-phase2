"""Exploratory (pre-registered 2026-10-15): within each model x task x form, logistic regression of item correctness
on the item's mean tokens per word, controlling for item length in characters. Uses Gate 1 scores and tokenizers
only (no model is run). Also reports the Sarvam-1 lossy/natural vs ITRANS comparison (confounded by ITRANS capitals).

Usage: python scripts/e0b_item_fragmentation.py
Outputs: results/e0b_familiarity/gate1/item_fragmentation.csv, item_fragmentation.json
"""
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

sys.path.insert(0, str(Path(__file__).parent))
from e0b_familiarity import apply_calibration, load_items  # noqa: E402

from shattered.interp.load import MODELS  # noqa: E402
from shattered.runlog import REPO, write_json  # noqa: E402

MODELS_RUN = ["qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
FORMS = ["native", "itrans", "lossy", "natural"]
ROMANIZED = {"itrans", "lossy", "natural"}
CONST_MAX = 0.95


def main() -> None:
    from transformers import AutoTokenizer
    sd = REPO / "results" / "e0b_familiarity" / "scores"
    out = REPO / "results" / "e0b_familiarity" / "gate1"
    df = pd.concat([pd.read_parquet(sd / f"{m}__{f}.parquet") for m in MODELS_RUN for f in FORMS + ["english"]],
                   ignore_index=True)
    df, _ = apply_calibration(df, {m: json.load(open(sd / f"cf_{m}.json")) for m in MODELS_RUN})
    acc = pd.read_csv(out / "accuracy.csv")
    en = acc[acc.form == "english"].set_index(["model", "task"])
    informative = {k for k, r in en.iterrows() if r.acc_cal >= r.chance + 0.05}
    items = load_items(FORMS)
    text = {(t, it["id"], f): " ".join(it["forms"][f].values())
            for t, its in items.items() for it in its for f in FORMS if f in it["forms"]}
    rows = []
    for m in MODELS_RUN:
        tok = AutoTokenizer.from_pretrained(MODELS[m], token=os.environ.get("HF_TOKEN"))
        for (t, f), g in df[df.form.isin(FORMS)].groupby(["task", "form"]):
            g = g[g.model == m]
            if (m, t) not in informative or g.empty:
                continue
            txt = [text[(t, i, f)] for i in g["id"]]
            ntok = np.array([len(tok(x, add_special_tokens=False)["input_ids"]) for x in txt])
            tpw = ntok / np.array([len(x.split()) for x in txt])
            chars = np.array([len(x) for x in txt], float)
            y = (g.pred_cal.to_numpy() == g.label.to_numpy()).astype(float)
            const = np.bincount(g.pred_cal).max() / len(g)
            row = {"model": m, "task": t, "form": f, "n": len(g), "accuracy": y.mean(), "constant_label_rate": const,
                   "tpw_mean": tpw.mean(), "tpw_sd": tpw.std(), "corr_tpw_chars": float(np.corrcoef(tpw, chars)[0, 1]),
                   "counted": bool(const < CONST_MAX)}
            try:
                X = sm.add_constant(np.column_stack([(tpw - tpw.mean()) / tpw.std(), (chars - chars.mean()) / chars.std()]))
                fit = sm.Logit(y, X).fit(disp=0)
                row.update({"coef_tpw_per_sd": fit.params[1], "se_tpw": fit.bse[1], "p_tpw": fit.pvalues[1],
                            "coef_tpw_per_token": fit.params[1] / tpw.std(), "coef_chars_per_sd": fit.params[2],
                            "p_chars": fit.pvalues[2], "fit": "ok"})
            except Exception as e:  # noqa: BLE001 - separation, singular fits: reported, not counted
                row.update({"fit": f"failed: {type(e).__name__}", "counted": False})
            rows.append(row)
    r = pd.DataFrame(rows)
    r["p_holm"] = np.nan
    for t in ("sentiment", "xnli"):
        sel = (r.task == t) & (r.fit == "ok")
        if sel.any():
            r.loc[sel, "p_holm"] = multipletests(r.loc[sel, "p_tpw"], method="holm")[1]
    r["sig_neg"] = (r.p_holm < 0.05) & (r.coef_tpw_per_sd < 0)
    r["sig_pos"] = (r.p_holm < 0.05) & (r.coef_tpw_per_sd > 0)
    r.to_csv(out / "item_fragmentation.csv", index=False)

    def verdict(sub):
        sub = sub[sub.counted]
        if sub.empty:
            return {"n_cells": 0, "verdict": "no counted cells"}
        neg = (sub.coef_tpw_per_sd < 0).mean()
        if sub.sig_pos.any() or (neg < 0.5 and not sub.sig_neg.any()):
            v = "contradicted"
        elif neg > 0.5 and sub.sig_neg.any():
            v = "supported"
        else:
            v = "no evidence"
        return {"n_cells": int(len(sub)), "frac_negative": float(neg), "n_sig_neg": int(sub.sig_neg.sum()),
                "n_sig_pos": int(sub.sig_pos.sum()), "verdict": v}
    res = {}
    for t in ("sentiment", "xnli"):
        s = r[r.task == t]
        res[t] = {"native": verdict(s[s.form == "native"]), "romanized": verdict(s[s.form.isin(ROMANIZED)])}

    # Sarvam-1 within-romanization comparison (exploratory, already seen; confounded by ITRANS capitals)
    mc = pd.read_csv(out / "mcnemar.csv")
    sarv = mc[(mc.model == "sarvam-1") & (mc.b == "itrans") & (mc.a.isin(["lossy", "natural"]))]
    fert = pd.read_csv(out / "fertility.csv")
    res["sarvam_within_romanization"] = {
        "rows": sarv[["task", "a", "b", "n", "acc_a", "acc_b", "diff", "a_only", "b_only", "p", "p_holm"]].to_dict("records"),
        "tokens_per_word": fert[fert.model == "sarvam-1"].set_index(["task", "form"]).tokens_per_word.round(2)
        .reset_index().to_dict("records"),
        "caveat": "exploratory; ITRANS uses capital letters for long vowels/retroflexes, lossy and natural do not"}
    write_json(out / "item_fragmentation.json", res, {"registered": "RESULTS.md 2026-10-15", "const_max": CONST_MAX,
                                                     "predictions": "pred_cal (avg3 calibration, raw fallback)"})
    pd.set_option("display.width", 220)
    print(r[["model", "task", "form", "n", "accuracy", "constant_label_rate", "tpw_mean", "corr_tpw_chars",
             "coef_tpw_per_sd", "p_tpw", "p_holm", "counted", "fit"]].round(3).to_string(index=False))
    print(json.dumps({k: v for k, v in res.items() if k != "sarvam_within_romanization"}, indent=1))


if __name__ == "__main__":
    main()
