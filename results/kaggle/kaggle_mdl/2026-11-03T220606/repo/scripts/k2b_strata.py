"""K2b overlap control, robustness (exploratory; registered in RESULTS.md 2026-10-29 02:00 IST before this ran). CPU only.
VIF of the three predictors; English-share coefficient within overlap-share quintile bins (pooled, bin fixed effects).
Usage: python scripts/k2b_strata.py   Outputs: results/k12/k2b_strata.csv, k2b_strata_bins.csv, k2b_strata.json"""
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from transformers import AutoTokenizer

from shattered.interp.load import MODELS as HF
from shattered.runlog import REPO, write_json
from shattered.translit.codemix import tag_v2

sys.path.insert(0, str(REPO / "scripts"))
import k2b_overlap as O  # noqa: E402
import k_k12 as K  # noqa: E402
import l_ladder as lad  # noqa: E402


def main() -> int:
    items = K.k_items()["sib"]
    m4b = pd.read_csv(REPO / "results/m4b_mapping/summary.csv")
    te = np.load(REPO / "results/m4b_mapping/items.npz")["test_idx"]
    pos = {int(i): k for k, i in enumerate(te)}
    txt = [it["forms"]["k_kan_ver"]["text"] for it in items]
    eng = [it["english"] for it in items]
    sh = np.array([sum(g == "en" for _, g in tag_v2(t, e)) / max(1, sum(g in ("en", "kn") for _, g in tag_v2(t, e)))
                   for t, e in zip(txt, eng)])
    ov = np.array([O.overlap_share(t, e) for t, e in zip(txt, eng)])
    bins = pd.qcut(ov, 5, labels=False, duplicates="drop")
    nb = int(pd.Series(bins).nunique())
    sizes = pd.Series(bins).value_counts().sort_index().tolist()
    rows, brow = [], []
    for m in K.M4_MODELS:
        L = int(m4b[(m4b.model == m) & (m4b.form == "native")].best_layer_unmapped.item())
        z_ = np.load(K.VEC / f"{m}__k_kan_ver300.npz")
        X = z_["sent_states"][:, L].astype(np.float64)
        E = np.load(lad.ACT / m / "english.npz")["flores_states"][te, L].astype(np.float64)
        X /= np.linalg.norm(X, axis=1, keepdims=True); E /= np.linalg.norm(E, axis=1, keepdims=True)
        sims = X @ E.T
        rank = np.array([1 + int((sims[k] > sims[k, pos[int(i)]]).sum()) for k, i in enumerate(z_["index"])])
        tok = AutoTokenizer.from_pretrained(HF[m])
        lt = np.log([len(tok(t, add_special_tokens=False)["input_ids"]) for t in txt])
        y = -np.log(rank)
        zz = O.zz
        D3 = sm.add_constant(np.column_stack([zz(sh), zz(ov), zz(lt)]))
        vif = [float(variance_inflation_factor(D3, j)) for j in (1, 2, 3)]
        F = pd.get_dummies(pd.Series(bins), drop_first=True, dtype=float).to_numpy()
        f = sm.OLS(y, np.column_stack([np.ones(len(y)), zz(sh), zz(lt), F])).fit(cov_type="HC3")
        ci = f.conf_int()[1]
        r = {"model": m, "layer": L, "n": len(y), "n_bins": nb, "vif_share": vif[0], "vif_overlap": vif[1], "vif_logtok": vif[2],
             "share_coef_within_bins": float(f.params[1]), "ci_low": float(ci[0]), "ci_high": float(ci[1]), "p": float(f.pvalues[1])}
        rows.append(r)
        for b in range(nb):
            k = bins == b
            if k.sum() > 5 and sh[k].std() > 0:
                g = sm.OLS(y[k], sm.add_constant(np.column_stack([zz(sh[k]), zz(lt[k])]))).fit(cov_type="HC3")
                brow.append({"model": m, "bin": b, "n": int(k.sum()), "mean_overlap": float(ov[k].mean()),
                             "share_coef": float(g.params[1]), "ci_low": float(g.conf_int()[1][0]), "ci_high": float(g.conf_int()[1][1])})
    R = pd.DataFrame(rows)
    R.to_csv(K.OUT / "k2b_strata.csv", index=False)
    pd.DataFrame(brow).to_csv(K.OUT / "k2b_strata_bins.csv", index=False)
    write_json(K.OUT / "k2b_strata.json", {"n_bins": nb, "bin_sizes": sizes, "tagger": "v2"},
               {"registered": "RESULTS.md 2026-10-29 02:00 IST (exploratory, no verdict)"})
    pd.set_option("display.width", 250)
    print("bins", nb, sizes); print(R.round(3).to_string(index=False)); print(pd.DataFrame(brow).round(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
