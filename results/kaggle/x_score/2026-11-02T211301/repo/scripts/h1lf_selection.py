"""H1-LF selection check (exploratory; registered in RESULTS.md 2026-10-28 06:20 IST before this ran). CPU only; tokenizer only.
Usage: python scripts/h1lf_selection.py     Outputs: results/h1lf/selection_desc.csv, selection_topics.csv, selection_fit.csv"""
import re
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import chi2_contingency, fisher_exact, mannwhitneyu
from statsmodels.stats.multitest import multipletests
from transformers import AutoTokenizer

from shattered.interp.load import MODELS as HF
from shattered.runlog import REPO, results_dir, write_json
from shattered.translit.codemix import names_in

sys.path.insert(0, str(REPO / "scripts"))
import english_share as es  # noqa: E402
import h1lf as H  # noqa: E402
import h_hindi as hh  # noqa: E402
import l_ladder as lad  # noqa: E402

OUT = results_dir("h1lf")


def main() -> int:
    wl = es.wordlists()["zipf>=3"]
    nk, nh = H.clean1("kannada"), H.clean1("hindi")
    both = sorted(set(nk) & set(nh))
    eng = H.english_of()
    free = set(i for i in both if not H.v2_loans(nk[i], eng[("m4c", i)], wl)[0] and not H.v2_loans(nh[i], eng[("m4c", i)], wl)[0])
    items = {int(it["id"]): it for it in lad.e0c_items()["sib"]}
    tok = AutoTokenizer.from_pretrained(HF["qwen3-1.7b"])
    rows = []
    for i in both:
        e = eng[("m4c", i)]
        kn = items[i]["forms"]["native"]["text"]
        rows.append({"id": i, "loan_free": int(i in free), "topic": items[i]["label"], "en_words": len(es.words(e)),
                     "kn_words": len(kn.split()), "kn_tokens": len(tok(kn, add_special_tokens=False)["input_ids"]),
                     "has_digit": int(bool(re.search(r"\d", e))), "has_name": int(bool(names_in(e)))})
    X = pd.DataFrame(rows).set_index("id")
    desc = []
    for c in ("en_words", "kn_words", "kn_tokens"):
        a, b = X[X.loan_free == 1][c], X[X.loan_free == 0][c]
        desc.append({"measure": c, "loan_free_mean": a.mean(), "other_mean": b.mean(), "all_mean": X[c].mean(),
                     "std_diff": (a.mean() - b.mean()) / X[c].std(), "p": float(mannwhitneyu(a, b).pvalue)})
    for c in ("has_digit", "has_name"):
        t = pd.crosstab(X.loan_free, X[c]).reindex(index=[0, 1], columns=[0, 1], fill_value=0).to_numpy()
        desc.append({"measure": c, "loan_free_mean": X[X.loan_free == 1][c].mean(), "other_mean": X[X.loan_free == 0][c].mean(),
                     "all_mean": X[c].mean(), "std_diff": np.nan, "p": float(fisher_exact(t)[1])})
    D = pd.DataFrame(desc)
    tp = pd.crosstab(X.topic, X.loan_free)
    topics = pd.DataFrame({"n_loan_free": tp[1], "n_other": tp[0], "share_loan_free": tp[1] / tp[1].sum(),
                           "share_all": (tp[0] + tp[1]) / len(X)}).reset_index()
    chi_p = float(chi2_contingency(tp.to_numpy())[1])
    # item-level gap per model (as analyse1)
    K = pd.concat([H.scored({"sib": lad.E0C_DIR}, ["native"]), H.scored({"sib": H.SCORE1["kannada"]}, [H.FORM1])])
    Hh = pd.concat([H.scored({"sib": hh.SCORE_DIRS["sib"]}, ["native"]), H.scored({"sib": H.SCORE1["hindi"]}, [H.FORM1])])
    T = pd.get_dummies(X.topic, drop_first=True, dtype=float)
    Z = X[["en_words", "kn_tokens"]].apply(lambda v: (v - v.mean()) / v.std())
    C = pd.concat([X[["loan_free"]].astype(float), Z, X[["has_digit", "has_name"]].astype(float), T - T.mean()], axis=1)
    C["has_digit"] -= C.has_digit.mean(); C["has_name"] -= C.has_name.mean()
    C = sm.add_constant(C)
    fits = []
    for m in lad.COUNT_ACC:
        a = K[K.model == m].pivot_table(index="id", columns="form", values="correct").loc[both]
        b = Hh[Hh.model == m].pivot_table(index="id", columns="form", values="correct").loc[both]
        d = ((a["native"] - a[H.FORM1]) - (b["native"] - b[H.FORM1]))
        f = sm.OLS(d.to_numpy(float), C.to_numpy(float)).fit(cov_type="HC3")
        names = list(C.columns)
        v = np.zeros(len(names)); v[0] = 1; v[1] = 1
        adj = f.t_test(v)
        ci = adj.conf_int()[0]
        fits.append({"model": m, "n": len(d), "n_loan_free": int(X.loan_free.sum()),
                     "unadjusted_loan_free_gap": float(d[X.loan_free == 1].mean()), "unadjusted_other_gap": float(d[X.loan_free == 0].mean()),
                     "adjusted_loan_free_gap": float(adj.effect[0]), "adj_ci_low": float(ci[0]), "adj_ci_high": float(ci[1]),
                     "adj_p": float(adj.pvalue), "indicator_coef": float(f.params[1]),
                     "ind_ci_low": float(f.conf_int()[1][0]), "ind_ci_high": float(f.conf_int()[1][1]), "ind_p": float(f.pvalues[1])})
    F = pd.DataFrame(fits)
    F["adj_p_holm"] = multipletests(F.adj_p, method="holm")[1]
    D.to_csv(OUT / "selection_desc.csv", index=False); topics.to_csv(OUT / "selection_topics.csv", index=False)
    F.to_csv(OUT / "selection_fit.csv", index=False)
    write_json(OUT / "selection.json", {"n_all": len(X), "n_loan_free": int(X.loan_free.sum()), "topic_chi2_p": chi_p,
                                        "covariates": list(C.columns)}, {"registered": "RESULTS.md 2026-10-28 06:20 IST (exploratory)"})
    pd.set_option("display.width", 250)
    print(D.round(3).to_string(index=False)); print(topics.round(3).to_string(index=False)); print("topic chi2 p", round(chi_p, 4))
    print(F.round(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
