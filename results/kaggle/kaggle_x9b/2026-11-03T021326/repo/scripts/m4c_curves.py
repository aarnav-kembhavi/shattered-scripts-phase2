"""Per-layer English alignment on the M4c test half (post hoc descriptive, 2026-10-22, no verdict). CPU only: reads the
cached sentence vectors (cache/activations/m14full), loads no model.

For Qwen3.5-2B, Sarvam-1 and Gemma 4 E2B and the forms native, ITRANS and natural: unmapped retrieval acc@1 against
English at every layer, on the M4c test half (248 sentences, M4c's seed-0 split of the 496 retained), each form's and
English's vectors centered with their train-half means, 248 candidates. This is M4c's `unmapped_test` at every layer.
Check (asserted): at each form's train-half-best layer the curve equals results/m4c_natural/summary.csv `unmapped_test`.

Usage: python scripts/m4c_curves.py      Output: results/m4c_curves/curves.json
"""
import sys

import numpy as np
import pandas as pd

from shattered.runlog import REPO, results_dir, write_json

sys.path.insert(0, str(REPO / "scripts"))
from m4b_mapping import ACT, retrieval  # noqa: E402
from m4c_natural_flores import SEED, rows  # noqa: E402

MODELS = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
FORMS = ["native", "itrans", "natural"]


def main() -> None:
    R = rows()
    keep = np.array([not r["defective"] for r in R])
    idx = np.array([r["index"] for r in R])[keep]
    n = len(idx)
    order = np.random.default_rng(SEED).permutation(n)
    tr, te = np.sort(order[: n // 2]), np.sort(order[n // 2:])
    summary = pd.read_csv(REPO / "results" / "m4c_natural" / "summary.csv")
    out = {"n_test": int(len(te)), "n_train": int(len(tr)), "curves": {}, "best_layer_train": {}, "check": {}}
    for m in MODELS:
        E = np.load(ACT / m / "english.npz")["flores_states"][idx].astype(np.float64)
        nat = np.load(ACT / m / "natural500.npz")
        assert np.array_equal(nat["index"][keep], idx)
        forms = {"native": np.load(ACT / m / "native.npz")["flores_states"][idx],
                 "itrans": np.load(ACT / m / "itrans.npz")["flores_states"][idx],
                 "natural": nat["flores_states"][keep]}
        out["curves"][m], out["best_layer_train"][m], out["check"][m] = {}, {}, {}
        for f in FORMS:
            X = forms[f].astype(np.float64)
            test, train = [], []
            for l in range(X.shape[1]):
                mx, my = X[tr, l].mean(0), E[tr, l].mean(0)
                test.append(float(retrieval(X[te, l] - mx, E[te, l] - my).mean()))
                train.append(float(retrieval(X[tr, l] - mx, E[tr, l] - my).mean()))
            lu = int(np.argmax(train))
            stored = float(summary[(summary.model == m) & (summary.form == f)].unmapped_test.iloc[0])
            assert abs(test[lu] - stored) < 1e-9, (m, f, test[lu], stored)
            out["curves"][m][f] = test
            out["best_layer_train"][m][f] = lu
            out["check"][m][f] = {"layer": lu, "curve_value": test[lu], "m4c_summary_unmapped_test": stored}
            print(m, f, "layers", len(test), "train-best layer", lu, "value", round(test[lu], 3), flush=True)
    write_json(results_dir("m4c_curves") / "curves.json", out,
               {"status": "post hoc descriptive, 2026-10-22, no verdict", "sample": "M4c test half",
                "split_seed": SEED, "models": MODELS, "forms": FORMS, "measure": "unmapped retrieval acc@1, train-half "
                "centering, 248 candidates (as m4c_natural unmapped_test)"})


if __name__ == "__main__":
    main()
