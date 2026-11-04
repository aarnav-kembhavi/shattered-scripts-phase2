"""E0c: SIB-200 topic classification (7 classes) in English, native, ITRANS and lossy; P-a and P-b (pre-registered in
RESULTS.md, 2026-10-16).

Data: Davlan/sib200 (CC-BY-SA 4.0, revision pinned below), Kannada and English, train+dev+test = 1,004 sentences.
`index_id` is the 0-based position in FLORES dev (997) + devtest (1012); all 1,004 sentences equal our FLORES+ text at
that position after NFC (checked by `verify`), so the native, ITRANS and English inputs are taken from
m14_full.flores_forms() and are exactly the M4 inputs. Lossy = to_lossy(native), as in E0b.

Scoring: the E0b setup unchanged (scripts/e0b_familiarity.py): log-likelihood of the label words, BOS always,
primary calibration = mean of content-free "N/A", "", "[MASK]" with the raw fallback rule (> 5 points English drop).

P-b uses the SIB sentences in the M4b test half (seed-0 split of the 2,009 FLORES+ sentences). Per sentence: rank of
the true English sentence among the 1,005 test-half English sentences, (i) unmapped at M4b's train-half best
unmapped layer (primary) and (ii) after M4b's ridge map at its train-half best mapped layer and alpha (secondary).

Usage: python scripts/e0c_sib.py verify
       python scripts/e0c_sib.py score --models ... [--limit 30 --tag pilot]
       python scripts/e0c_sib.py analyse
Outputs (results/e0c_sib/): scores/ (cached per model x form), gate/{accuracy.csv, mcnemar.csv,
         mcnemar_exploratory.csv, calibration_fallback.csv, pb_cells.csv, pb_items.csv, verdicts.json}
"""
import argparse
import json
import sys
import unicodedata

import numpy as np
import pandas as pd

from shattered.runlog import REPO, results_dir, write_json
from shattered.translit import to_lossy

sys.path.insert(0, str(REPO / "scripts"))
import e0b_familiarity as e0b  # noqa: E402
from m4b_mapping import ACT, DualRidge  # noqa: E402

SIB_REPO, SIB_REV = "Davlan/sib200", "38977a667f6fc264d5c26ec57a01e16db040b358"
CATS = ["science/technology", "travel", "politics", "sports", "health", "entertainment", "geography"]
MODELS = ["qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
M4_MODELS = MODELS[:4]
FORMS = ["english", "native", "itrans", "lossy"]
CHANCE = 1 / 7
e0b.CHANCE["sib"] = CHANCE
CONST_MAX = 0.90  # P-b: cells whose most frequent predicted label exceeds this share are not counted


def sib(lang: str) -> pd.DataFrame:
    import os
    from huggingface_hub import hf_hub_download
    parts = []
    for s in ("train", "dev", "test"):
        p = hf_hub_download(SIB_REPO, f"data/{lang}/{s}.tsv", repo_type="dataset", revision=SIB_REV,
                            token=os.environ.get("HF_TOKEN"), local_dir=REPO / "data" / "raw" / "sib200")
        parts.append(pd.read_csv(p, sep="\t").assign(split=s))
    return pd.concat(parts, ignore_index=True).sort_values("index_id", ignore_index=True)


def do_verify() -> dict:
    from m14_full import flores_forms
    F = flores_forms()
    N = lambda s: unicodedata.normalize("NFC", s).strip()  # noqa: E731
    out = {}
    for lang, form in (("kan_Knda", "native"), ("eng_Latn", "english")):
        S = sib(lang)
        same = [N(t) == N(F[form][i]) for t, i in zip(S.text, S.index_id)]
        out[lang] = {"n": len(S), "unique_ids": int(S.index_id.nunique()), "text_equal_at_index": int(sum(same)),
                     "nfc_changed": int(sum(t != unicodedata.normalize("NFC", t) for t in S.text)),
                     "categories": S.category.value_counts().to_dict()}
    k, e = sib("kan_Knda"), sib("eng_Latn")
    out["labels_and_ids_equal_kn_en"] = bool((k.index_id.values == e.index_id.values).all()
                                             and (k.category.values == e.category.values).all())
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return out


def load_items(limit: int | None = None) -> dict:
    from m14_full import flores_forms
    F = flores_forms()
    S = sib("kan_Knda")
    items = [{"id": int(i), "label": CATS.index(c),
              "forms": {"english": {"text": F["english"][i]}, "native": {"text": F["native"][i]},
                        "itrans": {"text": F["itrans"][i]}, "lossy": {"text": to_lossy(F["native"][i])}}}
             for i, c in zip(S.index_id, S.category)]
    if limit:
        items = [items[j] for j in np.random.default_rng(0).choice(len(items), limit, replace=False)]
    return {"sib": items}


def do_score(models: list[str], limit: int | None, tag: str) -> None:
    root = results_dir("e0c_sib")
    score_dir = root / ("scores" if tag == "gate" else f"scores_{tag}")
    score_dir.mkdir(exist_ok=True)
    items = load_items(limit)
    for m in models:
        e0b.score_model(m, items, FORMS, score_dir)


def ranks(m: str, f: str, te: np.ndarray, tr: np.ndarray) -> dict:
    """Rank (1 = best) of the true English sentence among the test-half English sentences, unmapped and mapped,
    at M4b's train-half best layers; reproduces M4b's acc@1 exactly (asserted)."""
    z = np.load(REPO / "results" / "m4b_mapping" / "items.npz")
    v = json.load(open(REPO / "results" / "m4b_mapping" / "verdict.json"))
    curves = (v.get("result") or v)["curves"]
    lm, lu = z[f"{m}__{f}__best"]
    X = np.load(ACT / m / f"{f}.npz")
    E = np.load(ACT / m / "english.npz")["flores_states"]
    out = {"n_tokens": X["flores_n_tokens"][te]}
    for kind, layer in (("unmapped", lu), ("mapped", lm)):
        x, y = X["flores_states"][:, layer].astype(np.float64), E[:, layer].astype(np.float64)
        mx, my = x[tr].mean(0), y[tr].mean(0)
        P = x[te] - mx
        if kind == "mapped":
            P = DualRidge(x[tr] - mx, y[tr] - my).predict(P, curves[m][f]["alpha"][layer])
        Y = y[te] - my
        P = P / (np.linalg.norm(P, axis=1, keepdims=True) + 1e-8)
        Y = Y / (np.linalg.norm(Y, axis=1, keepdims=True) + 1e-8)
        S = P @ Y.T
        r = 1 + (S > np.diag(S)[:, None]).sum(1)
        assert np.array_equal(r == 1, z[f"{m}__{f}__{kind}"][layer]), (m, f, kind)
        out[kind], out[f"{kind}_layer"] = r, int(layer)
    return out


def logit_cell(d: pd.DataFrame, kind: str) -> dict:
    import statsmodels.api as sm
    zs = lambda x: (x - x.mean()) / x.std()  # noqa: E731
    X = sm.add_constant(pd.DataFrame({"neg_log_rank": zs(-np.log(d[f"rank_{kind}"])),
                                      "log_tokens": zs(np.log(d.n_tokens))}))
    try:
        fit = sm.Logit(d.correct.astype(float), X).fit(disp=0)
        b, p2 = float(fit.params["neg_log_rank"]), float(fit.pvalues["neg_log_rank"])
        p1 = p2 / 2 if b > 0 else 1 - p2 / 2
        return {"beta": b, "se": float(fit.bse["neg_log_rank"]), "p_one_sided": p1, "fit_ok": True}
    except Exception as e:  # perfect separation etc.; reported, not hidden
        return {"beta": np.nan, "se": np.nan, "p_one_sided": np.nan, "fit_ok": False, "error": str(e)[:200]}


def do_analyse() -> None:
    from statsmodels.stats.multitest import multipletests
    root = results_dir("e0c_sib")
    score_dir, out = root / "scores", root / "gate"
    out.mkdir(exist_ok=True)
    df = pd.concat([pd.read_parquet(score_dir / f"{m}__{f}.parquet") for m in MODELS for f in FORMS],
                   ignore_index=True)
    df, fallback = e0b.apply_calibration(df, {m: json.load(open(score_dir / f"cf_{m}.json")) for m in MODELS})
    fallback.to_csv(out / "calibration_fallback.csv", index=False)
    fert = pd.DataFrame([r for m in MODELS for f in FORMS
                         for r in json.load(open(score_dir / f"{m}__{f}.json"))["fertility"]])
    acc = e0b.accuracy_table(df).merge(fert[["model", "task", "form", "tokens_per_word"]],
                                       on=["model", "task", "form"])
    acc.to_csv(out / "accuracy.csv", index=False)
    en = acc[acc.form == "english"].set_index("model")
    informative = [m for m in MODELS if en.loc[m, "acc_cal"] >= CHANCE + 0.05]

    # P-a: native > ITRANS and native > lossy in every informative model (McNemar, Holm over these tests)
    mc = e0b.mcnemar_table(df[df.model.isin(informative)], [("native", "itrans"), ("native", "lossy")])
    mc.to_csv(out / "mcnemar.csv", index=False)
    ex = e0b.mcnemar_table(df, [("lossy", "itrans")])
    ex.to_csv(out / "mcnemar_exploratory.csv", index=False)
    rev = mc[mc.significant & (mc["diff"] < 0)]
    if (mc["diff"] > 0).all() and mc.significant.all():
        pa = "supported"
    elif len(rev) or not mc.significant.any():
        pa = "refuted"
    else:
        pa = "partly supported"

    # P-b: within form, sentences retrieved better against English are classified correctly more often
    n = 2009
    order = np.random.default_rng(0).permutation(n)
    tr, te = np.sort(order[: n // 2]), np.sort(order[n // 2:])
    pos = {int(i): j for j, i in enumerate(te)}
    rows, cells = [], []
    for m in M4_MODELS:
        for f in ("native", "itrans"):
            R = ranks(m, f, te, tr)
            g = df[(df.model == m) & (df.form == f) & df.id.isin(pos)].copy()
            j = g.id.map(pos).to_numpy()
            g["rank_unmapped"], g["rank_mapped"], g["n_tokens"] = R["unmapped"][j], R["mapped"][j], R["n_tokens"][j]
            g["correct"] = g.pred_cal == g.label
            rows.append(g[["model", "form", "id", "label", "pred_cal", "correct", "rank_unmapped", "rank_mapped",
                           "n_tokens"]])
            const = np.bincount(g.pred_cal).max() / len(g)
            counted = m in informative and const <= CONST_MAX
            for kind in ("unmapped", "mapped"):
                hit = g[f"rank_{kind}"] == 1
                cells.append({"model": m, "form": f, "retrieval": kind, "layer": R[f"{kind}_layer"], "n": len(g),
                              "counted": counted, "constant_label_rate": const, "accuracy": g.correct.mean(),
                              "retrieved_at1": hit.mean(), "n_retrieved": int(hit.sum()),
                              "acc_if_retrieved": g.correct[hit].mean() if hit.any() else np.nan,
                              "acc_if_not_retrieved": g.correct[~hit].mean() if (~hit).any() else np.nan,
                              "median_rank": float(np.median(g[f"rank_{kind}"])), **logit_cell(g, kind)})
    C = pd.DataFrame(cells)
    for kind in ("unmapped", "mapped"):
        k = (C.retrieval == kind) & C.counted & C.fit_ok
        C.loc[k, "p_holm"] = multipletests(C.loc[k, "p_one_sided"], method="holm")[1]
    C["significant"] = C.p_holm < 0.05
    C.to_csv(out / "pb_cells.csv", index=False)
    pd.concat(rows).to_csv(out / "pb_items.csv", index=False)
    pv = C[(C.retrieval == "unmapped") & C.counted]
    if len(pv) == 0:
        pb = "not testable (no counted cell)"
    elif (pv.beta > 0).all() and pv.significant.sum() >= len(pv) / 2:
        pb = "supported"
    elif (pv.beta <= 0).sum() >= len(pv) / 2:
        pb = "refuted"
    else:
        pb = "inconclusive"
    v = {"informative_models": informative, "P_a": pa, "P_a_tests": mc.to_dict("records"),
         "P_b_primary_unmapped": pb, "P_b_cells_counted": int(len(pv)),
         "P_b_secondary_mapped": C[(C.retrieval == "mapped") & C.counted][
             ["model", "form", "beta", "p_holm"]].to_dict("records")}
    cfg = {"dataset": f"{SIB_REPO}@{SIB_REV}", "n_items": int(df.id.nunique()), "models": MODELS, "forms": FORMS,
           "template": "e0_sib_v1", "verbalizers": "loglik.VERBALIZERS['sib']",
           "calibration": "mean of content-free N/A, '', [MASK]; raw fallback if English drops > 5 pts",
           "calibration_fallback_rows": fallback[fallback.use_raw].model.tolist(), "bos": "always prepended",
           "pb_split": "M4b seed-0 test half", "registered": "RESULTS.md 2026-10-16 (E0c)"}
    write_json(out / "verdicts.json", v, cfg)
    pd.set_option("display.width", 250)
    print(acc[["model", "form", "n", "acc_cal", "acc_cal_ci_low", "acc_cal_ci_high", "acc_raw",
               "constant_label_rate_cal", "tokens_per_word"]].round(3).to_string(index=False))
    print(mc.round(4).to_string(index=False))
    print(C.drop(columns=[c for c in C.columns if c == "error"]).round(3).to_string(index=False))
    print(json.dumps({k: v[k] for k in ("informative_models", "P_a", "P_b_primary_unmapped")}, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["verify", "score", "analyse"])
    ap.add_argument("--models", nargs="+", default=MODELS)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--tag", default="gate")
    a = ap.parse_args()
    if a.step == "verify":
        write_json(results_dir("e0c_sib") / "verify.json", do_verify(), {"dataset": f"{SIB_REPO}@{SIB_REV}"})
    elif a.step == "score":
        do_score(a.models, a.limit, a.tag)
    else:
        do_analyse()
