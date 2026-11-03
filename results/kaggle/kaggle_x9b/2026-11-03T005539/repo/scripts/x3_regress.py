"""X3 exploratory corpus-frequency regression (defined in RESULTS.md, PHASE 2 CLARIFICATIONS C2, 2026-11-02, before this run).
Per model and measure (SIB-200 items, eligible M4c test sentences), per comparison split (c = the s_int-matched split; NC-O):
  x_i = mean s_ref(canonical span pieces) - mean s_ref(split span pieces);  y_i = correct(canonical) - correct(split);  OLS y = b0 + b1 x.
b0 = accuracy change at zero corpus-frequency difference; 95% CIs by item bootstrap (10,000, seed 0). Exploratory, no verdict.
Needs results/phase2/x3/per_item.csv (written by scripts/x3_analyse.py). Output: results/phase2/x3/regression.csv
"""
import sys

import numpy as np
import pandas as pd
from transformers import AutoTokenizer

from shattered.interp.load import MODELS as REPOS
from shattered.runlog import REPO, write_json
from shattered.translit import to_lossy

sys.path.insert(0, str(REPO / "scripts"))
import l_ladder as lad  # noqa: E402
import nc1  # noqa: E402
import x3  # noqa: E402

N_BOOT = 10_000


def mean_ref(info: list, sc) -> float:
    return float(np.mean([sc.piece(p) for u in info for p in u["pieces"]]))


def ols(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    xm, ym = x.mean(), y.mean()
    b1 = ((x - xm) * (y - ym)).sum() / max(((x - xm) ** 2).sum(), 1e-12)
    return float(ym - b1 * xm), float(b1)


def main() -> None:
    P = pd.read_csv(x3.OUT / "per_item.csv", dtype={"id": str})
    P = P[(P.cond == "m") & P.measure.isin(["sib", "retrieval"])]
    ref = x3.reference_sample()
    sib = {str(it["id"]): it for it in x3.datasets()["sib"]}
    R, keep, native = lad.m4c_sample()
    m4c = {str(r["index"]): t for r, k, t in zip(R, keep, native) if k}
    rows = []
    for m in x3.MODELS:
        V = nc1.Vocab(AutoTokenizer.from_pretrained(REPOS[m]))
        sc = x3.make_proxies(V.tok, V, ref["words"])["r"]
        g = P[P.model == m].copy()
        xa, xo, xm_ = [], [], []
        for meas, i in zip(g.measure, g.id):
            if meas == "sib":
                it = sib[i]
                N = nc1.prompt_conditions(V, m, it["id"], "sib", it["forms"]["lossy"], it["forms"]["lower"])
                X = x3.prompt_variants(V, m, it["id"], "sib", it["forms"]["lossy"], PROX[m])
                a, o, c = N["a"][1], N["c"][1], X["m"][1]
            else:
                t = m4c[i]
                text = to_lossy(t)
                enc = V.tok(text, return_offsets_mapping=True, add_special_tokens=False)
                n_low = len(V.tok(lad.to_lower(t), add_special_tokens=False)["input_ids"])
                N = nc1.make_conditions(V, m, f"m4c|{i}", enc["input_ids"], enc["offset_mapping"], (0, len(text)), text, n_low)
                X = x3.sentence_variants(V, m, i, text, PROX[m])
                a, o, c = N["a"][1], N["c"][1], X["m"][1]
            ra = mean_ref(a, sc)
            xa.append(ra - mean_ref(c, sc))
            xo.append(ra - mean_ref(o, sc))
        g["x_m"], g["x_nco"] = xa, xo
        for meas, gg in g.groupby("measure"):
            for split, xcol, ycol in (("c (matched)", "x_m", "x3"), ("NC-O", "x_nco", "nc_c")):
                x = gg[xcol].to_numpy(float)
                y = gg["nc_a"].to_numpy(float) - gg[ycol].to_numpy(float)
                b0, b1 = ols(x, y)
                rng = np.random.default_rng(0)
                bs = np.array([ols(x[i], y[i]) for i in (rng.integers(0, len(x), len(x)) for _ in range(N_BOOT))])
                rows.append({"model": m, "measure": meas, "split": split, "n": len(x), "mean_x": x.mean(), "sd_x": x.std(),
                             "mean_y": y.mean(), "b0": b0, "b0_ci_low": np.percentile(bs[:, 0], 2.5), "b0_ci_high": np.percentile(bs[:, 0], 97.5),
                             "b1": b1, "b1_ci_low": np.percentile(bs[:, 1], 2.5), "b1_ci_high": np.percentile(bs[:, 1], 97.5),
                             "counted": m in (lad.COUNT_RETRIEVAL if meas == "retrieval" else lad.COUNT_ACC)})
        print(m, "done", flush=True)
    D = pd.DataFrame(rows)
    D.to_csv(x3.OUT / "regression.csv", index=False)
    write_json(x3.OUT / "regression_provenance.json", {"rows": len(D)}, {"status": "exploratory, no verdict", "defined": "RESULTS.md C2 2026-11-02",
                                                                        "bootstrap": N_BOOT, "seed": 0})
    print(D.round(4).to_string(index=False))


PROX: dict = {}

if __name__ == "__main__":
    from shattered.interp.load import MODELS as _R
    _ref = x3.reference_sample()
    for _m in x3.MODELS:
        _V = nc1.Vocab(AutoTokenizer.from_pretrained(_R[_m]))
        PROX[_m] = x3.make_proxies(_V.tok, _V, _ref["words"])
    main()
