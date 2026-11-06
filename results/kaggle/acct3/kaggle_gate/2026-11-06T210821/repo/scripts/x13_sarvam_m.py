"""X13 Sarvam-m (23.6B, 4-bit NF4, SIB-200 only, no retrieval, exempt from A1-P; registered): counting rule and the native - ITRANS contrast from the forms that finished before the kernel's 5 h cap
(English, native, ITRANS; lossy, lowercase and natural were not reached). Calibration as Phase 1 (mean of three content-free inputs, raw fallback if English drops more than 5 points); counted only if the
native 95% bootstrap CI lower bound is above 0.40. Native - ITRANS: exact McNemar on paired per-item correctness and the paired bootstrap difference. Extended reading (all-but-one rule on native vs ITRANS):
the five Phase 1 and X13 counted models (Qwen3-1.7B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B, Qwen3-8B, Llama-3.1-8B) plus Sarvam-m, Holm over the native-vs-ITRANS tests only (lossy was not scored for Sarvam-m).
Usage: python scripts/x13_sarvam_m.py        Output: results/phase2/x13/sarvam-m/analysis.json"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.multitest import multipletests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e0b_familiarity as e0b  # noqa: E402
import x13_analyse as X  # noqa: E402

from shattered.runlog import REPO, results_dir, write_json  # noqa: E402

M = "sarvam-m"
D = REPO / "results" / "kaggle" / "acct2" / "x_score" / "2026-11-05T051051" / "out" / M


def main() -> None:
    df = pd.concat([pd.read_parquet(D / f"sib_{f}.parquet") for f in ("english", "native", "itrans")], ignore_index=True)
    df, fb = e0b.apply_calibration(df, {M: json.load(open(D / "cf.json"))})
    e0b.CHANCE.setdefault("sib", 1 / 7)
    acc = e0b.accuracy_table(df)
    out = {"model": M, "quantization": "4-bit NF4 (exempt from A1-P)", "forms_scored": ["english", "native", "itrans"], "forms_not_reached": ["lossy", "lower", "natural"],
           "reason": "the kernel's 5 h cap hit after ITRANS (about 85 min per form)", "raw_fallback_used": bool(fb.use_raw.any()), "accuracy": {}}
    for r in acc.itertuples():
        out["accuracy"][r.form] = {"n": int(r.n), "acc_cal": float(r.acc_cal), "ci95": [float(r.acc_cal_ci_low), float(r.acc_cal_ci_high)], "acc_raw": float(r.acc_raw)}
    nat = out["accuracy"]["native"]
    out["counted"] = {"native_ci_lower": nat["ci95"][0], "rule": "native CI lower bound > 0.40", "counted": bool(nat["ci95"][0] > 0.40)}
    t = df[df.form.isin(["native", "itrans"])].pivot(index="id", columns="form", values="pred_cal")
    lab = df[df.form == "native"].set_index("id").label
    cn, ci = (t["native"] == lab.loc[t.index]).to_numpy(), (t["itrans"] == lab.loc[t.index]).to_numpy()
    b, c = int((cn & ~ci).sum()), int((~cn & ci).sum())
    p = float(mcnemar([[int((cn & ci).sum()), b], [c, int((~cn & ~ci).sum())]], exact=True).pvalue)
    out["native_minus_itrans"] = {**X.paired_ci(cn, ci), "native_only_correct": b, "itrans_only_correct": c, "p_exact_mcnemar": p}
    v1 = json.load(open(REPO / "results" / "e0c_sib" / "gate" / "verdicts.json"))
    rows = [{"model": t_["model"], "diff": t_["diff"], "p": t_["p"]} for t_ in v1["P_a_tests"] if t_["model"] in X.PHASE1_ACC and t_["b"] == "itrans"]
    for m2 in ("qwen3-8b", "llama-3.1-8b"):
        a_ = json.load(open(REPO / "results" / "phase2" / "x13" / m2 / "analysis.json"))
        r_ = [x for x in a_["P_a_this_model"] if x["b"] == "itrans"][0]
        rows.append({"model": m2, "diff": float(r_["diff"]), "p": float(r_["p"])})
    if out["counted"]["counted"]:
        rows.append({"model": M, "diff": out["native_minus_itrans"]["diff"], "p": p})
    ph = multipletests([r["p"] for r in rows], method="holm")[1]
    for r, q in zip(rows, ph):
        r["p_holm"], r["significant"] = float(q), bool(q < 0.05)
    n = len(rows)
    pos = sum(1 for r in rows if r["diff"] > 0 and r["significant"])
    out["extended_native_vs_itrans"] = {"tests": rows, "n_models": n, "positive_and_significant": pos, "verdict_all_but_one": "supported" if pos >= n - 1 else "not supported"}
    write_json(results_dir("phase2/x13/sarvam-m") / "analysis.json", out, {"registration": "RESULTS.md Amendment 2, X13 (Sarvam-m, 4-bit, SIB-200 only)"})
    print(json.dumps({"acc": {f: (round(v["acc_cal"], 3), [round(x, 3) for x in v["ci95"]]) for f, v in out["accuracy"].items()}, "counted": out["counted"], "native_minus_itrans": out["native_minus_itrans"],
                      "extended": {"n": n, "pos": pos, "verdict": out["extended_native_vs_itrans"]["verdict_all_but_one"], "models": [(r["model"], round(r["diff"], 3), r["significant"]) for r in rows]}}, indent=1))


if __name__ == "__main__":
    main()
