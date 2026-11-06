"""X1 T3 analysis (EXPLORATORY, no registered claim: label "instruction verified by a native speaker, exploratory"); generated from scripts/x1_analyse.py by replacing T2 with T3 (same code, same rules, same item sets). Original header follows: X1 analysis (registered in RESULTS.md, 2026-11-01): T-a, T-b, T-c. CPU only; reads the stored T1 scores (Phase 1) and the T3 scores.

T-a (primary): P-a in its exact Phase 1 wording under T3 on SIB-200 (1,004 items), informative models = T3 English calibrated
   accuracy >= chance + 5 points; paired exact McNemar, Holm over all native-vs-ITRANS and native-vs-lossy tests of informative models;
   supported / refuted / partly supported by the Phase 1 rule. Secondary line: the same two contrasts in the four counted models only.
T-b: the 11 Phase 1 accuracy verdicts (P-a on SIB-200; L1, L2, L3 on sentiment and SIB-200 [SIB-200 L3 = the 257-item secondary];
   NC-F and NC-O on sentiment and SIB-200) recomputed under T3 by the same rules, Holm families, counted models and item sets, and
   compared with the same pipeline run on the stored T1 scores (which is checked against the stored Phase 1 verdict files).
T-c (descriptive): T3 minus T1 per cell (model x task x form) with a paired 95% bootstrap CI.
Outputs: results/phase2/x1/t3/analysis/.
"""
import json
import sys

import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

from shattered.runlog import REPO, write_json

sys.path.insert(0, str(REPO / "scripts"))
import e0b_familiarity as e0b  # noqa: E402
import l_ladder as lad  # noqa: E402
import nc1  # noqa: E402

ROOT = REPO / "results" / "phase2" / "x1" / "t3"
OUT = ROOT / "analysis"
MODELS = lad.ACC_MODELS
COUNTED = lad.COUNT_ACC
CONDS = nc1.CONDITIONS
CHANCE_SIB = 1 / 7
SRC = {"t1": {"B": lad.E0B_DIR, "C": lad.E0C_DIR, "NC": nc1.SCORES},
       "t3": {"B": ROOT / "scores_e0b", "C": ROOT / "scores_e0c", "NC": ROOT / "scores_nc"}}
FORMS_B = ["english", "native", "itrans", "lower", "lossy", "natural"]
FORMS_C = ["english", "native", "itrans", "lower", "lossy", "natural257"]
LADDER = [("L1", "lower", "itrans"), ("L2", "lossy", "lower"), ("L3", "natural", "lossy")]
NCC = [("NC-F", "nc_c", "nc_b"), ("NC-O", "nc_a", "nc_c")]


def frames(t: str):
    """Calibrated frames for one template: B (sentiment, xnli) and C (sib), each with the NC rows, plus the fallback tables."""
    d = SRC[t]
    out, fbs = {}, {}
    for key, forms, grp in (("B", FORMS_B, "e0b"), ("C", FORMS_C, "e0c")):
        cf = {m: json.load(open(d[key] / f"cf_{m}.json")) for m in MODELS}
        df = pd.concat([pd.read_parquet(d[key] / f"{m}__{f}.parquet") for m in MODELS for f in forms]
                       + [pd.read_parquet(d["NC"] / f"{m}__nc_{c}__{grp}.parquet") for m in MODELS for c in CONDS], ignore_index=True)
        out[key], fbs[key] = e0b.apply_calibration(df, cf)
    return out["B"], out["C"], pd.concat([fbs["B"], fbs["C"]], ignore_index=True)


def correct_matrix(df: pd.DataFrame, model: str, task: str):
    g = df[(df.model == model) & (df.task == task)]
    piv = g.pivot_table(index="id", columns="form", values="pred_cal")
    lab = g.drop_duplicates("id").set_index("id").label.loc[piv.index]
    return piv, piv.eq(lab, axis=0)


def contrasts(B: pd.DataFrame, C: pd.DataFrame) -> pd.DataFrame:
    rows = []
    specs = [("sentiment", B, "sentiment", LADDER), ("sib", C, "sib", LADDER[:2]),
             ("sib_L3_secondary", C, "sib", [("L3", "natural257", "lossy")]),
             ("sentiment_nc", B, "sentiment", NCC), ("sib_nc", C, "sib", NCC)]
    for measure, df, task, cons in specs:
        for m in COUNTED:
            piv, corr = correct_matrix(df, m, task)
            for L, a, b in cons:
                k = piv[a].notna() & piv[b].notna()
                rows.append({"measure": measure, "model": m, "contrast": L, "a": a, "b": b,
                             **lad.paired(corr[a][k].to_numpy(), corr[b][k].to_numpy())})
    K = pd.DataFrame(rows)
    K["p_holm"] = np.nan
    for s in K.measure.unique():
        k = K.measure == s
        K.loc[k, "p_holm"] = multipletests(K.loc[k, "p"], method="holm")[1]
    K["significant"] = K.p_holm < 0.05
    K["ci_excludes_0"] = [c[0] > 0 or c[1] < 0 for c in K.ci]
    K["ci_holm_disagree"] = K.significant != K.ci_excludes_0
    return K


def effect_verdicts(K: pd.DataFrame) -> dict:
    need = 3  # 3 of the 4 counted accuracy models (Phase 1 rule)
    out = {}
    for (s, L), g in K.groupby(["measure", "contrast"]):
        pos, neg = int((g.significant & (g["diff"] > 0)).sum()), int((g.significant & (g["diff"] < 0)).sum())
        v = "effect, positive" if pos >= need else "effect, negative" if neg >= need else "no effect detected"
        name = {"sentiment": "sentiment", "sib": "sib", "sib_L3_secondary": "sib", "sentiment_nc": "sentiment", "sib_nc": "sib"}[s]
        out[f"{L}|{name}"] = {"verdict": v, "n_significant_positive": pos, "n_significant_negative": neg, "n_counted": len(g),
                              "ci_holm_disagreements": g[g.ci_holm_disagree].model.tolist()}
    return out


def pa_verdict(C: pd.DataFrame, models: list[str]) -> dict:
    """P-a, exact Phase 1 wording, on SIB-200 for the given candidate models (informative ones are kept)."""
    acc = e0b.accuracy_table(C[C.form == "english"]).set_index("model")
    informative = [m for m in models if acc.loc[m, "acc_cal"] >= CHANCE_SIB + 0.05]
    mc = e0b.mcnemar_table(C[C.model.isin(informative) & C.form.isin(["native", "itrans", "lossy"])],
                           [("native", "itrans"), ("native", "lossy")])
    rev = mc[mc.significant & (mc["diff"] < 0)]
    npos = int(((mc["diff"] > 0) & mc.significant).sum())
    if (mc["diff"] > 0).all() and mc.significant.all():
        v = "supported"
    elif len(rev) or not mc.significant.any():
        v = "refuted"
    else:
        v = "partly supported"
    return {"verdict": v, "n_positive_significant": npos, "n_tests": len(mc), "informative_models": informative,
            "english_acc_cal": {m: float(acc.loc[m, "acc_cal"]) for m in models},
            "misses": mc[~((mc["diff"] > 0) & mc.significant)][["model", "b", "diff", "p_holm"]].to_dict("records")}, mc


def template_results(t: str):
    B, C, fb = frames(t)
    K = contrasts(B, C)
    V = effect_verdicts(K)
    pa5, mc5 = pa_verdict(C, MODELS)
    pa4, mc4 = pa_verdict(C, COUNTED)
    return dict(B=B, C=C, fb=fb, K=K, V=V, pa5=pa5, mc5=mc5, pa4=pa4, mc4=mc4)


NAMES = [("P-a|sib", "P-a on SIB-200")] + [(f"{L}|{m}", f"{L} {m}") for m in ("sentiment", "sib") for L in ("L1", "L2", "L3")] + \
        [(f"{L}|{m}", f"{L} {m}") for m in ("sentiment", "sib") for L in ("NC-F", "NC-O")]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    R = {t: template_results(t) for t in ("t1", "t3")}

    # --- check: the T1 pipeline here reproduces the stored Phase 1 verdicts
    lad_v = json.load(open(REPO / "results" / "l_ladder" / "verdict.json"))
    nc_v = json.load(open(REPO / "results" / "nc1" / "verdict.json"))
    pa_v = json.load(open(REPO / "results" / "e0c_sib" / "gate" / "verdicts.json"))
    stored = {"P-a|sib": pa_v["P_a"]}
    for key in ("L1", "L2", "L3"):
        stored[f"{key}|sentiment"] = lad_v[f"{key}|sentiment"]["verdict"]
    stored["L1|sib"], stored["L2|sib"] = lad_v["L1|sib"]["verdict"], lad_v["L2|sib"]["verdict"]
    stored["L3|sib"] = lad_v["L3|sib_L3_secondary"]["verdict"]
    for key in ("NC-F", "NC-O"):
        for m in ("sentiment", "sib"):
            stored[f"{key}|{m}"] = nc_v[f"{key}|{m}"]["verdict"]
    cat = lambda r, k: r["pa5"]["verdict"] if k == "P-a|sib" else r["V"][k]["verdict"]  # noqa: E731
    repro = {k: (cat(R["t1"], k), stored[k]) for k in stored}
    bad = {k: v for k, v in repro.items() if v[0] != v[1]}

    # --- T-a
    ta = {"primary_P_a_exact_wording_all_informative_models": R["t3"]["pa5"],
          "secondary_every_counted_model": R["t3"]["pa4"],
          "phase1_same_lines": {"P_a": R["t1"]["pa5"]["verdict"], "n_positive_significant": R["t1"]["pa5"]["n_positive_significant"],
                                "n_tests": R["t1"]["pa5"]["n_tests"], "counted_four": R["t1"]["pa4"]["verdict"]}}
    R["t3"]["mc5"].to_csv(OUT / "ta_primary_mcnemar.csv", index=False)
    R["t3"]["mc4"].to_csv(OUT / "ta_secondary_mcnemar.csv", index=False)

    # --- T-b
    tb = []
    for k, label in NAMES:
        a, b = cat(R["t1"], k), cat(R["t3"], k)
        tb.append({"verdict_line": label, "t1": a, "t3": b, "same": a == b})
    tb = pd.DataFrame(tb)
    tb.to_csv(OUT / "tb_verdicts.csv", index=False)
    pd.concat([R["t1"]["K"].assign(template="t1"), R["t3"]["K"].assign(template="t3")]).drop(columns=["ci"]).to_csv(OUT / "contrasts_t1_t3.csv", index=False)

    # --- T-c
    rows = []
    for key, g1, g2 in (("B", R["t1"]["B"], R["t3"]["B"]), ("C", R["t1"]["C"], R["t3"]["C"])):
        for (m, t, f), x2 in g2.groupby(["model", "task", "form"]):
            x1 = g1[(g1.model == m) & (g1.task == t) & (g1.form == f)]
            j = x2.merge(x1, on="id", suffixes=("_2", "_1"))
            if j.empty:
                continue
            c2, c1 = (j.pred_cal_2 == j.label_2).to_numpy(), (j.pred_cal_1 == j.label_1).to_numpy()
            rows.append({"model": m, "task": t, "form": f, "n": len(j), **lad.paired(c2, c1)})
    TC = pd.DataFrame(rows)
    TC["acc_t3"], TC["acc_t1"] = TC.pop("acc_a"), TC.pop("acc_b")
    ci = TC.pop("ci")
    TC["ci_low"], TC["ci_high"] = [c[0] for c in ci], [c[1] for c in ci]
    TC.to_csv(OUT / "tc_cells.csv", index=False)
    fb = R["t1"]["fb"].assign(template="t1").merge(R["t3"]["fb"].assign(template="t3"), on=["model", "task"], suffixes=("_t1", "_t3"))
    fb.to_csv(OUT / "calibration_fallback_t1_t3.csv", index=False)

    summary = {"T-a": ta, "T-b": tb.to_dict("records"),
               "T-b_same_category": int(tb.same.sum()), "T-b_total": len(tb),
               "t1_pipeline_reproduces_phase1_verdicts": not bad, "t1_reproduction_mismatches": bad,
               "t3_calibration_fallback_rows": fb[fb.use_raw_t3][["model", "task"]].to_dict("records"),
               "t1_calibration_fallback_rows": fb[fb.use_raw_t1][["model", "task"]].to_dict("records"),
               "t3_effect_verdicts": R["t3"]["V"], "t1_effect_verdicts": R["t1"]["V"]}
    write_json(OUT / "summary.json", summary, {"registered": "RESULTS.md 2026-11-01 (X1)", "template": "e0_*_v2",
                                               "counted_accuracy": COUNTED, "all_models": MODELS})
    print(json.dumps({k: summary[k] for k in ("T-b_same_category", "T-b_total", "t1_pipeline_reproduces_phase1_verdicts", "t1_reproduction_mismatches")}, indent=1))
    print(tb.to_string(index=False))
    print(json.dumps(ta["primary_P_a_exact_wording_all_informative_models"], indent=1))


if __name__ == "__main__":
    main()
