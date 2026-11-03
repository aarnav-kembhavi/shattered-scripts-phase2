"""Surface baseline for the natural form (addendum of 2026-10-21 to the M4b surface-baseline registration). On the M4c
sample (496 retained sentences, M4c's seed-0 50/50 split and folds, M4b ridge grid): per model x form (native, ITRANS,
natural), L0 = mapped test retrieval at layer 0, Lb = at the train-half-CV-best layer >= 1, gain = Lb - L0 (paired
bootstrap CI); beyond surface / surface-level / partial as in scripts/m4b_surface.py. CPU only.

Usage: python scripts/m4c_surface.py      Outputs: results/m4c_surface/{surface.csv, verdict.json}
"""
import numpy as np
import pandas as pd

from m4b_mapping import ACT, MODELS, boot, layer_fit
from m4b_surface import status3
from m4c_natural_flores import SEED, rows
from shattered.runlog import results_dir, write_json


def main() -> None:
    R = rows()
    keep = np.array([not r["defective"] for r in R])
    idx = np.array([r["index"] for r in R])[keep]
    n = len(idx)
    order = np.random.default_rng(SEED).permutation(n)
    tr, te = np.sort(order[: n // 2]), np.sort(order[n // 2:])
    folds = np.array_split(np.random.default_rng(SEED + 2).permutation(tr), 5)
    out, res = results_dir("m4c_surface"), []
    for m in MODELS:
        E = np.load(ACT / m / "english.npz")["flores_states"][idx]
        nat = np.load(ACT / m / "natural500.npz")
        assert np.array_equal(nat["index"][keep], idx)
        forms = {"native": np.load(ACT / m / "native.npz")["flores_states"][idx],
                 "itrans": np.load(ACT / m / "itrans.npz")["flores_states"][idx],
                 "natural": nat["flores_states"][keep]}
        for f, X in forms.items():
            fits = [layer_fit(X[:, l], E[:, l], tr, te, folds) for l in range(X.shape[1])]
            cv = np.array([r["cv"] for r in fits])
            lb = 1 + int(cv[1:].argmax())
            L0, Lb = fits[0]["mapped"], fits[lb]["mapped"]
            c = boot(Lb, L0)
            res.append({"model": m, "form": f, "n_test": len(te), "L0": L0.mean(), "L0_ci": boot(L0),
                        "best_later_layer": lb, "Lb": Lb.mean(), "Lb_ci": boot(Lb), "gain": Lb.mean() - L0.mean(),
                        "gain_ci": c, "status": status3(c)})
            print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in res[-1].items()}, flush=True)
    S = pd.DataFrame(res)
    S.to_csv(out / "surface.csv", index=False)
    write_json(out / "verdict.json", {"status": {f"{r.model}|{r.form}": r.status for r in S.itertuples()},
                                      "n_sentences": n},
               {"sample": "M4c 496 retained", "split_seed": SEED,
                "registered": "RESULTS.md 2026-10-21 (addendum, natural surface baseline)"})


if __name__ == "__main__":
    main()
