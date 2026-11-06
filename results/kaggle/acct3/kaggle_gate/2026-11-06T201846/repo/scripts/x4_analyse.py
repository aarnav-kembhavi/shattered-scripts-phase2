"""X4 analysis, part 1 (registered in RESULTS.md, Phase 2 pre-registration, X4): R1 and the counting rule for Bengali and Telugu on SIB-200 for the forms scored so far (native, ITRANS, lossy; natural on the
257 SIB ids). NOT included yet (not built or not run): the E9 lowercase form and the ladder L1-L3, retrieval (R2, R3), the MDL assembly layer (R4), IndicSentiment, K3b-bn/te.
Counting rule per language (registered): accuracy models are counted if the native SIB-200 accuracy (calibrated as Phase 1: mean of three content-free inputs, raw fallback if English drops more than 5 points;
English from the stored Kannada-run scores, the same 1,004 items) has a 95% bootstrap CI lower bound above 0.40; Qwen2.5-1.5B is reported and never counted.
R1: native > ITRANS and native > lossy on SIB-200, exact McNemar, Holm over (2 contrasts x counted models), effect positive for each contrast; the enlarged-set effect rule (all-but-one: positive and significant in
at least n - 1 of the n counted models, uninformative with fewer than three counted models) decides each contrast; R1 holds if both do.
Usage: python scripts/x4_analyse.py        Output: results/phase2/x4/<lang>/r1.json"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e0b_familiarity as e0b  # noqa: E402

from shattered.runlog import REPO, write_json  # noqa: E402

MODELS = ["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen2.5-1.5b"]
E0C = REPO / "results" / "e0c_sib" / "scores"


def analyse(lang: str) -> dict:
    base = REPO / "results" / "phase2" / "x4" / lang / "scores" / "sib"
    e0b.CHANCE.setdefault("sib", 1 / 7)
    parts, cf = [], {}
    for m in MODELS:
        for f in ("native", "itrans", "lossy", "natural"):
            parts.append(pd.read_parquet(base / f"{m}__{f}.parquet"))
        parts.append(pd.read_parquet(E0C / f"{m}__english.parquet"))
        cf[m] = json.load(open(base / f"cf_{m}.json"))
    df = pd.concat(parts, ignore_index=True)
    df = df[["model", "task", "form", "id", "label", "logprobs"]]
    df, fb = e0b.apply_calibration(df, cf)
    acc = e0b.accuracy_table(df)
    out = {"language": lang, "raw_fallback_rows": fb[fb.use_raw][["model", "task"]].to_dict("records"), "accuracy": {}, "counted": {}}
    for r in acc.itertuples():
        out["accuracy"].setdefault(r.model, {})[r.form] = {"n": int(r.n), "acc_cal": float(r.acc_cal), "ci95": [float(r.acc_cal_ci_low), float(r.acc_cal_ci_high)]}
    for m in MODELS:
        nat = out["accuracy"][m]["native"]
        eng = out["accuracy"][m]["english"]["acc_cal"]
        out["counted"][m] = {"native_ci_lower": nat["ci95"][0], "counted": bool(m != "qwen2.5-1.5b" and nat["ci95"][0] > 0.40), "english_acc": eng}
    counted = [m for m in MODELS if out["counted"][m]["counted"]]
    out["counted_models"] = counted
    mc = e0b.mcnemar_table(df[df.model.isin(counted) & df.form.isin(["native", "itrans", "lossy"])], [("native", "itrans"), ("native", "lossy")]) if counted else pd.DataFrame()
    out["R1_tests"] = mc.drop(columns=[c for c in ("task",) if c in mc.columns]).to_dict("records") if len(mc) else []
    r1 = {}
    n = len(counted)
    for b in ("itrans", "lossy"):
        ts = mc[mc.b == b] if len(mc) else mc
        pos = int(((ts["diff"] > 0) & ts.significant).sum()) if len(ts) else 0
        neg = int(((ts["diff"] < 0) & ts.significant).sum()) if len(ts) else 0
        r1[f"native_vs_{b}"] = {"n_counted": n, "positive_and_significant": pos, "significantly_negative": neg,
                                "verdict": "uninformative (fewer than three counted models)" if n < 3 else ("supported" if pos >= n - 1 and neg == 0 else "refuted" if neg > 0 or pos == 0 else "partly supported")}
    r1["R1"] = "supported" if all(v["verdict"] == "supported" for v in r1.values()) else "uninformative" if any(v["verdict"].startswith("uninformative") for v in r1.values()) else "not supported"
    out["R1"] = r1
    # the natural form on the 257 (descriptive here; ladder rules need the lowercase form)
    nat = {m: out["accuracy"][m].get("natural") for m in MODELS}
    out["natural_257_accuracy"] = nat
    write_json(REPO / "results" / "phase2" / "x4" / lang / "r1.json", out, {"registration": "RESULTS.md X4 (R1 and counting rule; part 1)"})
    return out


if __name__ == "__main__":
    for lang in ("bn", "te"):
        o = analyse(lang)
        print(lang, "counted:", o["counted_models"], "| R1:", o["R1"]["R1"], {k: (v["positive_and_significant"], v["verdict"]) for k, v in o["R1"].items() if k != "R1"})
        for m in MODELS:
            a = o["accuracy"][m]
            print("  ", m, {f: round(a[f]["acc_cal"], 3) for f in ("english", "native", "itrans", "lossy", "natural") if f in a}, "native CI lower", round(o["counted"][m]["native_ci_lower"], 3))
