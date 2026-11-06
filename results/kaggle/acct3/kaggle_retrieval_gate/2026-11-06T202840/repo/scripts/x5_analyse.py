"""X5 (registered, Phase 2 pre-registration; analysis only, descriptive): cross-language consistency of the native-minus-natural gap with measured romanized exposure.

For Kannada, Hindi, Telugu and Bengali, on the ids that have a clean natural romanization in ALL four languages (FLORES ids for retrieval; the SIB-200 ids of the natural overlap restricted likewise), the gap
g = native minus natural per counted model on SIB-200 accuracy (calibrated as Phase 1) and on unmapped retrieval (M4c rows, test half), paired with the X2 exposure ratio e (Source A, documents).
Registered: the Spearman correlation between e and g across the four languages is negative (more romanized exposure goes with a smaller gap), separately for accuracy and for retrieval; "consistent" if negative in
all counted models but one (a model enters a measure only if it is counted for that measure in all four languages; fewer than three such models: uninformative), otherwise "inconsistent". No p value and no fitted line.
Counting (as registered per language): accuracy: native SIB-200 CI lower bound above 0.40; retrieval: native unmapped retrieval at least 0.50; Qwen2.5-1.5B is never counted.
Usage: X4_LANG=bn python scripts/x5_analyse.py        Output: results/phase2/x5/analysis.json (requires the Hindi vectors cache/activations/h_hindi)"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e0b_familiarity as e0b  # noqa: E402
import x4_lang as X  # noqa: E402

from shattered.runlog import REPO, results_dir, write_json  # noqa: E402

LANGS = ["kn", "hi", "bn", "te"]
MODELS = ["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
RET_MODELS = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
E0C = REPO / "results" / "e0c_sib" / "scores"
SIBDIR = {"kn": E0C, "hi": REPO / "results" / "h_hindi" / "scores" / "sib", "bn": REPO / "results" / "phase2" / "x4" / "bn" / "scores" / "sib", "te": REPO / "results" / "phase2" / "x4" / "te" / "scores" / "sib"}
NATFORM = {"kn": "natural257", "hi": "natural", "bn": "natural", "te": "natural"}
ACT = {"hi": REPO / "cache" / "activations" / "h_hindi", "bn": REPO / "cache" / "activations" / "x4_bn", "te": REPO / "cache" / "activations" / "x4_te"}


def natural_ids_flores() -> dict:
    out = {}
    kn = [json.loads(x) for x in open(REPO / "data" / "processed" / "natural_flores_m4_500_v1.jsonl", encoding="utf-8")]
    out["kn"] = {r["index"] for r in kn if not r["defective"]}
    hi = {}
    for x in open(REPO / "data" / "processed" / "natural_hindi_v1.jsonl", encoding="utf-8"):
        r = json.loads(x)
        hi[r["key"]] = r
    out["hi"] = {int(k.split("-")[1]) for k, r in hi.items() if k.startswith("flores-") and not r["defective"]}
    for lang in ("bn", "te"):
        d = {}
        for x in open(REPO / "data" / "processed" / f"natural_flores_{lang}_x4_v1.jsonl", encoding="utf-8"):
            r = json.loads(x)
            d[r["index"]] = r
        out[lang] = {i for i, r in d.items() if not r["defective"]}
    return out


def sib_acc(lang: str, m: str) -> tuple[pd.DataFrame, float]:
    base = SIBDIR[lang]
    e0b.CHANCE.setdefault("sib", 1 / 7)
    parts = [pd.read_parquet(base / f"{m}__native.parquet"), pd.read_parquet(base / f"{m}__{NATFORM[lang]}.parquet"), pd.read_parquet(E0C / f"{m}__english.parquet")]
    df = pd.concat(parts, ignore_index=True)[["model", "task", "form", "id", "label", "logprobs"]]
    df.loc[df.form == NATFORM[lang], "form"] = "natural"
    df, _ = e0b.apply_calibration(df, {m: json.load(open(base / f"cf_{m}.json"))})
    acc = e0b.accuracy_table(df)
    nat_lo = float(acc[(acc.form == "native")].acc_cal_ci_low.iloc[0])
    return df, nat_lo


def main() -> None:
    expo = json.load(open(REPO / "results" / "phase2" / "x2" / "exposure.json", encoding="utf-8"))["languages"]
    e = {l: expo[l]["e_documents"] for l in LANGS}
    flo = natural_ids_flores()
    common_f = sorted(set.intersection(*[flo[l] for l in LANGS]))
    out = {"e_documents": e, "n_common_flores_ids": len(common_f), "accuracy": {}, "retrieval": {}}
    # ---- SIB-200 accuracy
    g_acc, counted_acc = {}, {m: [] for m in MODELS}
    nat_ids = None
    frames = {}
    for l in LANGS:
        for m in MODELS:
            df, lo = sib_acc(l, m)
            frames[(l, m)] = df
            if lo > 0.40:
                counted_acc[m].append(l)
    ids = [set(frames[(l, MODELS[0])][frames[(l, MODELS[0])].form == "natural"].id) for l in LANGS]
    nat_ids = sorted(set.intersection(*ids) & set(common_f))
    out["n_common_sib_ids"] = len(nat_ids)
    for m in MODELS:
        if len(counted_acc[m]) < len(LANGS):
            out["accuracy"][m] = {"counted_in": counted_acc[m], "entered": False}
            continue
        gg = {}
        for l in LANGS:
            df = frames[(l, m)]
            c = {}
            for f in ("native", "natural"):
                g_ = df[(df.form == f) & df.id.isin(nat_ids)].sort_values("id")
                c[f] = float((g_.pred_cal.to_numpy() == g_.label.to_numpy()).mean())
            gg[l] = c["native"] - c["natural"]
        rho = float(stats.spearmanr([e[l] for l in LANGS], [gg[l] for l in LANGS]).statistic)
        out["accuracy"][m] = {"entered": True, "gap_by_language": gg, "spearman_e_vs_gap": rho}
    # ---- retrieval (M4c rows, test half), counted when native unmapped retrieval >= 0.50 in every language
    counted_ret = {m: True for m in RET_MODELS}
    gap_ret = {m: {} for m in RET_MODELS}
    for l in LANGS:
        if l == "kn":
            X.H_ACT = ACT.get("kn")
        else:
            X.H_ACT = ACT[l]
        for m in RET_MODELS:
            lang_arg = "kannada" if l == "kn" else l
            h_nat = np.asarray(X.retrieval_hits(m, lang_arg, "native", common_f), float)
            h_nl = np.asarray(X.retrieval_hits(m, lang_arg, "natural", common_f), float)
            if h_nat.mean() < 0.50:
                counted_ret[m] = False
            gap_ret[m][l] = {"native": float(h_nat.mean()), "natural": float(h_nl.mean()), "gap": float(h_nat.mean() - h_nl.mean()), "n_test": int(len(h_nat))}
    for m in RET_MODELS:
        if not counted_ret[m]:
            out["retrieval"][m] = {"entered": False, "gap_by_language": gap_ret[m]}
            continue
        rho = float(stats.spearmanr([e[l] for l in LANGS], [gap_ret[m][l]["gap"] for l in LANGS]).statistic)
        out["retrieval"][m] = {"entered": True, "gap_by_language": gap_ret[m], "spearman_e_vs_gap": rho}

    def verdict(block: dict) -> dict:
        ent = {m: v for m, v in block.items() if isinstance(v, dict) and v.get("entered")}
        neg = [m for m, v in ent.items() if v["spearman_e_vs_gap"] < 0]
        if len(ent) < 3:
            return {"n_models": len(ent), "negative_in": neg, "verdict": "uninformative (fewer than three models)"}
        return {"n_models": len(ent), "negative_in": neg, "verdict": "consistent" if len(neg) >= len(ent) - 1 else "inconsistent"}
    out["accuracy_verdict"], out["retrieval_verdict"] = verdict(out["accuracy"]), verdict(out["retrieval"])
    k3b = {}
    for l, p in (("kn", REPO / "results" / "k3b" / "verdict.json"), ("hi", REPO / "results" / "k3b_hi" / "verdict.json"), ("bn", REPO / "results" / "phase2" / "x4" / "k3b_bn" / "verdict.json"),
                 ("te", REPO / "results" / "phase2" / "x4" / "k3b_te" / "verdict.json")):
        if p.exists():
            d = json.load(open(p, encoding="utf-8"))
            k3b[l] = {"verdict": d["K3b"], "ratios": {k: v["ratio"] for k, v in d["statistics"].items()}}
    out["k3b_reported_next_to_the_figure"] = k3b
    write_json(results_dir("phase2/x5") / "analysis.json", out, {"registration": "RESULTS.md X5 (descriptive, no p value)"})
    print(json.dumps({"e": {l: round(v * 100, 3) for l, v in e.items()}, "n_common_flores": len(common_f), "n_common_sib": len(nat_ids), "accuracy_verdict": out["accuracy_verdict"], "retrieval_verdict": out["retrieval_verdict"],
                      "accuracy": {m: ({l: round(g, 3) for l, g in v["gap_by_language"].items()}, round(v["spearman_e_vs_gap"], 2)) for m, v in out["accuracy"].items() if v.get("entered")},
                      "retrieval": {m: ({l: round(g["gap"], 3) for l, g in v["gap_by_language"].items()}, round(v["spearman_e_vs_gap"], 2)) for m, v in out["retrieval"].items() if v.get("entered")}}, indent=1))


if __name__ == "__main__":
    main()
