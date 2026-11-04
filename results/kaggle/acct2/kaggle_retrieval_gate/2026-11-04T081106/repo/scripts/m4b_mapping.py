"""M4b linear mapping test (pre-registered in RESULTS.md, 2026-10-16). For each model, form and layer: ridge map from
the form's FLORES+ sentence vectors to the English ones, fitted on a random 50% (seed 0), retrieval acc@1 on the other
50%. Unmapped retrieval on the same test half. No model is run: uses the cached vectors in cache/activations/m14full.

Ridge (dual form, linear kernel, features centered with train-half means): lambda = alpha * mean squared row norm,
alpha chosen per (model, form, layer) by 5-fold CV retrieval acc@1 on the train half. Best layer chosen on the train
half (CV retrieval for mapped, train-half retrieval for unmapped), then evaluated once on the test half.
Control: the same ridge (same alpha) fitted on shuffled train pairs, at the mapped best layer.

Usage: python scripts/m4b_mapping.py [--models ...] [--forms native itrans]
Outputs (results/m4b_mapping/): curves.json, summary.csv, verdict.json, items.npz (test correctness per layer)
"""
import argparse
import json

import numpy as np
import pandas as pd

from shattered.interp.clustered import B, CHUNK, ci
from shattered.runlog import REPO, results_dir, write_json

MODELS = ["qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
ALPHAS = [1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0]
N_FOLDS, SEED = 5, 0
ACT = REPO / "cache" / "activations" / "m14full"


def retrieval(P: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """Row i of P should retrieve row i of Y (cosine); returns correctness [n]."""
    P = P / (np.linalg.norm(P, axis=1, keepdims=True) + 1e-8)
    Y = Y / (np.linalg.norm(Y, axis=1, keepdims=True) + 1e-8)
    return (P @ Y.T).argmax(1) == np.arange(len(P))


class DualRidge:
    """Ridge from X to Y in dual form; one eigendecomposition serves every lambda."""

    def __init__(self, X: np.ndarray, Y: np.ndarray):
        self.X, self.Y = X, Y
        self.s, self.U = np.linalg.eigh(X @ X.T)
        self.UtY = self.U.T @ Y
        self.scale = float(np.einsum("ij,ij->", X, X) / len(X))  # mean squared row norm

    def predict(self, Xq: np.ndarray, alpha: float) -> np.ndarray:
        lam = alpha * self.scale
        A = self.U @ (self.UtY / (self.s + lam)[:, None])  # (K + lam I)^-1 Y
        return (Xq @ self.X.T) @ A


def layer_fit(X: np.ndarray, Y: np.ndarray, tr: np.ndarray, te: np.ndarray, folds: list) -> dict:
    """X, Y [n, d] for one layer. Returns CV scores, chosen alpha, mapped/unmapped test correctness, train-half
    unmapped retrieval, and the shuffled-pair control."""
    X, Y = X.astype(np.float64), Y.astype(np.float64)
    cv = np.zeros(len(ALPHAS))
    for f in folds:
        fit_idx = np.setdiff1d(tr, f)
        mx, my = X[fit_idx].mean(0), Y[fit_idx].mean(0)
        r = DualRidge(X[fit_idx] - mx, Y[fit_idx] - my)
        for k, a in enumerate(ALPHAS):
            cv[k] += retrieval(r.predict(X[f] - mx, a), Y[f] - my).mean() / len(folds)
    a = ALPHAS[int(cv.argmax())]
    mx, my = X[tr].mean(0), Y[tr].mean(0)
    r = DualRidge(X[tr] - mx, Y[tr] - my)
    mapped = retrieval(r.predict(X[te] - mx, a), Y[te] - my)
    unmapped = retrieval(X[te] - mx, Y[te] - my)
    unmapped_train = retrieval(X[tr] - mx, Y[tr] - my).mean()
    perm = np.random.default_rng(SEED + 1).permutation(len(tr))
    rs = DualRidge(X[tr] - mx, Y[tr][perm] - my)
    shuffled = retrieval(rs.predict(X[te] - mx, a), Y[te] - my)
    return {"cv": float(cv.max()), "alpha": a, "mapped": mapped, "unmapped": unmapped,
            "unmapped_train": float(unmapped_train), "shuffled": shuffled}


def boot(a: np.ndarray, b: np.ndarray | None = None, seed: int = 0) -> list:
    """CI of mean(a) or of mean(a) - mean(b), paired over test sentences."""
    n, rng, out = len(a), np.random.default_rng(seed), []
    x = a.astype(np.float32) - (0 if b is None else b.astype(np.float32))
    for s in range(0, B, CHUNK):
        w = rng.multinomial(n, np.full(n, 1 / n), size=min(CHUNK, B - s)).astype(np.float32)
        out.append(w @ x / n)
    return ci(np.concatenate(out))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=MODELS)
    ap.add_argument("--forms", nargs="+", default=["native", "itrans"])
    args = ap.parse_args()
    out = results_dir("m4b_mapping")
    n = 2009
    order = np.random.default_rng(SEED).permutation(n)
    tr, te = np.sort(order[: n // 2]), np.sort(order[n // 2:])
    folds = np.array_split(np.random.default_rng(SEED + 2).permutation(tr), N_FOLDS)
    curves, rows, items = {}, [], {}
    for m in args.models:
        E = np.load(ACT / m / "english.npz")["flores_states"]
        assert E.shape[0] == n
        curves[m] = {}
        for f in args.forms:
            X = np.load(ACT / m / f"{f}.npz")["flores_states"]
            res = [layer_fit(X[:, l], E[:, l], tr, te, folds) for l in range(X.shape[1])]
            cvs = np.array([r["cv"] for r in res])
            utr = np.array([r["unmapped_train"] for r in res])
            lm, lu = int(cvs.argmax()), int(utr.argmax())
            M = np.stack([r["mapped"] for r in res])
            U = np.stack([r["unmapped"] for r in res])
            items[f"{m}__{f}__mapped"], items[f"{m}__{f}__unmapped"] = M, U
            curves[m][f] = {"mapped_test": M.mean(1).tolist(), "unmapped_test": U.mean(1).tolist(),
                            "cv_mapped": cvs.tolist(), "unmapped_train": utr.tolist(),
                            "alpha": [r["alpha"] for r in res]}
            rows.append({"model": m, "form": f, "n_layers": X.shape[1] - 1, "best_layer_mapped": lm,
                         "mapped": M[lm].mean(), "mapped_ci": boot(M[lm]), "alpha": res[lm]["alpha"],
                         "best_layer_unmapped": lu, "unmapped": U[lu].mean(), "unmapped_ci": boot(U[lu]),
                         "mapped_minus_unmapped_ci": boot(M[lm], U[lu]),
                         "shuffled_control": res[lm]["shuffled"].mean(),
                         "max_test_mapped_any_layer": M.mean(1).max(), "max_test_unmapped_any_layer": U.mean(1).max()})
            items[f"{m}__{f}__best"] = np.array([lm, lu])
            print(f"{m}/{f}: mapped {M[lm].mean():.3f} (layer {lm}, alpha {res[lm]['alpha']}) unmapped "
                  f"{U[lu].mean():.3f} (layer {lu}) shuffled {res[lm]['shuffled'].mean():.4f}", flush=True)
    S = pd.DataFrame(rows)
    S.to_csv(out / "summary.csv", index=False)
    np.savez_compressed(out / "items.npz", **items, test_idx=te)
    verdict = {}
    if {"native", "itrans"} <= set(args.forms):
        per = {}
        for m in args.models:
            bn, bi = items[f"{m}__native__best"], items[f"{m}__itrans__best"]
            Mn, Mi = items[f"{m}__native__mapped"][bn[0]], items[f"{m}__itrans__mapped"][bi[0]]
            Un, Ui = items[f"{m}__native__unmapped"][bn[1]], items[f"{m}__itrans__unmapped"][bi[1]]
            g, c = Mn.mean() - Mi.mean(), boot(Mn, Mi)
            ug = Un.mean() - Ui.mean()
            per[m] = {"mapped_gap": g, "mapped_gap_ci": c, "unmapped_gap": ug, "unmapped_gap_ci": boot(Un, Ui),
                      "share_of_unmapped_gap_remaining": g / ug if ug > 0 else None,
                      "itrans_mapped_minus_unmapped_ci": boot(Mi, Ui),
                      "status": "persists" if c[0] > 0.10 else "closes" if c[1] < 0.10 else "partial"}
        st = [v["status"] for v in per.values()]
        verdict = {"per_model": per,
                   "strong_H1": "supported" if all(s == "persists" for s in st) else
                   "refuted" if sum(s == "closes" for s in st) >= 3 else "inconclusive"}
    write_json(out / "verdict.json", {"verdict": verdict, "curves": curves},
               {"split_seed": SEED, "n_train": len(tr), "n_test": len(te), "alphas": ALPHAS, "folds": N_FOLDS,
                "bootstrap": B, "registered": "RESULTS.md 2026-10-16"})
    pd.set_option("display.width", 250)
    print(S.round(3).to_string(index=False))
    print(json.dumps(verdict, indent=1, default=float))


if __name__ == "__main__":
    main()
