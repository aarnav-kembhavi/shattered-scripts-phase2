"""X12 contrast 1 (registered, Amendment 2): Llama-2-7B vs Ambari-7B-base-v0.1, form-specific exposure transfer.

Statistic: DiD = gain(native) - gain(ITRANS), gain = Ambari minus Llama-2, on SIB-200 (calibrated accuracy as Phase 1, n = 1,004 paired items) and on FLORES+ retrieval (unmapped, train-chosen
layer, M4b test half, n = 1,005 paired sentences). Paired bootstrap over items (10,000, seed 0), 97.5% interval (two measures): "above 0" = lower bound above 0, "below 0" = upper bound below 0.
Supported: both measures above 0; partly supported: one; refuted: neither above 0 and one below 0; inconclusive: otherwise. Reads the scored shards via results/kaggle/queue_state.json.
Output: results/phase2/x12/contrast1.json. Usage: python scripts/x12_analyse.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e0b_familiarity as e0b  # noqa: E402

from shattered.runlog import REPO, results_dir, write_json  # noqa: E402

N_BOOT, SEED = 10_000, 0
A, L = "ambari-7b-base", "llama-2-7b"
FORMS = ["english", "native", "itrans", "lossy"]


def sib_correct(d: Path, m: str) -> tuple[pd.DataFrame, dict]:
    df = pd.concat([pd.read_parquet(d / f"sib_{f}.parquet") for f in FORMS], ignore_index=True)
    df, fb = e0b.apply_calibration(df, {m: json.load(open(d / "cf.json"))})
    e0b.CHANCE.setdefault("sib", 1 / 7)
    piv = df.pivot_table(index="id", columns="form", values="pred_cal")
    lab = df.drop_duplicates("id").set_index("id").label.loc[piv.index]
    return piv.eq(lab, axis=0), {"raw_fallback_used": bool(fb.use_raw.any())}


def did(a_n, a_i, l_n, l_i) -> dict:
    d = (a_n.astype(float) - l_n.astype(float)) - (a_i.astype(float) - l_i.astype(float))
    idx = np.random.default_rng(SEED).integers(0, len(d), (N_BOOT, len(d)))
    b = d[idx].mean(1)
    lo, hi = float(np.percentile(b, 1.25)), float(np.percentile(b, 98.75))
    return {"did": float(d.mean()), "ci975": [lo, hi], "n": int(len(d)), "above_0": bool(lo > 0), "below_0": bool(hi < 0),
            "gain_native": float(a_n.mean() - l_n.mean()), "gain_itrans": float(a_i.mean() - l_i.mean())}


def gain(a, l) -> dict:
    """Ambari minus Llama-2 for one form: paired bootstrap over items, 95% interval (descriptive)."""
    d = a.astype(float) - l.astype(float)
    idx = np.random.default_rng(SEED).integers(0, len(d), (N_BOOT, len(d)))
    b = d[idx].mean(1)
    return {"gain": float(d.mean()), "ci95": [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))], "acc_ambari": float(a.mean()), "acc_llama2": float(l.mean())}


def main() -> int:
    st = json.load(open(REPO / "results" / "kaggle" / "queue_state.json"))
    assert st["precision"][A]["pass"] and st["precision"][L]["pass"], "A1-P must pass for both endpoints"
    dA, dL = REPO / st["scored"][A]["dir"], REPO / st["scored"][L]["dir"]
    cA, fA = sib_correct(dA, A)
    cL, fL = sib_correct(dL, L)
    ids = cA.index.intersection(cL.index)
    sib = did(cA.loc[ids, "native"].to_numpy(), cA.loc[ids, "itrans"].to_numpy(), cL.loc[ids, "native"].to_numpy(), cL.loc[ids, "itrans"].to_numpy())
    acc = {m: {f: float(c.loc[ids, f].mean()) for f in FORMS} for m, c in ((A, cA), (L, cL))}
    ra = {f: np.load(dA / f"retrieval_test_correct_{f}.npy") for f in ("native", "itrans")}
    rl = {f: np.load(dL / f"retrieval_test_correct_{f}.npy") for f in ("native", "itrans")}
    ret = did(ra["native"], ra["itrans"], rl["native"], rl["itrans"])
    ret["acc"] = {A: {f: float(v.mean()) for f, v in ra.items()}, L: {f: float(v.mean()) for f, v in rl.items()}}
    sib["gain_by_form"] = {f: gain(cA.loc[ids, f].to_numpy(), cL.loc[ids, f].to_numpy()) for f in FORMS}
    ret["gain_by_form"] = {f: gain(ra[f], rl[f]) for f in ("native", "itrans")}
    a1p = {m: {"pass": st["precision"][m]["pass"], "forms": json.load(open(sorted((REPO / "results" / "kaggle" / "kaggle_precision").glob(f"*/out/precision_{m}.json"))[-1]))["forms"]} for m in (A, L)}
    pos = int(sib["above_0"]) + int(ret["above_0"])
    neg = int(sib["below_0"]) + int(ret["below_0"])
    verdict = "supported" if pos == 2 else "partly supported" if pos == 1 else "refuted" if neg >= 1 else "inconclusive"
    out = {"contrast": "1: Llama-2-7B vs Ambari-7B-base-v0.1", "sib": sib, "sib_accuracy_by_form": acc, "retrieval": ret, "calibration": {A: fA, L: fL}, "a1p": a1p,
           "prediction": "native gain exceeds ITRANS gain on SIB-200 and on retrieval (DiD > 0)", "verdict": verdict,
           "rule": "supported: both measures above 0 (97.5% interval); partly supported: one; refuted: neither above 0 and one below 0; inconclusive otherwise",
           "caveat": "natural experiment on released models; native gain confounds exposure with the tokenizer extension (ITRANS tokens per word 4.69 vs 4.55); X9b is the causal test"}
    write_json(results_dir("phase2/x12") / "contrast1.json", out, {"registration": "RESULTS.md Amendment 2, X12 contrast 1"})
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
