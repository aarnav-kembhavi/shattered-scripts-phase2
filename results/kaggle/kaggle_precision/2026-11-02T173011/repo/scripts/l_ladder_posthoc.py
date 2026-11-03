"""Ladder post hoc analyses (post hoc descriptive, 2026-10-22, no verdict). CPU only; stored ladder scores and cached
sentence vectors, the ladder's own procedures (retrieval per-item hits are recomputed exactly as `l_ladder.py analyse`
and checked against results/l_ladder/contrasts.csv).

1. L3 (natural - lossy) restricted to items whose natural text has no English word longer than 3 characters (wordfreq
   English, Zipf >= 3, as scripts/english_share.py), on retrieval (M4c test half), sentiment (198) and SIB-257, next to
   the full-sample L3.
2. Net ITRANS -> lossy change (L1 + L2 = lossy - itrans) on retrieval and SIB-200 (1,004); sentiment from
   results/l_ladder_posthoc/net_itrans_to_lossy.csv is included in the combined table.

Paired bootstrap 95% CIs and exact McNemar p (unadjusted) as in the ladder.

Usage: python scripts/l_ladder_posthoc.py
Outputs: results/l_ladder_posthoc/{l3_no_english.csv, net_itrans_to_lossy_all.csv}
"""
import json
import sys

import numpy as np
import pandas as pd

from shattered.runlog import REPO, results_dir, write_json

sys.path.insert(0, str(REPO / "scripts"))
import e0b_familiarity as e0b  # noqa: E402
import english_share as es  # noqa: E402
import l_ladder as lad  # noqa: E402
from m4b_mapping import ACT, layer_fit  # noqa: E402
from m4c_natural_flores import SEED  # noqa: E402


def has_english(text: str, wl: set) -> bool:
    return any(len(w) >= 4 and w.lower() in wl for w in es.words(text))


def retrieval_hits() -> tuple[dict, np.ndarray, list]:
    """{model: {form: hits on the 248 test sentences}}, test-half M4c indices, retained rows (ladder procedure)."""
    R, keep, _ = lad.m4c_sample()
    idx = np.array([r["index"] for r in R])[keep]
    n = len(idx)
    order = np.random.default_rng(SEED).permutation(n)
    tr, te = np.sort(order[: n // 2]), np.sort(order[n // 2:])
    folds = np.array_split(np.random.default_rng(SEED + 2).permutation(tr), 5)
    out = {}
    for m in lad.M4_MODELS:
        E = np.load(ACT / m / "english.npz")["flores_states"][idx]
        forms = {"itrans": np.load(ACT / m / "itrans.npz")["flores_states"][idx]}
        for f in ("lower", "lossy", "natural"):
            z = np.load(ACT / m / f"{f}500.npz")
            assert np.array_equal(z["index"][keep], idx)
            forms[f] = z["flores_states"][keep]
        out[m] = {}
        for f, X in forms.items():
            fits = [layer_fit(X[:, l], E[:, l], tr, te, folds) for l in range(X.shape[1])]
            out[m][f] = fits[int(np.argmax([r["unmapped_train"] for r in fits]))]["unmapped"]
        print(m, "retrieval hits recomputed", flush=True)
    return out, idx[te], [r for r, k in zip(R, keep) if k]


def correctness(df, task):
    out = {}
    for m in lad.ACC_MODELS:
        g = df[(df.model == m) & (df.task == task)]
        piv = g.pivot_table(index="id", columns="form", values="pred_cal")
        out[m] = piv.eq(g.drop_duplicates("id").set_index("id").label.loc[piv.index], axis=0)
    return out


def main() -> None:
    wl = es.wordlists()["zipf>=3"]
    K = pd.read_csv(REPO / "results/l_ladder/contrasts.csv").set_index(["measure", "model", "contrast"])
    hits, te_idx, kept = retrieval_hits()
    for m in lad.M4_MODELS:  # recomputed hits reproduce the registered contrasts
        for L, a, b in lad.CONTRASTS:
            assert np.isclose(hits[m][a].mean() - hits[m][b].mean(), K.loc[("retrieval", m, L), "diff"]), (m, L)
    nat_m4c = {r["index"]: r["natural"] for r in kept}
    clean_ret = np.array([not has_english(nat_m4c[i], wl) for i in te_idx])

    cf_b = {m: json.load(open(lad.E0B_DIR / f"cf_{m}.json")) for m in lad.ACC_MODELS}
    cf_c = {m: json.load(open(lad.E0C_DIR / f"cf_{m}.json")) for m in lad.ACC_MODELS}
    B = pd.concat([pd.read_parquet(lad.E0B_DIR / f"{m}__{f}.parquet") for m in lad.ACC_MODELS
                   for f in ("english", "lossy", "natural")], ignore_index=True)
    C = pd.concat([pd.read_parquet(lad.E0C_DIR / f"{m}__{f}.parquet") for m in lad.ACC_MODELS
                   for f in ("english", "itrans", "lower", "lossy", "natural257")], ignore_index=True)
    B, _ = e0b.apply_calibration(B, cf_b)
    C, _ = e0b.apply_calibration(C, cf_c)
    sent, sib = correctness(B, "sentiment"), correctness(C, "sib")
    nat_sent = {it["id"]: it["forms"]["natural"]["text"] for it in lad.e0b_items()["sentiment"]
                if not it.get("natural_defective")}
    nat_sib = {it["id"]: it["forms"]["natural257"]["text"] for it in lad.sib257_items()["sib"]}

    rows = []
    for measure, models, get in (
            ("retrieval", lad.M4_MODELS, lambda m: (hits[m]["natural"], hits[m]["lossy"], clean_ret)),
            ("sentiment", lad.ACC_MODELS, None), ("sib_L3_secondary", lad.ACC_MODELS, None)):
        for m in models:
            if measure == "retrieval":
                a, b, clean = get(m)
            else:
                corr, nat, col = ((sent[m], nat_sent, "natural") if measure == "sentiment"
                                  else (sib[m], nat_sib, "natural257"))
                k = corr[col].notna() & corr["lossy"].notna() & corr.index.isin(list(nat))
                corr = corr[k]
                a, b = corr[col].to_numpy(bool), corr["lossy"].to_numpy(bool)
                clean = np.array([not has_english(nat[i], wl) for i in corr.index])
            full = lad.paired(a, b)
            assert np.isclose(full["diff"], K.loc[(measure, m, "L3"), "diff"]), (measure, m)
            sub = lad.paired(a[clean], b[clean])
            rows.append({"measure": measure, "model": m, "counted": m in (lad.COUNT_RETRIEVAL if measure == "retrieval"
                                                                          else lad.COUNT_ACC),
                         "n_full": full["n"], "L3_full": full["diff"], "ci_full": full["ci"],
                         "n_no_english": sub["n"], "L3_no_english": sub["diff"], "ci_no_english": sub["ci"],
                         "p_unadjusted_no_english": sub["p"]})
    out = results_dir("l_ladder_posthoc")
    pd.DataFrame(rows).to_csv(out / "l3_no_english.csv", index=False)

    net = []
    for measure, models, pair in (("retrieval", lad.M4_MODELS, lambda m: (hits[m]["lossy"], hits[m]["itrans"])),
                                  ("sib", lad.ACC_MODELS, lambda m: (sib[m]["lossy"].to_numpy(bool),
                                                                    sib[m]["itrans"].to_numpy(bool)))):
        for m in models:
            r = lad.paired(*pair(m))
            l1, l2 = K.loc[(measure, m, "L1"), "diff"], K.loc[(measure, m, "L2"), "diff"]
            assert np.isclose(r["diff"], l1 + l2), (measure, m)
            net.append({"measure": measure, "model": m, "n": r["n"], "L1": l1, "L2": l2,
                        "net_lossy_minus_itrans": r["diff"], "ci_low": r["ci"][0], "ci_high": r["ci"][1],
                        "mcnemar_p_unadjusted": r["p"]})
    S = pd.read_csv(out / "net_itrans_to_lossy.csv").assign(measure="sentiment")
    net += S[["measure", "model", "n", "L1", "L2", "net_lossy_minus_itrans", "ci_low", "ci_high",
              "mcnemar_p_unadjusted"]].to_dict("records")
    N = pd.DataFrame(net)
    N["counted"] = [m in (lad.COUNT_RETRIEVAL if s == "retrieval" else lad.COUNT_ACC) for s, m in zip(N.measure, N.model)]
    N.to_csv(out / "net_itrans_to_lossy_all.csv", index=False)
    write_json(out / "posthoc_provenance.json", {"l3_rows": len(rows), "net_rows": len(N)},
               {"status": "post hoc descriptive, 2026-10-22, no verdict", "english": "wordfreq en Zipf>=3, len>=4"})
    pd.set_option("display.width", 250)
    print(pd.DataFrame(rows).round(3).to_string())
    print(N.round(3).to_string())


if __name__ == "__main__":
    main()
