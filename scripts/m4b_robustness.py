"""M4b robustness check (registered in RESULTS.md, 2026-10-16, before running). Same cached vectors, split (seed 0),
folds and train-half layer selection as scripts/m4b_mapping.py; two alternative maps:

- ridge_wide: the M4b dual ridge with a wider alpha grid (1e-6 ... 1e3), CV-tuned on the train half. M4b's grid
  bottomed out at 1e-3, which Qwen2.5 chose at most layers.
- procrustes: orthogonal Procrustes between the top-k PCA subspaces of the form and of English (both fitted on the
  fitting rows, centered, rows unit-normalized), k CV-tuned in {32, 64, 128, 256, 512}; retrieval by cosine in the
  English PCA space. An orthogonal map cannot distort geometry, so it tests whether the form's space is a rotation of
  the English one.

The registered M4b status rule is applied to each: per model, persists if the CI lower bound of the mapped gap
(native - ITRANS) > 0.10, closes if the CI upper bound < 0.10, partial otherwise.

Usage: python scripts/m4b_robustness.py
Outputs (results/m4b_robustness/): summary.csv, verdict.json, items.npz
"""
import json

import numpy as np
import pandas as pd

from m4b_mapping import ACT, MODELS, N_FOLDS, SEED, DualRidge, boot, retrieval
from shattered.runlog import results_dir, write_json

ALPHAS_WIDE = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0, 1000.0]
KS = [32, 64, 128, 256, 512]


def _unit(A: np.ndarray) -> np.ndarray:
    return A / (np.linalg.norm(A, axis=1, keepdims=True) + 1e-8)


class Procrustes:
    def __init__(self, X: np.ndarray, Y: np.ndarray):
        self.mx, self.my = X.mean(0), Y.mean(0)
        self.Vx = np.linalg.svd(X - self.mx, full_matrices=False)[2]
        self.Vy = np.linalg.svd(Y - self.my, full_matrices=False)[2]
        self.X, self.Y = X, Y

    def retrieve(self, Xq: np.ndarray, Yq: np.ndarray, k: int) -> np.ndarray:
        vx, vy = self.Vx[:k].T, self.Vy[:k].T
        A, Bm = _unit((self.X - self.mx) @ vx), _unit((self.Y - self.my) @ vy)
        u, _, vt = np.linalg.svd(A.T @ Bm)
        P = _unit((Xq - self.mx) @ vx) @ (u @ vt)
        return retrieval(P, (Yq - self.my) @ vy)


def ridge_fit(X, Y, tr, te, folds):
    cv = np.zeros(len(ALPHAS_WIDE))
    for f in folds:
        fi = np.setdiff1d(tr, f)
        mx, my = X[fi].mean(0), Y[fi].mean(0)
        r = DualRidge(X[fi] - mx, Y[fi] - my)
        for j, a in enumerate(ALPHAS_WIDE):
            cv[j] += retrieval(r.predict(X[f] - mx, a), Y[f] - my).mean() / len(folds)
    a = ALPHAS_WIDE[int(cv.argmax())]
    mx, my = X[tr].mean(0), Y[tr].mean(0)
    test = retrieval(DualRidge(X[tr] - mx, Y[tr] - my).predict(X[te] - mx, a), Y[te] - my)
    return float(cv.max()), a, test


def procrustes_fit(X, Y, tr, te, folds):
    cv = np.zeros(len(KS))
    for f in folds:
        fi = np.setdiff1d(tr, f)
        p = Procrustes(X[fi], Y[fi])
        for j, k in enumerate(KS):
            cv[j] += p.retrieve(X[f], Y[f], k).mean() / len(folds)
    k = KS[int(cv.argmax())]
    return float(cv.max()), k, Procrustes(X[tr], Y[tr]).retrieve(X[te], Y[te], k)


def main() -> None:
    out = results_dir("m4b_robustness")
    n = 2009
    order = np.random.default_rng(SEED).permutation(n)
    tr, te = np.sort(order[: n // 2]), np.sort(order[n // 2:])
    folds = np.array_split(np.random.default_rng(SEED + 2).permutation(tr), N_FOLDS)
    rows, items, curves = [], {}, {}
    for m in MODELS:
        E = np.load(ACT / m / "english.npz")["flores_states"].astype(np.float64)
        for f in ("native", "itrans"):
            X = np.load(ACT / m / f"{f}.npz")["flores_states"].astype(np.float64)
            for method, fit in (("ridge_wide", ridge_fit), ("procrustes", procrustes_fit)):
                res = [fit(X[:, l], E[:, l], tr, te, folds) for l in range(X.shape[1])]
                cv = np.array([r[0] for r in res])
                lb = int(cv.argmax())
                T = np.stack([r[2] for r in res])
                items[f"{m}__{f}__{method}"], items[f"{m}__{f}__{method}__best"] = T, np.array([lb])
                curves[f"{m}|{f}|{method}"] = {"cv": cv.tolist(), "test": T.mean(1).tolist(),
                                               "hyper": [r[1] for r in res]}
                rows.append({"model": m, "form": f, "method": method, "best_layer": lb, "hyper": res[lb][1],
                             "hyper_at_grid_edge": res[lb][1] in (ALPHAS_WIDE[0], ALPHAS_WIDE[-1], KS[0], KS[-1]),
                             "mapped": T[lb].mean(), "mapped_ci": boot(T[lb]),
                             "max_test_any_layer": T.mean(1).max(), "argmax_test_layer": int(T.mean(1).argmax())})
                print(rows[-1], flush=True)
    S = pd.DataFrame(rows)
    S.to_csv(out / "summary.csv", index=False)
    np.savez_compressed(out / "items.npz", **items, test_idx=te)
    m4b = json.load(open(out.parent / "m4b_mapping" / "verdict.json"))
    m4b = (m4b.get("result") or m4b)["verdict"]["per_model"]
    verdict = {}
    for method in ("ridge_wide", "procrustes"):
        per = {}
        for m in MODELS:
            a = items[f"{m}__native__{method}"][items[f"{m}__native__{method}__best"][0]]
            b = items[f"{m}__itrans__{method}"][items[f"{m}__itrans__{method}__best"][0]]
            c = boot(a, b)
            per[m] = {"mapped_gap": float(a.mean() - b.mean()), "mapped_gap_ci": c,
                      "status": "persists" if c[0] > 0.10 else "closes" if c[1] < 0.10 else "partial",
                      "m4b_status": m4b[m]["status"]}
        st = [v["status"] for v in per.values()]
        verdict[method] = {"per_model": per, "same_status_as_m4b_all_models":
                           all(v["status"] == v["m4b_status"] for v in per.values()),
                           "strong_H1": "supported" if all(s == "persists" for s in st) else
                           "refuted" if sum(s == "closes" for s in st) >= 3 else "inconclusive"}
    write_json(out / "verdict.json", {"verdict": verdict, "curves": curves},
               {"split_seed": SEED, "n_train": len(tr), "n_test": len(te), "alphas": ALPHAS_WIDE, "pca_k": KS,
                "folds": N_FOLDS, "registered": "RESULTS.md 2026-10-16 (robustness check)"})
    pd.set_option("display.width", 250)
    print(S.drop(columns="mapped_ci").round(3).to_string(index=False))
    print(json.dumps(verdict, indent=1, default=float))


if __name__ == "__main__":
    main()
