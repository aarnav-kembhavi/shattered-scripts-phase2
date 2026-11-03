"""X1 T-c review (2026-11-02, Aarnav's request): all cells of results/phase2/x1/t2/analysis/tc_cells.csv.
Per model x task: number of significant T1 vs T2 shifts (McNemar p < 0.05, and Holm over all non-English cells); cells where the
sign of (native - romanized form) differs between T1 and T2; Pearson and Spearman correlation across cells of the form gaps.
Output: results/phase2/x1/t2/analysis/tc_review.json and tc_gaps.csv"""
import itertools
import json
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from statsmodels.stats.multitest import multipletests
from shattered.runlog import REPO, write_json

D = REPO / "results/phase2/x1/t2/analysis"
C = pd.read_csv(D / "tc_cells.csv")
C["p_holm_all"] = multipletests(C.p, method="holm")[1]
C["sig"], C["sig_holm"] = C.p < 0.05, C.p_holm_all < 0.05
shift = C.groupby(["model", "task"]).agg(cells=("p", "size"), sig_raw=("sig", "sum"), sig_holm=("sig_holm", "sum")).reset_index()
print(shift.to_string(index=False))
print("totals: cells", len(C), "sig raw", int(C.sig.sum()), "sig Holm", int(C.sig_holm.sum()))
print(C[C.sig_holm][["model", "task", "form", "acc_t1", "acc_t2", "diff", "p", "p_holm_all"]].to_string(index=False))
ROM = ["itrans", "lower", "lossy", "natural", "nc_a"]
rows = []
for (m, t), g in C.groupby(["model", "task"]):
    g = g.set_index("form")
    for f in ["itrans", "lower", "lossy", "natural"]:
        if f in g.index and "native" in g.index:
            rows.append({"model": m, "task": t, "form": f, "gap_t1": g.loc["native", "acc_t1"] - g.loc[f, "acc_t1"],
                         "gap_t2": g.loc["native", "acc_t2"] - g.loc[f, "acc_t2"], "n_form": int(g.loc[f, "n"])})
G = pd.DataFrame(rows)
G["sign_t1"], G["sign_t2"] = np.sign(G.gap_t1), np.sign(G.gap_t2)
G["sign_differs"] = G.sign_t1 != G.sign_t2
G.to_csv(D / "tc_gaps.csv", index=False)
print(G[G.sign_differs].to_string(index=False))
cor = {}
for t, g in G.groupby("task"):
    cor[t] = {"n_cells": len(g), "pearson": float(pearsonr(g.gap_t1, g.gap_t2)[0]), "spearman": float(spearmanr(g.gap_t1, g.gap_t2)[0]),
              "sign_differs": int(g.sign_differs.sum())}
print(json.dumps(cor, indent=1))
write_json(D / "tc_review.json", {"shift_counts": shift.to_dict("records"), "n_cells": len(C), "sig_raw": int(C.sig.sum()),
           "sig_holm": int(C.sig_holm.sum()), "gap_sign_differs": G[G.sign_differs].to_dict("records"), "gap_correlation": cor},
           {"note": "native - form accuracy gaps; natural rows use the native accuracy on the full item set; McNemar p as in tc_cells.csv"})
