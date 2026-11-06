"""K2b lexical-overlap control (exploratory; registered in RESULTS.md 2026-10-28 03:40 IST before this ran). CPU only: reads the
stored K2b vectors, loads tokenizers, no model. Usage: python scripts/k2b_overlap.py
Outputs: results/k12/k2b_overlap.csv, results/k12/k2b_overlap.json"""
import re
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm
from transformers import AutoTokenizer

from shattered.interp.load import MODELS as HF
from shattered.runlog import REPO, write_json
from shattered.translit.codemix import code_mixing, tag_v2

sys.path.insert(0, str(REPO / "scripts"))
import k_k12 as K  # noqa: E402
import l_ladder as lad  # noqa: E402

WORD = re.compile(r"[A-Za-z]+")
zz = lambda x: (x - x.mean()) / x.std()  # noqa: E731


def overlap_share(text: str, english: str) -> float:
    tags = tag_v2(text, english)
    E = {w.lower() for w in WORD.findall(english)}
    n = sum(g in ("en", "kn") for _, g in tags)
    return sum(g == "en" and w.lower() in E for w, g in tags) / n if n else 0.0


def main() -> int:
    items = K.k_items()["sib"]
    m4b = pd.read_csv(REPO / "results/m4b_mapping/summary.csv")
    te = np.load(REPO / "results/m4b_mapping/items.npz")["test_idx"]
    pos = {int(i): k for k, i in enumerate(te)}
    txt = [it["forms"]["k_kan_ver"]["text"] for it in items]
    eng = [it["english"] for it in items]
    SH = {"v2": np.array([sum(g == "en" for _, g in tag_v2(t, e)) / max(1, sum(g in ("en", "kn") for _, g in tag_v2(t, e)))
                          for t, e in zip(txt, eng)]),
          "v1": np.array([code_mixing(t)["english_share"] for t in txt])}
    OV = np.array([overlap_share(t, e) for t, e in zip(txt, eng)])
    rows = []
    for m in K.M4_MODELS:
        L = int(m4b[(m4b.model == m) & (m4b.form == "native")].best_layer_unmapped.item())
        z_ = np.load(K.VEC / f"{m}__k_kan_ver300.npz")
        X = z_["sent_states"][:, L].astype(np.float64)
        E = np.load(lad.ACT / m / "english.npz")["flores_states"][te, L].astype(np.float64)
        X /= np.linalg.norm(X, axis=1, keepdims=True)
        E /= np.linalg.norm(E, axis=1, keepdims=True)
        sims = X @ E.T
        rank = np.array([1 + int((sims[k] > sims[k, pos[int(i)]]).sum()) for k, i in enumerate(z_["index"])])
        tok = AutoTokenizer.from_pretrained(HF[m])
        lt = np.log([len(tok(t, add_special_tokens=False)["input_ids"]) for t in txt])
        y = -np.log(rank)
        for tg in ("v2", "v1"):
            sh = SH[tg]
            a = sm.OLS(y, sm.add_constant(np.column_stack([zz(sh), zz(lt)]))).fit()
            b = sm.OLS(y, sm.add_constant(np.column_stack([zz(sh), zz(lt), zz(OV)]))).fit()
            c = sm.OLS(y, sm.add_constant(np.column_stack([zz(OV), zz(lt)]))).fit()
            ca, cb, cc = a.conf_int()[1], b.conf_int()[1], c.conf_int()[1]
            rows.append({"tagger": tg, "model": m, "layer": L, "n": len(y),
                         "corr_share_overlap": float(np.corrcoef(sh, OV)[0, 1]), "mean_share": float(sh.mean()),
                         "mean_overlap": float(OV.mean()),
                         "share_coef_without": float(a.params[1]), "share_ci_without_low": float(ca[0]), "share_ci_without_high": float(ca[1]),
                         "share_coef_with": float(b.params[1]), "share_ci_with_low": float(cb[0]), "share_ci_with_high": float(cb[1]),
                         "share_p_with_two_sided": float(b.pvalues[1]),
                         "overlap_coef_with": float(b.params[3]), "overlap_ci_low": float(b.conf_int()[3][0]),
                         "overlap_ci_high": float(b.conf_int()[3][1]),
                         "overlap_only_coef": float(c.params[1]), "overlap_only_ci_low": float(cc[0]), "overlap_only_ci_high": float(cc[1])})
    R = pd.DataFrame(rows)
    R.to_csv(K.OUT / "k2b_overlap.csv", index=False)
    write_json(K.OUT / "k2b_overlap.json", {"rows": len(R)}, {"registered": "RESULTS.md 2026-10-28 03:40 IST (exploratory, no verdict)"})
    pd.set_option("display.width", 250)
    print(R.round(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
