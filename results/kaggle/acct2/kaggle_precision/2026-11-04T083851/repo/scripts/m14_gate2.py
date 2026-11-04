"""Gate 2 analysis of the full M1/M4 run (results/m14_full/), against the registrations in RESULTS.md:
H1-H3 (2026-10-15; MDL detok primary) and the original M1 registration (2026-10-07; Patchscopes primary, H-frag /
H-script). No model is run: reads the per-item files written by scripts/m14_full.py.

Bootstraps: 10,000 resamples by multinomial reweighting. M1 CIs are computed twice: clustered by word (primary since
2026-10-16: a resampled word brings all its occurrences) and over occurrences (suffix _occ). Native vs ITRANS differences are paired (the same resampled
occurrences / test occurrences / words / FLORES sentences in both forms; pairing is checked). Lags resample
occurrences and sentences independently in the same iteration.
Detok / alignment layer = first layer reaching 90% of the curve's maximum (MDL compression, probe accuracy,
Patchscopes identification rate, retrieval accuracy@1 vs English).

Usage: python scripts/m14_gate2.py
Outputs (results/m14_full/gate2/): per_form.csv, paired.csv, erasure.csv, m4.csv, patchscopes_prereg.csv,
         patchscopes_spearman.csv, verdicts.json; figure paper2/figures/F_m14_layer_curves_draft.{pdf,png}
"""
import json

import numpy as np
import pandas as pd
from scipy import stats

from shattered.interp.clustered import B, FRAC, acc_curves, ci, first_reach, mdl_curves, weights
from shattered.plots import m14 as m14_plots
from shattered.runlog import REPO, results_dir, write_json

MODELS = ["qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
QWEN = ["qwen2.5-1.5b", "qwen3.5-2b"]
FORMS = ["english", "native", "itrans"]
PS_MIN_RATE = 0.5  # post hoc (set after seeing rates of 0-7% on Kannada): Patchscopes detok only where defined
RUN = REPO / "results" / "m14_full"


def load(m: str) -> dict:
    d = {"res": {f: json.load(open(RUN / m / f"{f}.json")) for f in FORMS},
         "items": {f: dict(np.load(RUN / m / f"items_{f}.npz")) for f in FORMS},
         "ps": {f: pd.read_parquet(RUN / m / f"patchscopes_{f}.parquet") for f in FORMS},
         "m4": json.load(open(RUN / m / "m4.json")), "m4_items": dict(np.load(RUN / m / "m4_items.npz"))}
    n, it = d["items"]["native"], d["items"]["itrans"]
    for k in ("mdl_order", "labels", "probe_train_mask", "in_e0"):
        assert np.array_equal(n[k], it[k]), f"{m}: native/ITRANS not paired on {k}"
    assert len(d["ps"]["native"]) == len(d["ps"]["itrans"])
    d["L"] = d["res"]["native"]["n_layers"]
    return d


def mdl_groups(d: dict) -> np.ndarray:
    """Word label of each column of the (shuffled-order) MDL cost matrices."""
    return d["items"]["native"]["labels"][d["items"]["native"]["mdl_order"]]


def paired_mdl(d: dict, subset: bool = False, seed: int = 0, cluster: bool = True) -> dict:
    """ITRANS minus native MDL detok layer, paired over the same resampled words (cluster) or occurrences."""
    cn, ci_ = d["items"]["native"]["mdl_costs"], d["items"]["itrans"]["mdl_costs"]
    g = mdl_groups(d)
    if subset:
        keep = d["items"]["native"]["in_e0"][d["items"]["native"]["mdl_order"]]
        cn, ci_, g = cn[:, keep], ci_[:, keep], g[keep]
    pn, pi = int(first_reach(1 / cn.sum(1))), int(first_reach(1 / ci_.sum(1)))
    diffs = []
    for w in weights(cn.shape[1], seed, g if cluster else None):
        diffs.append(first_reach(mdl_curves(ci_, w)) - first_reach(mdl_curves(cn, w)))
    diffs = np.concatenate(diffs)
    return {"native": pn, "itrans": pi, "diff": pi - pn, "diff_ci": ci(diffs), "diff_frac_depth": (pi - pn) / d["L"],
            "n": int(cn.shape[1])}


def single_mdl(costs: np.ndarray, groups: np.ndarray, seed: int = 0) -> dict:
    comp = 1 / costs.sum(1)
    out = {"detok": int(first_reach(comp)), "peak_layer": int(comp.argmax())}
    for key, g in (("ci", groups), ("ci_occ", None)):
        out[key] = ci(np.concatenate([first_reach(mdl_curves(costs, w)) for w in weights(costs.shape[1], seed, g)]))
    return out


def paired_probe(d: dict, seed: int = 0, cluster: bool = True) -> dict:
    a, b = d["items"]["native"]["probe_correct"], d["items"]["itrans"]["probe_correct"]
    it = d["items"]["native"]
    g = it["labels"][~it["probe_train_mask"]] if cluster else None
    diffs = np.concatenate([first_reach(acc_curves(b, w)) - first_reach(acc_curves(a, w))
                            for w in weights(a.shape[1], seed, g)])
    pn, pi = int(first_reach(a.mean(1))), int(first_reach(b.mean(1)))
    return {"native": pn, "itrans": pi, "diff": pi - pn, "diff_ci": ci(diffs), "n_test": int(a.shape[1])}


def ps_matrix(df: pd.DataFrame) -> np.ndarray:
    return np.stack([np.asarray(x, bool) for x in df.identified])


def paired_ps(d: dict, seed: int = 0) -> dict:
    a, b = ps_matrix(d["ps"]["native"]), ps_matrix(d["ps"]["itrans"])
    ra, rb = d["ps"]["native"].first_id_layer.notna().mean(), d["ps"]["itrans"].first_id_layer.notna().mean()
    out = {"id_rate_native": float(ra), "id_rate_itrans": float(rb), "n_words": int(len(a))}
    if min(ra, rb) < PS_MIN_RATE:
        return {**out, "diff": None, "diff_ci": None, "note": f"not measurable (identification rate < {PS_MIN_RATE})"}
    diffs = np.concatenate([first_reach(acc_curves(b.T, w)) - first_reach(acc_curves(a.T, w))
                            for w in weights(len(a), seed)])
    pn, pi = int(first_reach(a.mean(0))), int(first_reach(b.mean(0)))
    return {**out, "native": pn, "itrans": pi, "diff": pi - pn, "diff_ci": ci(diffs)}


def m4_and_lag(d: dict, seed: int = 0, cluster: bool = True) -> dict:
    """Alignment layers, max retrieval, paired differences, and lag difference (ITRANS minus native)."""
    rn, ri = d["m4_items"]["native"], d["m4_items"]["itrans"]
    cn, cI = d["items"]["native"]["mdl_costs"], d["items"]["itrans"]["mdl_costs"]
    an, ai = int(first_reach(rn.mean(1))), int(first_reach(ri.mean(1)))
    dn, di = int(first_reach(1 / cn.sum(1))), int(first_reach(1 / cI.sum(1)))
    al_d, max_d, lag_d, max_n, max_i = [], [], [], [], []
    wo = weights(cn.shape[1], seed + 1, mdl_groups(d) if cluster else None)  # sentences x words (or occurrences)
    for ws in weights(rn.shape[1], seed):
        wocc = next(wo)
        An, Ai = acc_curves(rn, ws), acc_curves(ri, ws)
        a_n, a_i = first_reach(An), first_reach(Ai)
        d_n, d_i = first_reach(mdl_curves(cn, wocc)), first_reach(mdl_curves(cI, wocc))
        al_d.append(a_i - a_n)
        lag_d.append((a_i - d_i) - (a_n - d_n))
        max_n.append(An.max(1))
        max_i.append(Ai.max(1))
        max_d.append(An.max(1) - Ai.max(1))
    cat = np.concatenate
    return {"n_sentences": int(rn.shape[1]), "align_native": an, "align_itrans": ai, "align_diff": ai - an,
            "align_diff_ci": ci(cat(al_d)), "max_retrieval_native": float(rn.mean(1).max()),
            "max_retrieval_native_ci": ci(cat(max_n)), "max_retrieval_itrans": float(ri.mean(1).max()),
            "max_retrieval_itrans_ci": ci(cat(max_i)), "native_minus_itrans_max": float(rn.mean(1).max() - ri.mean(1).max()),
            "native_minus_itrans_max_ci": ci(cat(max_d)), "lag_native": an - dn, "lag_itrans": ai - di,
            "lag_diff": (ai - di) - (an - dn), "lag_diff_ci": ci(cat(lag_d)),
            "max_cka_native": float(max(d["m4"]["native"]["cka"])), "max_cka_itrans": float(max(d["m4"]["itrans"]["cka"]))}


def excl0(c) -> int:
    """+1 if the CI lies above 0, -1 if below, 0 if it includes 0."""
    return 1 if c[0] > 0 else -1 if c[1] < 0 else 0


def main() -> None:
    out = results_dir("m14_full/gate2")
    per_form, paired, erasure, m4rows, prereg, spear, curves = [], [], [], [], [], [], {}
    data = {m: load(m) for m in MODELS}
    for m, d in data.items():
        L = d["L"]
        curves[m] = {"L": L, "mdl": {}, "retrieval": {f: d["m4"][f]["retrieval_acc"] for f in ("native", "itrans")}}
        for f in FORMS:
            r, it, ps = d["res"][f], d["items"][f], d["ps"][f]
            s = single_mdl(it["mdl_costs"], it["labels"][it["mdl_order"]])
            comp = np.asarray(r["mdl"]["compression"])
            curves[m]["mdl"][f] = comp.tolist()
            assert s["detok"] == r["mdl"]["detok_layer"], (m, f)
            id_rate = ps.first_id_layer.notna().mean()
            ps_rate = ps_matrix(ps).mean(0)
            per_form.append({
                "model": m, "form": f, "n_layers": L, "n_occ": r["n_occ"], "tokens_per_word": r["tokens_per_word_mean"],
                "frac_ge3_tokens": r["frac_ge3"], "mdl_detok": s["detok"], "mdl_ci_low": s["ci"][0],
                "mdl_ci_high": s["ci"][1], "mdl_ci_occ_low": s["ci_occ"][0], "mdl_ci_occ_high": s["ci_occ"][1],
                "mdl_detok_frac_depth": s["detok"] / L, "mdl_peak_layer": s["peak_layer"],
                "compression_max": comp.max(), "compression_last": comp[-1],
                "probe_detok": r["probe_detok"]["detok_layer"], "probe_ci_low": r["probe_detok"]["ci_low"],
                "probe_ci_high": r["probe_detok"]["ci_high"], "probe_acc_layer0": r["probe_acc"][0],
                "probe_acc_layer1": r["probe_acc"][1], "probe_acc_max": max(r["probe_acc"]),
                "probe_control_max": max(r["probe_acc_control"]),
                "ps_id_rate_any_layer": id_rate, "ps_rate_max_layer": ps_rate.max(),
                "ps_detok": int(first_reach(ps_rate)) if id_rate >= PS_MIN_RATE else None,
                "mdl_detok_e0": r["mdl_e0_subset"]["detok_layer"] if r["mdl_e0_subset"] else None,
                "n_e0_occ": r["mdl_e0_subset"]["n"] if r["mdl_e0_subset"] else 0, "n_e0_words": r["n_e0_words"]})
            for off in ("-1", "-2"):
                e = r["erasure"][off]
                erasure.append({"model": m, "form": f, "offset": off, "defined": e is not None,
                                **({k: e[k] for k in ("peak_layer", "erasure_layer", "magnitude", "n", "n_test",
                                                       "n_classes")} | {"acc_peak": max(e["acc"]), "acc_last": e["acc"][-1]}
                                   if e else {})})
            # original registration, secondary: Patchscopes detok layer rises with token count (identified words)
            idf = ps[ps.first_id_layer.notna()]
            if len(idf) >= 30:
                x, y = idf.n_tokens.to_numpy(), idf.first_id_layer.to_numpy()
                rho = stats.spearmanr(x, y).statistic
                rng = np.random.default_rng(0)
                bs = [stats.spearmanr(x[i], y[i]).statistic for i in rng.integers(0, len(x), (2000, len(x)))]
                spear.append({"model": m, "form": f, "n_identified": len(idf), "rho": rho, "ci": ci(np.nan_to_num(bs)),
                              "verdict": "rises" if np.percentile(np.nan_to_num(bs), 2.5) > 0 else "not shown"})
            else:
                spear.append({"model": m, "form": f, "n_identified": len(idf), "rho": None, "ci": None,
                              "verdict": "not testable (< 30 identified words)"})
        pm, pme, pp, pps, lag = paired_mdl(d), paired_mdl(d, subset=True), paired_probe(d), paired_ps(d), m4_and_lag(d)
        pm_o, pme_o, pp_o = paired_mdl(d, cluster=False), paired_mdl(d, subset=True, cluster=False), paired_probe(
            d, cluster=False)
        lag_o = m4_and_lag(d, cluster=False)
        tpw = d["res"]["itrans"]["tokens_per_word_mean"] - d["res"]["native"]["tokens_per_word_mean"]
        paired.append({"model": m, "tpw_native": d["res"]["native"]["tokens_per_word_mean"],
                       "tpw_itrans": d["res"]["itrans"]["tokens_per_word_mean"], "tpw_diff": tpw,
                       **{f"mdl_{k}": v for k, v in pm.items()}, **{f"mdl_e0_{k}": v for k, v in pme.items()},
                       **{f"probe_{k}": v for k, v in pp.items()}, **{f"ps_{k}": v for k, v in pps.items()},
                       "mdl_diff_ci_occ": pm_o["diff_ci"], "mdl_e0_diff_ci_occ": pme_o["diff_ci"],
                       "probe_diff_ci_occ": pp_o["diff_ci"]})
        m4rows.append({"model": m, **lag, "lag_diff_ci_occ": lag_o["lag_diff_ci"]})
        # original registration (2026-10-07): Delta = mean over words of (native - ITRANS) first_id_layer / L, words
        # identified in both forms, paired bootstrap over words
        a, b = d["ps"]["native"].first_id_layer.to_numpy(), d["ps"]["itrans"].first_id_layer.to_numpy()
        both = ~np.isnan(a.astype(float)) & ~np.isnan(b.astype(float))
        row = {"model": m, "n_words": len(a), "success_native": float(np.mean(~np.isnan(a.astype(float)))),
               "success_itrans": float(np.mean(~np.isnan(b.astype(float)))), "n_both": int(both.sum())}
        if both.sum() >= 30:
            dd = (a[both].astype(float) - b[both].astype(float)) / L
            bs = dd[np.random.default_rng(0).integers(0, len(dd), (B, len(dd)))].mean(1)
            row.update({"delta": dd.mean(), "delta_ci": ci(bs), "favors": {1: "ITRANS-earlier", -1: "native-earlier",
                                                                           0: "no difference"}[excl0(ci(bs))]})
        else:
            row.update({"delta": None, "delta_ci": None, "favors": "not testable (< 30 words identified in both forms)"})
        prereg.append(row)
        print(f"{m}: MDL ITRANS-native {pm['diff']} word {np.round(pm['diff_ci'], 1).tolist()} occ "
              f"{np.round(pm_o['diff_ci'], 1).tolist()} | lag diff {lag['lag_diff']} "
              f"{lag['lag_diff_ci']} | max retrieval native {lag['max_retrieval_native']:.3f} itrans "
              f"{lag['max_retrieval_itrans']:.3f}", flush=True)

    P = pd.DataFrame(paired).set_index("model")
    M4 = pd.DataFrame(m4rows).set_index("model")
    # ---- registered verdicts (2026-10-15)
    sign_d = {m: excl0(P.loc[m, "mdl_diff_ci"]) for m in MODELS}
    h1_parts = {}
    for m in QWEN:
        detok_ok = P.loc[m, "mdl_diff_ci"][0] <= 0  # CI includes 0 or is negative
        lag_ok = excl0(M4.loc[m, "lag_diff_ci"]) == 1
        never = excl0(M4.loc[m, "native_minus_itrans_max_ci"]) == 1  # ITRANS max retrieval below native's (paired CI)
        h1_parts[m] = {"detok_not_later": bool(detok_ok), "larger_lag": bool(lag_ok),
                       "never_reaches_native_max_retrieval": bool(never),
                       "holds": bool(detok_ok and (lag_ok or never))}
    h1 = all(v["holds"] for v in h1_parts.values())
    h2 = all(sign_d[m] == 1 for m in QWEN)
    want = {m: int(np.sign(P.loc[m, "tpw_diff"])) for m in MODELS}
    point = {m: int(np.sign(P.loc[m, "mdl_diff"])) for m in MODELS}
    h3_match = all(point[m] == want[m] for m in MODELS)
    h3_n_excl = sum(sign_d[m] == want[m] for m in MODELS)
    h3_refuted = all(sign_d[m] == 1 for m in MODELS)
    h3 = "supported" if h3_match and h3_n_excl >= 3 else "refuted" if h3_refuted else "not supported"
    qwen_outcome = "H1" if h1 and not h2 else "H2" if h2 and not h1 else "inconclusive"
    # ---- original registration (2026-10-07): H-frag / H-script on Patchscopes (primary) and MDL (reported alongside)
    PR = pd.DataFrame(prereg).set_index("model")
    fav = {m: PR.loc[m, "favors"] for m in MODELS}
    testable = all(isinstance(PR.loc[m, "delta"], float) for m in MODELS)
    mdl_fav = {m: {1: "native-earlier", -1: "ITRANS-earlier", 0: "no difference"}[sign_d[m]] for m in MODELS}

    def hfrag_hscript(f):
        q_itr = [f[m] == "ITRANS-earlier" for m in QWEN]
        hfrag = (all(f[m] == "native-earlier" for m in ("gemma4-e2b", "sarvam-1"))
                 and (all(q_itr) or (sum(q_itr) == 1 and "no difference" in [f[m] for m in QWEN])))
        hscript = all(f[m] == "ITRANS-earlier" for m in MODELS)
        return "H-frag" if hfrag else "H-script" if hscript else "inconclusive"
    # ---- method disagreements on the ordering (ITRANS vs native)
    dis = []
    for m in MODELS:
        o = {"mdl": sign_d[m], "probe": excl0(P.loc[m, "probe_diff_ci"])}
        if P.loc[m, "ps_diff_ci"] is not None:
            o["patchscopes"] = excl0(P.loc[m, "ps_diff_ci"])
        dis.append({"model": m, **o, "agree": len(set(o.values())) == 1})
    verdicts = {
        "H1": {"per_qwen_model": h1_parts, "holds": h1},
        "H2": {"mdl_sign_ci": {m: sign_d[m] for m in QWEN}, "holds": h2},
        "qwen_outcome_H1_vs_H2": qwen_outcome,
        "H3": {"expected_sign_from_tpw": want, "mdl_point_sign": point, "mdl_ci_sign": sign_d,
               "n_models_ci_excluding_0_in_expected_direction": h3_n_excl, "verdict": h3},
        "original_2026_10_07": {"patchscopes_primary": {"favors": fav, "testable": testable,
                                                        "verdict": hfrag_hscript(fav) if testable else "not testable"},
                                "mdl_alongside": {"favors": mdl_fav, "verdict": hfrag_hscript(mdl_fav)}},
        "method_agreement": dis,
        "notes": {"ps_min_rate": f"post hoc: Patchscopes detok computed only where identification rate >= {PS_MIN_RATE}",
                  "never_reaches": "operationalized as the paired CI of (native max - ITRANS max retrieval) above 0; "
                                   "chosen after the max retrieval values were printed by the run log"}}
    pd.DataFrame(per_form).to_csv(out / "per_form.csv", index=False)
    P.reset_index().to_csv(out / "paired.csv", index=False)
    pd.DataFrame(erasure).to_csv(out / "erasure.csv", index=False)
    M4.reset_index().to_csv(out / "m4.csv", index=False)
    PR.reset_index().to_csv(out / "patchscopes_prereg.csv", index=False)
    pd.DataFrame(spear).to_csv(out / "patchscopes_spearman.csv", index=False)
    write_json(out / "verdicts.json", {"verdicts": verdicts, "curves": curves},
               {"bootstrap": B, "frac": FRAC, "primary_ci": "clustered by word (2026-10-16)", "models": MODELS, "registered": "RESULTS.md 2026-10-07 and 2026-10-15"})
    m14_plots.layer_curves(curves)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 40)
    print(pd.DataFrame(per_form).round(3).to_string(index=False))
    print(P.round(3).to_string())
    print(M4.round(3).to_string())
    print(pd.DataFrame(erasure).round(3).to_string(index=False))
    print(PR.to_string())
    print(pd.DataFrame(spear).to_string(index=False))
    print(json.dumps(verdicts, indent=1, default=str))


if __name__ == "__main__":
    main()
