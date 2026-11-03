"""X3 analysis (CPU), registered in RESULTS.md 2026-11-01 (section X3). Run after scripts/x3.py score has finished.

Contrasts on each model's eligible (matched) items, two-sided, Holm within each measure over 3 contrasts x counted models:
  D1 = a - NC-O,  D2 = a - c (c = frequency-matched split, proxy s_int),  D3 = NC-O - c.
Measures: SIB-200 and sentiment accuracy (counted: Qwen3, Qwen3.5, Sarvam-1, Gemma 4; effect = Holm-significant, same sign, in >= 3 of 4),
retrieval on the eligible M4c sentences (counted Qwen3.5, Sarvam-1, Gemma 4; >= 2 of 3; layer chosen on the eligible train half, evaluated
on the eligible test half, separately for a, NC-O and c). XNLI and Qwen2.5 reported, never counted. The s_ref split (r) is exploratory:
same contrasts, no verdict. Floors: a model with fewer than 300 eligible SIB items (150 eligible M4c sentences for retrieval) is exploratory.
Outputs: results/phase2/x3/{accuracy.csv, retrieval.csv, contrasts.csv, d1_full_vs_matched.csv, controls.csv, verdict.json}
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
import x3  # noqa: E402
from m4b_mapping import ACT, boot, layer_fit  # noqa: E402
from m4c_natural_flores import SEED  # noqa: E402

OUT = x3.OUT
CONTRASTS = {"D1": ("nc_a", "nc_c"), "D2": ("nc_a", "x3_{c}"), "D3": ("nc_c", "x3_{c}")}
PER_ITEM: list = []  # per-item correctness / hits for the exploratory regression (scripts/x3_regress.py)
NEED = {"retrieval": 2, "sentiment": 3, "sib": 3}
COUNTED = {"retrieval": lad.COUNT_RETRIEVAL, "sentiment": lad.COUNT_ACC, "sib": lad.COUNT_ACC}


def accuracy_contrasts() -> tuple[pd.DataFrame, pd.DataFrame]:
    con, acc = [], []
    for d, grp in ((lad.E0B_DIR, "e0b"), (lad.E0C_DIR, "e0c")):
        cf = {m: json.load(open(d / f"cf_{m}.json")) for m in lad.ACC_MODELS}
        for cond in x3.CONDS:
            parts = [pd.read_parquet(d / f"{m}__english.parquet") for m in lad.ACC_MODELS]
            parts += [pd.read_parquet(nc1.SCORES / f"{m}__nc_{c}__{grp}.parquet") for m in lad.ACC_MODELS for c in ("a", "c")]
            parts += [pd.read_parquet(x3.SCORES / f"{m}__x3_{cond}__{grp}.parquet") for m in lad.ACC_MODELS]
            B = pd.concat(parts, ignore_index=True)
            B, _ = e0b.apply_calibration(B, cf)
            for t in x3.GROUPS[grp]:
                measure = t if t != "xnli" else "xnli_reported_only"
                for m in lad.ACC_MODELS:
                    g = B[(B.model == m) & (B.task == t)]
                    piv = g.pivot_table(index="id", columns="form", values="pred_cal")
                    lab = g.drop_duplicates("id").set_index("id").label.loc[piv.index]
                    elig = g[g.form == f"x3_{cond}"].id.unique()
                    piv, lab = piv.loc[elig], lab.loc[elig]
                    corr = piv.eq(lab, axis=0)
                    PER_ITEM.append(pd.DataFrame({"measure": measure, "model": m, "cond": cond, "id": [str(i) for i in corr.index],
                                                  "nc_a": corr["nc_a"].to_numpy(), "nc_c": corr["nc_c"].to_numpy(),
                                                  "x3": corr[f"x3_{cond}"].to_numpy()}))
                    acc.append({"model": m, "task": t, "cond": cond, "n_eligible": len(elig),
                                **{f: corr[f].mean() for f in ("nc_a", "nc_c", f"x3_{cond}")}})
                    for L, (a, b) in CONTRASTS.items():
                        a, b = a.format(c=cond), b.format(c=cond)
                        con.append({"measure": measure, "model": m, "contrast": L, "cond": cond, "a": a, "b": b,
                                    **lad.paired(corr[a].to_numpy(), corr[b].to_numpy())})
    return pd.DataFrame(con), pd.DataFrame(acc)


def retrieval_contrasts() -> tuple[pd.DataFrame, pd.DataFrame]:
    R, keep, _ = lad.m4c_sample()
    idx = np.array([r["index"] for r in R])[keep]
    n = len(idx)
    order = np.random.default_rng(SEED).permutation(n)
    tr0, te0 = np.sort(order[: n // 2]), np.sort(order[n // 2:])
    con, res = [], []
    for m in lad.M4_MODELS:
        E = np.load(ACT / m / "english.npz")["flores_states"][idx]
        zs = {c: np.load(nc1.NC_ACT / m / f"{c}500.npz") for c in ("a", "c")}
        base = {c: z["flores_states"][keep] for c, z in zs.items()}
        for cond in x3.CONDS:
            z = np.load(x3.X3_ACT / m / f"{cond}500.npz")
            pos = {int(i): j for j, i in enumerate(idx)}
            rows = np.array([pos[int(i)] for i in z["index"]])
            el = np.zeros(n, bool)
            el[rows] = True
            tr, te = tr0[el[tr0]], te0[el[te0]]
            folds = np.array_split(np.random.default_rng(SEED + 2).permutation(tr), 5)
            Xm = np.zeros_like(base["a"])
            Xm[rows] = z["flores_states"]
            hits = {}
            for name, X in (("nc_a", base["a"]), ("nc_c", base["c"]), (f"x3_{cond}", Xm)):
                fits = [layer_fit(X[:, l], E[:, l], tr, te, folds) for l in range(X.shape[1])]
                lu = int(np.argmax([r["unmapped_train"] for r in fits]))
                hits[name] = fits[lu]["unmapped"]
                res.append({"model": m, "cond": cond, "form": name, "n_eligible": int(el.sum()), "n_train": len(tr), "n_test": len(te),
                            "unmapped_test": hits[name].mean(), "unmapped_test_ci": boot(hits[name]), "unmapped_layer": lu})
            PER_ITEM.append(pd.DataFrame({"measure": "retrieval", "model": m, "cond": cond, "id": [str(i) for i in idx[te]],
                                          "nc_a": hits["nc_a"], "nc_c": hits["nc_c"], "x3": hits[f"x3_{cond}"]}))
            for L, (a, b) in CONTRASTS.items():
                a, b = a.format(c=cond), b.format(c=cond)
                con.append({"measure": "retrieval", "model": m, "contrast": L, "cond": cond, "a": a, "b": b, **lad.paired(hits[a], hits[b])})
    return pd.DataFrame(con), pd.DataFrame(res)


def verdicts(K: pd.DataFrame, floor: dict) -> dict:
    out = {}
    for cond in x3.CONDS:
        for s, models in COUNTED.items():
            above = [m for m in models if floor[(s, m, cond)]]
            for L in CONTRASTS:
                g = K[(K.measure == s) & (K.contrast == L) & (K.cond == cond) & K.model.isin(above)]
                pos, neg = int((g.significant & (g["diff"] > 0)).sum()), int((g.significant & (g["diff"] < 0)).sum())
                informative = len(above) >= 3 if s != "retrieval" else len(above) >= 3
                v = ("uninformative (fewer than 3 models above the floor)" if not informative else
                     "effect, positive" if pos >= NEED[s] else "effect, negative" if neg >= NEED[s] else "no effect detected")
                out[f"{L}|{s}|{cond}"] = {"verdict": v, "status": "registered" if cond == "m" else "exploratory (s_ref split), no verdict",
                                          "n_significant_positive": pos, "n_significant_negative": neg, "needed": NEED[s],
                                          "models_above_floor": above}
    for s in COUNTED:
        d2, d3 = (out[f"{L}|{s}|m"]["verdict"] for L in ("D2", "D3"))
        e2, e3 = d2 == "effect, positive", d3 == "effect, positive"
        out[f"interpretation|{s}"] = ("both contribute" if e2 and e3 else "segmentation unfamiliarity itself costs" if e2 else
                                      "Phase 1 NC-O cost attributed to piece rarity" if e3 and d2 == "no effect detected" else
                                      "unresolved" if d2 == "no effect detected" and d3 == "no effect detected" else
                                      f"not covered by the registered rule (D2 {d2}; D3 {d3})")
    return out


def main() -> None:
    Ka, acc = accuracy_contrasts()
    Kr, ret = retrieval_contrasts()
    K = pd.concat([Ka, Kr], ignore_index=True)
    K["counted"] = [m in COUNTED.get(s, []) for s, m in zip(K.measure, K.model)]
    K["p_holm"] = np.nan
    for cond in x3.CONDS:
        for s in COUNTED:
            k = (K.measure == s) & K.counted & (K.cond == cond)
            K.loc[k, "p_holm"] = multipletests(K.loc[k, "p"], method="holm")[1]
    K["significant"] = K.p_holm < 0.05
    K["ci_excludes_0"] = [c[0] > 0 or c[1] < 0 for c in K.ci]
    K["ci_holm_disagree"] = K.counted & (K.significant != K.ci_excludes_0)
    E = pd.read_csv(OUT / "eligibility.csv", dtype={"id": str})
    floor = {}
    for cond in x3.CONDS:
        for s, models in COUNTED.items():
            for m in models:
                n_sib = int(E[(E.model == m) & (E.cond == cond) & (E.dataset == "sib") & E.eligible].shape[0])
                n_m4c = int(E[(E.model == m) & (E.cond == cond) & (E.dataset == "m4c") & E.eligible].shape[0])
                floor[(s, m, cond)] = (n_m4c >= x3.FLOOR_RET) if s == "retrieval" else (n_sib >= x3.FLOOR_ACC)
    V = verdicts(K, floor)
    # D1 on the full Phase 1 item sets next to the matched value
    P1 = pd.read_csv(REPO / "results" / "nc1" / "contrasts.csv")
    P1 = P1[P1.contrast == "NC-O"][["measure", "model", "n", "diff", "p_holm"]].rename(columns={"n": "n_full", "diff": "diff_full", "p_holm": "p_holm_full"})
    D1 = K[(K.contrast == "D1") & (K.cond == "m")][["measure", "model", "n", "diff", "p_holm"]].rename(
        columns={"n": "n_matched", "diff": "diff_matched", "p_holm": "p_holm_matched"})
    D1 = D1.merge(P1, on=["measure", "model"], how="left")
    ctl = [x for m in x3.MODELS for x in json.load(open(OUT / "control" / f"{m}.json"))]
    C = pd.DataFrame(ctl)
    pd.concat(PER_ITEM, ignore_index=True).to_csv(OUT / "per_item.csv", index=False)
    K.to_csv(OUT / "contrasts.csv", index=False)
    acc.to_csv(OUT / "accuracy.csv", index=False)
    ret.to_csv(OUT / "retrieval.csv", index=False)
    D1.to_csv(OUT / "d1_full_vs_matched.csv", index=False)
    C.to_csv(OUT / "controls.csv", index=False)
    V["recompute_control"] = {"max_abs_dlogprob": float(C.max_abs_dlogprob.max()), "all_below_1e-3": bool((C.max_abs_dlogprob < 1e-3).all())}
    write_json(OUT / "verdict.json", V, {"registered": "RESULTS.md 2026-11-01 (X3)", "counted_retrieval": lad.COUNT_RETRIEVAL,
                                         "counted_accuracy": lad.COUNT_ACC, "m4c_split_seed": SEED})
    print(json.dumps({k: v for k, v in V.items() if k.endswith("|m") or k.startswith("interp") or k == "recompute_control"}, indent=1))


if __name__ == "__main__":
    main()
