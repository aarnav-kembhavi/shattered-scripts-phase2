"""M4b surface baseline and entity/number filter (registered in RESULTS.md, 2026-10-17, before running). CPU only.

(a) Surface baseline, from the existing M4b outputs (no refit): per model x form (native, ITRANS) and map (ridge =
    M4b primary, results/m4b_mapping; PCA Procrustes, results/m4b_robustness), L0 = mapped test retrieval at layer 0,
    Lb = mapped test retrieval at the train-half-CV-best layer among layers >= 1, gain = Lb - L0 (paired bootstrap CI).
    Beyond surface if CI low > 0.10, surface-level if CI high < 0.10, else partial.
(b) Entity/number filter: keep sentences whose English has no digit and no capitalised Latin word (except the first
    word and "I"). The M4b ridge mapping (M4b grid, folds, train-half selection) is rerun within kept sentences of each
    half; retrieval among kept test sentences. Same analysis on a size-matched random subset per half (seed 3).

Usage: python scripts/m4b_surface.py
Outputs (results/m4b_surface/): surface.csv, subset.csv, verdict.json
"""
import json
import re

import numpy as np
import pandas as pd

from m4b_mapping import ACT, MODELS, N_FOLDS, SEED, boot, layer_fit
from shattered.runlog import REPO, results_dir, write_json

FORMS = ["native", "itrans"]
WORD = re.compile(r"[A-Za-z][A-Za-z'’-]*")


def status3(c, hi="beyond surface", lo="surface-level"):
    return hi if c[0] > 0.10 else lo if c[1] < 0.10 else "partial"


def gap_status(c):
    return "persists" if c[0] > 0.10 else "closes" if c[1] < 0.10 else "partial"


def keep_sentence(en: str) -> bool:
    if re.search(r"[0-9]", en):
        return False
    words = WORD.findall(en)
    return not any(w[0].isupper() and w != "I" for w in words[1:])


def surface_part() -> list:
    rows = []
    rv = json.load(open(REPO / "results/m4b_mapping/verdict.json"))["curves"]
    ri = np.load(REPO / "results/m4b_mapping/items.npz")
    pv = json.load(open(REPO / "results/m4b_robustness/verdict.json"))["curves"]
    pi = np.load(REPO / "results/m4b_robustness/items.npz")
    for m in MODELS:
        for f in FORMS:
            for method, T, cv in (("ridge", ri[f"{m}__{f}__mapped"], rv[m][f]["cv_mapped"]),
                                  ("procrustes", pi[f"{m}__{f}__procrustes"], pv[f"{m}|{f}|procrustes"]["cv"])):
                lb = 1 + int(np.argmax(cv[1:]))
                c = boot(T[lb], T[0])
                rows.append({"model": m, "form": f, "map": method, "L0": T[0].mean(), "L0_ci": boot(T[0]),
                             "best_later_layer": lb, "Lb": T[lb].mean(), "Lb_ci": boot(T[lb]),
                             "gain": T[lb].mean() - T[0].mean(), "gain_ci": c, "status": status3(c)})
                print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in rows[-1].items()}, flush=True)
    return rows


def ind_boot(a: np.ndarray, b: np.ndarray, B: int = 10000, seed: int = 0) -> list:
    """CI of mean(a) - mean(b) for two independent samples (resampled separately)."""
    rng = np.random.default_rng(seed)
    da = np.array([a[rng.integers(0, len(a), len(a))].mean() for _ in range(B)])
    db = np.array([b[rng.integers(0, len(b), len(b))].mean() for _ in range(B)])
    return [float(x) for x in np.percentile(da - db, [2.5, 97.5])]


def subset_fit(m: str, tr: np.ndarray, te: np.ndarray, label: str) -> tuple[list, dict, dict]:
    folds = np.array_split(np.random.default_rng(SEED + 2).permutation(tr), N_FOLDS)
    E = np.load(ACT / m / "english.npz")["flores_states"]
    rows, best = [], {}
    for f in FORMS:
        X = np.load(ACT / m / f"{f}.npz")["flores_states"]
        res = [layer_fit(X[:, l], E[:, l], tr, te, folds) for l in range(X.shape[1])]
        cv = np.array([r["cv"] for r in res])
        lm, lu = int(cv.argmax()), int(np.argmax([r["unmapped_train"] for r in res]))
        lb = 1 + int(cv[1:].argmax())
        M = np.stack([r["mapped"] for r in res])
        best[f] = M[lm]
        g = boot(M[lb], M[0])
        rows.append({"model": m, "subset": label, "form": f, "n_train": len(tr), "n_test": len(te),
                     "mapped": M[lm].mean(), "mapped_ci": boot(M[lm]), "mapped_layer": lm,
                     "unmapped": res[lu]["unmapped"].mean(), "unmapped_ci": boot(res[lu]["unmapped"]),
                     "unmapped_layer": lu, "L0": M[0].mean(), "best_later_layer": lb, "Lb": M[lb].mean(),
                     "gain": M[lb].mean() - M[0].mean(), "gain_ci": g, "surface_status": status3(g),
                     "shuffled_control": res[lm]["shuffled"].mean()})
        print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in rows[-1].items()}, flush=True)
    c = boot(best["native"], best["itrans"])
    return rows, {"mapped_gap": float(best["native"].mean() - best["itrans"].mean()), "mapped_gap_ci": c,
                  "status": gap_status(c), "native_mapped": float(best["native"].mean()),
                  "itrans_mapped": float(best["itrans"].mean()),
                  "native_mapped_ci": boot(best["native"]), "itrans_mapped_ci": boot(best["itrans"])}, best


def main() -> None:
    import sys
    sys.path.insert(0, str(REPO / "scripts"))
    from m14_full import flores_forms
    out = results_dir("m4b_surface")
    S = pd.DataFrame(surface_part())
    S.to_csv(out / "surface.csv", index=False)

    F = flores_forms()
    n = 2009
    order = np.random.default_rng(SEED).permutation(n)
    tr, te = np.sort(order[: n // 2]), np.sort(order[n // 2:])
    keep = np.array([keep_sentence(s) for s in F["english"]])
    ktr, kte = tr[keep[tr]], te[keep[te]]
    rng = np.random.default_rng(3)
    rtr, rte = np.sort(rng.choice(tr, len(ktr), replace=False)), np.sort(rng.choice(te, len(kte), replace=False))
    latin_in_native = int(sum(bool(re.search(r"[0-9A-Za-z]", F["native"][i])) for i in np.r_[ktr, kte]))
    print({"kept_train": len(ktr), "kept_test": len(kte), "kept_native_with_digit_or_latin": latin_in_native}, flush=True)

    rows, gaps, vecs = [], {}, {}
    for m in MODELS:
        for label, a, b in (("filtered", ktr, kte), ("random_size_matched", rtr, rte)):
            r, g, v = subset_fit(m, a, b, label)
            rows += r
            gaps[f"{m}|{label}"], vecs[f"{m}|{label}"] = g, v
    D = pd.DataFrame(rows)
    D.to_csv(out / "subset.csv", index=False)

    # descriptive: filtered minus size-matched random, per form (independent bootstrap: different sentences)
    drop = {}
    for m in MODELS:
        drop[m] = {}
        for f in FORMS:
            a, b = vecs[f"{m}|filtered"][f], vecs[f"{m}|random_size_matched"][f]
            d = ind_boot(a, b)
            drop[m][f] = {"diff": float(a.mean() - b.mean()), "ci": d}
        drop[m]["itrans_drops_more_than_native"] = drop[m]["itrans"]["diff"] < drop[m]["native"]["diff"]
    sub3 = [gaps[f"{m}|filtered"]["status"] for m in MODELS[1:]]
    verdict = {
        "surface": {f"{r.model}|{r.form}|{r.map}": r.status for r in S.itertuples()},
        "subset_gap": gaps,
        "filtered_minus_random_mapped": drop,
        "prediction_gap_persists_filtered_3_models": all(s == "persists" for s in sub3),
        "gap_entity_dependent": sum(s == "closes" for s in sub3) >= 2,
        "n": {"kept_train": len(ktr), "kept_test": len(kte), "kept_native_with_digit_or_latin": latin_in_native},
    }
    write_json(out / "verdict.json", verdict, {"split_seed": SEED, "random_subset_seed": 3, "bootstrap": 10000,
                                               "registered": "RESULTS.md 2026-10-17 (surface baseline)"})
    pd.set_option("display.width", 250)
    print(S.drop(columns=["L0_ci", "Lb_ci"]).round(3).to_string(index=False))
    print(D.drop(columns=["mapped_ci", "unmapped_ci"]).round(3).to_string(index=False))
    print(json.dumps(verdict, indent=1, default=float))


if __name__ == "__main__":
    main()
