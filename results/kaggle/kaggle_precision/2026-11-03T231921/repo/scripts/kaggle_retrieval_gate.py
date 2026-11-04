"""A1-R retrieval gate (Amendment 2): FLORES+ retrieval rescored on Kaggle for the two gate models in float16, native and ITRANS, same
2,009 sentences, same sentence vectors (mean residual over tokens, every layer), same M4b split (seed 0) and unmapped retrieval at the
layer chosen on the train half. Kaggle retrieval counts only if |Kaggle - laptop| <= 0.03 acc@1 for each model and form and no vector is
non-finite. Reads the private dataset `shattered-flores-private` (never public). Output: gate_retrieval.json with per-layer test accuracy
(so the same-layer comparison is also available), the chosen layers, the laptop values from results/m4b_mapping/summary.csv.
Usage: python scripts/kaggle_retrieval_gate.py --out DIR [--models sarvam-1 gemma4-e2b]
"""
import argparse
import glob
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from shattered.interp.collect import Sentence, collect
from shattered.interp.load import load
from shattered.translit import to_itrans

REPO = Path(__file__).resolve().parents[1]
TOL = 0.03
SEED = 0


def flores() -> dict:
    p = glob.glob("/kaggle/input/**/flores_private.json", recursive=True)
    p = p[0] if p else str(REPO / "build" / "kaggle" / "flores_private" / "flores_private.json")
    d = json.load(open(p, encoding="utf-8"))
    return {"native": d["kn"], "itrans": [" ".join(to_itrans(w) for w in s.split()) for s in d["kn"]], "english": d["en"]}


def retrieval(P: np.ndarray, Y: np.ndarray) -> np.ndarray:
    P = P / (np.linalg.norm(P, axis=1, keepdims=True) + 1e-8)
    Y = Y / (np.linalg.norm(Y, axis=1, keepdims=True) + 1e-8)
    return (P @ Y.T).argmax(1) == np.arange(len(P))


def unmapped_curves(X: np.ndarray, E: np.ndarray, tr: np.ndarray, te: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Per-layer unmapped retrieval, centered with train-half means as m4b_mapping.layer_fit: (train acc [L], test correctness [L, n_te])."""
    tr_acc, te_ok = [], []
    for l in range(X.shape[1]):
        x, y = X[:, l].astype(np.float64), E[:, l].astype(np.float64)
        mx, my = x[tr].mean(0), y[tr].mean(0)
        tr_acc.append(retrieval(x[tr] - mx, y[tr] - my).mean())
        te_ok.append(retrieval(x[te] - mx, y[te] - my))
    return np.array(tr_acc), np.stack(te_ok)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--models", nargs="+", default=["sarvam-1", "gemma4-e2b"])
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    F = flores()
    n = len(F["english"])
    assert n == 2009
    order = np.random.default_rng(SEED).permutation(n)
    tr, te = np.sort(order[: n // 2]), np.sort(order[n // 2:])
    laptop = pd.read_csv(REPO / "results" / "m4b_mapping" / "summary.csv").set_index(["model", "form"]) if (
        REPO / "results" / "m4b_mapping" / "summary.csv").exists() else None
    res = {"rule": {"tolerance_acc_at_1": TOL, "dtype": "float16"}, "models": {}}
    for m in a.models:
        t0 = time.time()
        model, tok = load(m, "cuda", dtype=torch.float16)
        st, nonfinite = {}, {}
        for f in ("english", "native", "itrans"):
            S = collect(model, tok, [Sentence(str(i), s, []) for i, s in enumerate(F[f])])["sent_states"]
            nonfinite[f] = int((~np.isfinite(S.astype(np.float32))).sum())
            st[f] = S.astype(np.float32)
            print(m, f, S.shape, "non-finite", nonfinite[f], f"{time.time() - t0:.0f}s", flush=True)
        r = {"seconds": time.time() - t0, "nonfinite": nonfinite, "forms": {}}
        for f in ("native", "itrans"):
            tra, tes = unmapped_curves(st[f], st["english"], tr, te)
            lu = int(tra.argmax())
            g = {"layer_kaggle": lu, "acc_kaggle": float(tes[lu].mean()), "test_acc_per_layer": tes.mean(1).tolist(),
                 "train_acc_per_layer": tra.tolist()}
            if laptop is not None and (m, f) in laptop.index:
                row = laptop.loc[(m, f)]
                g.update({"layer_laptop": int(row["best_layer_unmapped"]), "acc_laptop": float(row["unmapped"]),
                          "acc_kaggle_at_laptop_layer": float(tes[int(row["best_layer_unmapped"])].mean())})
                g["abs_diff"] = abs(g["acc_kaggle"] - g["acc_laptop"])
                g["pass"] = bool(g["abs_diff"] <= TOL and nonfinite[f] == 0 and nonfinite["english"] == 0)
            r["forms"][f] = g
        r["pass"] = bool(all(v.get("pass") for v in r["forms"].values()))
        res["models"][m] = r
        del model, st
        torch.cuda.empty_cache()
        (out / "gate_retrieval.json").write_text(json.dumps(res, indent=1))
        print(m, json.dumps({f: {k: v for k, v in g.items() if "per_layer" not in k} for f, g in r["forms"].items()}), flush=True)
    res["gate_passed"] = bool(all(v["pass"] for v in res["models"].values()))
    (out / "gate_retrieval.json").write_text(json.dumps(res, indent=1))
    print("A1-R gate_passed:", res["gate_passed"])


if __name__ == "__main__":
    main()
