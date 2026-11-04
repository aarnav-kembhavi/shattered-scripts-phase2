"""X13 analysis for a Kaggle-scored 7-9B model (default Qwen3-8B), Phase 1 standards (Amendment 2, A0 and X13). Reads the shards written by scripts/x_score.py.

1. Counting rule (A0/X13): the model is counted only if its native SIB-200 accuracy (calibrated as Phase 1: mean of the three content-free inputs, raw fallback if English drops more than
   5 points) has a 95% bootstrap CI lower bound above 0.40, and A1-P passed (read from results/kaggle/queue_state.json).
2. SIB-200 accuracy per form with 95% CIs (n = 1,004; natural on the 257 items with a clean draft), and the Phase 1 P-a contrasts native - ITRANS and native - lossy (exact McNemar on paired
   per-item correctness). The extended P-a reading enlarges the counted accuracy set (Phase 1: Qwen3-1.7B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B; Qwen2.5 never counted) by this model and applies
   the all-but-one rule: a contrast is "supported" if it is positive and significant (Holm over the extended family of native-vs-ITRANS and native-vs-lossy tests) in at least n - 1 of the n counted
   models, "refuted" if it is significantly negative in any counted model or in none is significant, "partly supported" otherwise. Reported separately; the Phase 1 verdicts do not change.
3. Retrieval (unmapped, M4b test half, n = 1,005): native and ITRANS acc@1 at the train-chosen layer, the paired bootstrap difference (10,000, seed 0), and the same for the three Phase 1
   counted retrieval models (Qwen3.5-2B, Sarvam-1, Gemma 4 E2B; `results/m4b_mapping/items.npz`); the extended count of models whose native - ITRANS difference has a 95% CI above 0
   (all-but-one rule: at least n - 1 of n).
Output: results/phase2/x13/<model>/analysis.json. Usage: python scripts/x13_analyse.py [--model qwen3-8b]
"""
import argparse
import glob
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.multitest import multipletests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e0b_familiarity as e0b  # noqa: E402

from shattered.runlog import REPO, results_dir, write_json  # noqa: E402

N_BOOT = 10_000
PHASE1_ACC = ["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
PHASE1_RET = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
CHANCE = 1 / 7


def paired_ci(a: np.ndarray, b: np.ndarray) -> dict:
    d = a.astype(float) - b.astype(float)
    idx = np.random.default_rng(0).integers(0, len(d), (N_BOOT, len(d)))
    m = d[idx].mean(1)
    return {"diff": float(d.mean()), "ci95": [float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))], "n": int(len(d))}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen3-8b")
    a = ap.parse_args()
    m = a.model
    state = json.load(open(REPO / "results" / "kaggle" / "queue_state.json"))
    d = REPO / state["scored"][m]["dir"]
    forms = {"english": "english", "native": "native", "itrans": "itrans", "lossy": "lossy", "lower": "lower", "natural": "natural257"}
    df = pd.concat([pd.read_parquet(d / f"sib_{f}.parquet") for f in forms], ignore_index=True)
    df, fb = e0b.apply_calibration(df, {m: json.load(open(d / "cf.json"))})
    e0b.CHANCE.setdefault("sib", CHANCE)  # as scripts/e0c_sib.py does for the SIB-200 tables
    acc = e0b.accuracy_table(df)
    out = {"model": m, "dtype": "float16 (A1-P passed: %s)" % state["precision"][m]["pass"], "raw_fallback_used": bool(fb.use_raw.any()), "english_accuracy_calibrated": None, "accuracy": {}}
    for r in acc.itertuples():
        out["accuracy"][r.form] = {"n": int(r.n), "acc_cal": float(r.acc_cal), "ci95": [float(r.acc_cal_ci_low), float(r.acc_cal_ci_high)], "acc_raw": float(r.acc_raw)}
    out["english_accuracy_calibrated"] = out["accuracy"]["english"]["acc_cal"]
    nat = out["accuracy"]["native"]
    out["counted"] = {"native_ci_lower": nat["ci95"][0], "rule": "native CI lower bound > 0.40 and A1-P passed", "counted": bool(nat["ci95"][0] > 0.40 and state["precision"][m]["pass"]),
                      "informative_english_above_chance_plus_5": bool(out["english_accuracy_calibrated"] >= CHANCE + 0.05)}
    # P-a contrasts for this model
    mc_new = e0b.mcnemar_table(df, [("native", "itrans"), ("native", "lossy")])
    out["P_a_this_model"] = mc_new.drop(columns=["p_holm", "significant"]).to_dict("records")
    # extended family: Phase 1 counted models (their stored raw p) + this model
    v1 = json.load(open(REPO / "results" / "e0c_sib" / "gate" / "verdicts.json"))
    rows = [t for t in v1["P_a_tests"] if t["model"] in PHASE1_ACC]
    for r in mc_new.itertuples():
        rows.append({"model": r.model, "a": r.a, "b": r.b, "diff": float(r.diff), "p": float(r.p)})
    ph = multipletests([t["p"] for t in rows], method="holm")[1]
    for t, p in zip(rows, ph):
        t["p_holm_extended"], t["significant_extended"] = float(p), bool(p < 0.05)
    out["P_a_extended_tests"] = [{k: t[k] for k in ("model", "a", "b", "diff", "p", "p_holm_extended", "significant_extended")} for t in rows]
    ext = {}
    for b in ("itrans", "lossy"):
        ts = [t for t in rows if t["b"] == b]
        n = len(ts)
        pos = sum(1 for t in ts if t["diff"] > 0 and t["significant_extended"])
        neg = sum(1 for t in ts if t["diff"] < 0 and t["significant_extended"])
        ext[f"native_vs_{b}"] = {"n_models": n, "positive_and_significant": pos, "significantly_negative": neg,
                                 "verdict": "supported" if pos >= n - 1 and neg == 0 else "refuted" if neg > 0 or pos == 0 else "partly supported"}
    out["P_a_extended"] = ext
    # retrieval
    rj = json.load(open(d / "retrieval.json"))
    nat_ok, it_ok = np.load(d / "retrieval_test_correct_native.npy"), np.load(d / "retrieval_test_correct_itrans.npy")
    ret = {m: {"native": float(nat_ok.mean()), "itrans": float(it_ok.mean()), **paired_ci(nat_ok, it_ok), "layer_native": rj["forms"]["native"]["layer"],
               "layer_itrans": rj["forms"]["itrans"]["layer"]}}
    z = np.load(REPO / "results" / "m4b_mapping" / "items.npz", allow_pickle=True)
    for mm in PHASE1_RET:
        n_ = z[f"{mm}__native__unmapped"][int(z[f"{mm}__native__best"][1])]  # per-layer arrays [layers, n]; best[1] = the train-chosen unmapped layer
        i_ = z[f"{mm}__itrans__unmapped"][int(z[f"{mm}__itrans__best"][1])]
        ret[mm] = {"native": float(n_.mean()), "itrans": float(i_.mean()), **paired_ci(n_, i_)}
    n_models = len(ret)
    n_pos = sum(1 for v in ret.values() if v["ci95"][0] > 0)
    out["retrieval"] = ret
    out["retrieval_extended"] = {"n_models": n_models, "native_minus_itrans_ci_above_0": n_pos, "all_but_one_met": bool(n_pos >= n_models - 1)}
    out["scoring"] = {"hours": state["scored"][m]["hours"], "dir": state["scored"][m]["dir"]}
    path = results_dir(f"phase2/x13/{m}") / "analysis.json"
    write_json(path, out, {"registration": "RESULTS.md Amendment 2, A0 and X13", "reading": "extended verdicts use the all-but-one rule (at least n - 1 of n); Phase 1 verdicts unchanged"})
    print(json.dumps({"counted": out["counted"], "accuracy": {k: (round(v["acc_cal"], 3), [round(x, 3) for x in v["ci95"]]) for k, v in out["accuracy"].items()},
                      "P_a_this_model": [(r["b"], round(r["acc_a"], 3), round(r["acc_b"], 3), round(r["diff"], 3), r["p"]) for r in out["P_a_this_model"]],
                      "P_a_extended": ext, "retrieval": {k: (round(v["native"], 3), round(v["itrans"], 3), [round(x, 3) for x in v["ci95"]]) for k, v in ret.items()},
                      "retrieval_extended": out["retrieval_extended"]}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
