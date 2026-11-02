"""Romanization ladder L1-L3 (pre-registered in RESULTS.md, 2026-10-22, before this script was written).

Forms: ITRANS -> lowercase lossless (E9 `universal|lower`) -> lossy (to_lossy) -> natural (Gemini).
  L1 casing:              lower - itrans
  L2 fragmentation:       lossy - lower
  L3 spelling familiarity: natural - lossy
Measures that count: unmapped M4 retrieval on the M4c sample (496 sentences, M4c split; counted Qwen3.5, Sarvam-1,
Gemma 4; effect if Holm-significant in >= 2 of 3, same sign) and accuracy on sentiment (E0b, 200; L3 on the 198 clean
natural items) and SIB-200 (E0c, 1,004; L3 secondary on the M4c-SIB overlap, 257) (counted Qwen3, Qwen3.5, Sarvam-1,
Gemma 4; >= 3 of 4). Qwen2.5 is reported, never counted. Holm within each measure across contrasts x counted models;
exact McNemar on per-item correctness; 95% paired bootstrap CIs. XNLI and the surface baseline are reported only.

Usage: python scripts/l_ladder.py pilot     (timing only: 30 sentences/items on Qwen2.5 and Gemma 4; nothing kept)
       python scripts/l_ladder.py forward   (GPU: lossy and lower sentence vectors, M4c 500 sentences, 4 models)
       python scripts/l_ladder.py score     (GPU: E0b + E0c lowercase, 5 models; SIB natural on the 257 overlap)
       python scripts/l_ladder.py analyse   (CPU)
Outputs: cache/activations/m14full/<model>/{lossy,lower}500.npz; scores in results/e0b_familiarity/scores and
         results/e0c_sib/scores (forms `lower`, `natural257`); results/l_ladder/{tokens_per_word.csv, retrieval.csv,
         accuracy.csv, contrasts.csv, verdict.json}
"""
import json
import sys
import time
from functools import lru_cache

import numpy as np
import pandas as pd
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.multitest import multipletests

from shattered.runlog import REPO, commit, results_dir, tmp_path, write_json
from shattered.translit import to_lossy

sys.path.insert(0, str(REPO / "scripts"))
import e0b_familiarity as e0b  # noqa: E402
import e0c_sib as e0c  # noqa: E402
from m4b_mapping import ACT, boot, layer_fit  # noqa: E402
from m4b_surface import status3  # noqa: E402
from m4c_natural_flores import SEED, rows  # noqa: E402

M4_MODELS = ["qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
ACC_MODELS = M4_MODELS + ["qwen3-1.7b"]
COUNT_RETRIEVAL = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
COUNT_ACC = ["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
CONTRASTS = [("L1", "lower", "itrans"), ("L2", "lossy", "lower"), ("L3", "natural", "lossy")]
CHECK = {"L1": "about equal", "L2": "differ", "L3": "about equal"}
TOL = 0.10  # tokens-per-word check: within 10% = about equal; lossy >= 10% below lower = differ
E0B_DIR = REPO / "results" / "e0b_familiarity" / "scores"
E0C_DIR = REPO / "results" / "e0c_sib" / "scores"
SCHEME = "universal|lower"


@lru_cache(maxsize=1)
def lower_scheme():
    from e09_eval import scheme_from
    best = json.load(open(REPO / "results" / "e09_romanize" / "best_schemes.json", encoding="utf-8"))["best"]
    return scheme_from(best[SCHEME]["assignment"])


def to_lower(text: str) -> str:
    return lower_scheme().encode(text)


def m4c_sample() -> tuple[list, np.ndarray, list]:
    """All 500 M4c rows (vectors are computed for all, as for natural500), the retained mask and native texts."""
    from m14_full import flores_forms
    R, kn = rows(), flores_forms()["native"]
    native = [kn[r["index"]] for r in R]
    return R, np.array([not r["defective"] for r in R]), native


def e0b_items() -> dict:
    items = e0b.load_items(["natural"])
    for its in items.values():
        for it in its:
            it["forms"]["lower"] = {k: to_lower(v) for k, v in it["forms"]["native"].items()}
    return items


def e0c_items(limit: int | None = None) -> dict:
    items = e0c.load_items(limit)
    for it in items["sib"]:
        it["forms"]["lower"] = {"text": to_lower(it["forms"]["native"]["text"])}
    return items


def sib257_items() -> dict:
    """SIB items in the retained M4c sample, with the M4c natural romanization as form `natural257`."""
    R, keep, _ = m4c_sample()
    nat = {r["index"]: r["natural"] for r, k in zip(R, keep) if k}
    its = [it for it in e0c.load_items()["sib"] if it["id"] in nat]
    for it in its:
        it["forms"]["natural257"] = {"text": nat[it["id"]]}
    return {"sib": its}


def forward_form(model, tok, texts: list[str], ids: list) -> dict:
    from shattered.interp.collect import Sentence, collect
    return collect(model, tok, [Sentence(str(i), t, []) for i, t in zip(ids, texts)])


def do_forward() -> None:
    import torch
    from shattered.interp.load import load
    R, _, native = m4c_sample()
    ids = [r["index"] for r in R]
    texts = {"lossy": [to_lossy(t) for t in native], "lower": [to_lower(t) for t in native]}
    for m in M4_MODELS:
        todo = [f for f in texts if not (ACT / m / f"{f}500.npz").exists()]
        if not todo:
            continue
        t0 = time.time()
        model, tok = load(m, "cuda")
        for f in todo:
            path = ACT / m / f"{f}500.npz"
            out = forward_form(model, tok, texts[f], ids)
            np.savez(tmp_path(path), flores_states=out["sent_states"], index=np.array(ids), n_tokens=out["n_tokens"])
            commit(tmp_path(path), path)
            print(f"{m}: {f}500 forward done ({time.time() - t0:.0f}s since load)", flush=True)
        del model
        torch.cuda.empty_cache()


def do_score() -> None:
    a, c, s = e0b_items(), e0c_items(), sib257_items()
    print(f"items: sentiment {len(a['sentiment'])}, xnli {len(a['xnli'])}, sib {len(c['sib'])}, "
          f"sib257 {len(s['sib'])}", flush=True)
    for m in ACC_MODELS:
        e0b.score_model(m, a, ["lower"], E0B_DIR)
        e0b.score_model(m, c, ["lower"], E0C_DIR)
        e0b.score_model(m, s, ["natural257"], E0C_DIR)


def do_pilot() -> None:
    """Timing only. Vectors and scores go to throwaway paths and no accuracy is printed."""
    import torch
    from shattered.interp.load import load
    R, _, native = m4c_sample()
    pilot_dir = results_dir("l_ladder") / "scores_pilot"
    pilot_dir.mkdir(exist_ok=True)
    items = e0c_items(limit=30)
    timing = {}
    for m in ("qwen2.5-1.5b", "gemma4-e2b"):
        t0 = time.time()
        model, tok = load(m, "cuda")
        t1 = time.time()
        forward_form(model, tok, [to_lower(t) for t in native[:30]], [r["index"] for r in R[:30]])
        timing[m] = {"load_s": t1 - t0, "forward_30_sentences_s": time.time() - t1}
        del model
        torch.cuda.empty_cache()
        t2 = time.time()
        e0b.score_model(m, items, ["lower"], pilot_dir)  # loads the model again; includes content-free inputs
        timing[m]["sib_30_items_incl_load_s"] = time.time() - t2
        print(m, {k: round(v) for k, v in timing[m].items()}, flush=True)
    write_json(results_dir("l_ladder") / "pilot_timing.json", timing, {"n": 30, "accuracies": "not computed"})


# ---------------------------------------------------------------- analysis

def tokens_per_word() -> pd.DataFrame:
    from transformers import AutoTokenizer
    from shattered.interp.load import MODELS as REPOS
    from m14_full import flores_forms
    R, keep, native = m4c_sample()
    itrans = flores_forms()["itrans"]  # the exact M4 ITRANS inputs
    m4c = {"itrans": [], "lower": [], "lossy": [], "natural": []}
    for r, k, t in zip(R, keep, native):
        if k:
            m4c["itrans"].append(itrans[r["index"]]); m4c["lower"].append(to_lower(t))
            m4c["lossy"].append(to_lossy(t)); m4c["natural"].append(r["natural"])
    a, c, s = e0b_items(), e0c_items(), sib257_items()

    def texts(its, form, skip_defective):
        return [v for it in its if not (skip_defective and it.get("natural_defective")) for v in it["forms"][form].values()]

    sets = {"m4c496": {f: m4c[f] for f in m4c}}
    for task in ("sentiment", "xnli"):
        sets[task] = {f: texts(a[task], f, f == "natural") for f in ("itrans", "lower", "lossy", "natural")}
    sets["sib"] = {f: texts(c["sib"], f, False) for f in ("itrans", "lower", "lossy")}
    sets["sib257"] = {"lossy": texts(s["sib"], "lossy", False), "natural": texts(s["sib"], "natural257", False)}
    out = []
    for m in ACC_MODELS:
        tok = AutoTokenizer.from_pretrained(REPOS[m])
        for d, forms in sets.items():
            for f, T in forms.items():
                n = sum(len(x) for x in tok(T, add_special_tokens=False)["input_ids"])
                out.append({"model": m, "dataset": d, "form": f, "n_texts": len(T),
                            "tokens_per_word": n / sum(len(x.split()) for x in T)})
    return pd.DataFrame(out)


def tpw_checks(T: pd.DataFrame) -> pd.DataFrame:
    out = []
    for (m, d), g in T.groupby(["model", "dataset"]):
        v = g.set_index("form").tokens_per_word
        for L, x, y in CONTRASTS:
            if x in v and y in v:
                ratio = v[x] / v[y]
                ok = abs(ratio - 1) <= TOL if CHECK[L] == "about equal" else ratio <= 1 - TOL
                out.append({"model": m, "dataset": d, "contrast": L, "a": x, "b": y, "tpw_a": v[x], "tpw_b": v[y],
                            "ratio": ratio, "check": CHECK[L], "check_passed": bool(ok)})
    return pd.DataFrame(out)


def paired(ca: np.ndarray, cb: np.ndarray) -> dict:
    ca, cb = ca.astype(bool), cb.astype(bool)
    table = [[int((ca & cb).sum()), int((ca & ~cb).sum())], [int((~ca & cb).sum()), int((~ca & ~cb).sum())]]
    return {"n": len(ca), "acc_a": ca.mean(), "acc_b": cb.mean(), "diff": ca.mean() - cb.mean(),
            "ci": boot(ca, cb), "a_only": table[0][1], "b_only": table[1][0],
            "p": mcnemar(table, exact=True).pvalue}


def retrieval_part() -> tuple[pd.DataFrame, list]:
    R, keep, _ = m4c_sample()
    idx = np.array([r["index"] for r in R])[keep]
    n = len(idx)
    order = np.random.default_rng(SEED).permutation(n)
    tr, te = np.sort(order[: n // 2]), np.sort(order[n // 2:])
    folds = np.array_split(np.random.default_rng(SEED + 2).permutation(tr), 5)
    res, con = [], []
    for m in M4_MODELS:
        E = np.load(ACT / m / "english.npz")["flores_states"][idx]
        forms = {"native": np.load(ACT / m / "native.npz")["flores_states"][idx],
                 "itrans": np.load(ACT / m / "itrans.npz")["flores_states"][idx]}
        for f in ("lower", "lossy", "natural"):
            z = np.load(ACT / m / f"{f}500.npz")
            assert np.array_equal(z["index"][keep], idx)
            forms[f] = z["flores_states"][keep]
        hits = {}
        for f, X in forms.items():
            fits = [layer_fit(X[:, l], E[:, l], tr, te, folds) for l in range(X.shape[1])]
            cv = np.array([r["cv"] for r in fits])
            lu, lm, lb = int(np.argmax([r["unmapped_train"] for r in fits])), int(cv.argmax()), 1 + int(cv[1:].argmax())
            hits[f] = fits[lu]["unmapped"]
            L0, Lb = fits[0]["mapped"], fits[lb]["mapped"]
            g = boot(Lb, L0)
            res.append({"model": m, "form": f, "n_test": len(te), "unmapped_test": hits[f].mean(),
                        "unmapped_test_ci": boot(hits[f]), "unmapped_layer": lu, "mapped_test": fits[lm]["mapped"].mean(),
                        "mapped_layer": lm, "surface_L0": L0.mean(), "surface_Lb": Lb.mean(), "surface_Lb_layer": lb,
                        "surface_gain": Lb.mean() - L0.mean(), "surface_gain_ci": g, "surface_status": status3(g)})
            print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in res[-1].items()}, flush=True)
        for L, a, b in CONTRASTS:
            con.append({"measure": "retrieval", "model": m, "contrast": L, "a": a, "b": b, **paired(hits[a], hits[b])})
    return pd.DataFrame(res), con


def accuracy_part() -> tuple[pd.DataFrame, list]:
    cf_b = {m: json.load(open(E0B_DIR / f"cf_{m}.json")) for m in ACC_MODELS}
    cf_c = {m: json.load(open(E0C_DIR / f"cf_{m}.json")) for m in ACC_MODELS}
    B = pd.concat([pd.read_parquet(E0B_DIR / f"{m}__{f}.parquet") for m in ACC_MODELS
                   for f in ("english", "itrans", "lower", "lossy", "natural")], ignore_index=True)
    C = pd.concat([pd.read_parquet(E0C_DIR / f"{m}__{f}.parquet") for m in ACC_MODELS
                   for f in ("english", "itrans", "lower", "lossy", "natural257")], ignore_index=True)
    B, _ = e0b.apply_calibration(B, cf_b)
    C, _ = e0b.apply_calibration(C, cf_c)
    acc = pd.concat([e0b.accuracy_table(B), e0b.accuracy_table(C)], ignore_index=True)
    con = []
    for df, task, measure, contrasts in (
            (B, "sentiment", "sentiment", CONTRASTS),
            (C, "sib", "sib", CONTRASTS[:2]),
            (C, "sib", "sib_L3_secondary", [("L3", "natural257", "lossy")]),
            (B, "xnli", "xnli_reported_only", CONTRASTS)):
        for m in ACC_MODELS:
            g = df[(df.model == m) & (df.task == task)]
            piv = g.pivot_table(index="id", columns="form", values="pred_cal")
            lab = g.drop_duplicates("id").set_index("id").label.loc[piv.index]
            corr = piv.eq(lab, axis=0)
            for L, a, b in contrasts:
                k = piv[a].notna() & piv[b].notna()
                con.append({"measure": measure, "model": m, "contrast": L, "a": a, "b": b,
                            **paired(corr[a][k].to_numpy(), corr[b][k].to_numpy())})
    return acc, con


def do_analyse() -> None:
    out = results_dir("l_ladder")
    T = tokens_per_word()
    T.to_csv(out / "tokens_per_word.csv", index=False)
    chk = tpw_checks(T)
    chk.to_csv(out / "tokens_per_word_checks.csv", index=False)
    print(chk.round(3).to_string(index=False), flush=True)
    S, con_r = retrieval_part()
    S.to_csv(out / "retrieval.csv", index=False)
    acc, con_a = accuracy_part()
    acc.to_csv(out / "accuracy.csv", index=False)
    K = pd.DataFrame(con_r + con_a)
    counted = {"retrieval": COUNT_RETRIEVAL, "sentiment": COUNT_ACC, "sib": COUNT_ACC, "sib_L3_secondary": COUNT_ACC}
    need = {"retrieval": 2, "sentiment": 3, "sib": 3, "sib_L3_secondary": 3}
    K["counted"] = [m in counted.get(s, []) for s, m in zip(K.measure, K.model)]
    K["p_holm"] = np.nan
    for s in counted:
        k = (K.measure == s) & K.counted
        K.loc[k, "p_holm"] = multipletests(K.loc[k, "p"], method="holm")[1]
    K["significant"] = K.p_holm < 0.05
    K["ci_excludes_0"] = [c[0] > 0 or c[1] < 0 for c in K.ci]
    K["ci_holm_disagree"] = K.counted & (K.significant != K.ci_excludes_0)
    K.to_csv(out / "contrasts.csv", index=False)
    dataset = {"retrieval": "m4c496", "sentiment": "sentiment", "sib": "sib", "sib_L3_secondary": "sib257"}
    verdicts = {}
    for s in counted:
        for L in ("L1", "L2", "L3"):
            g = K[(K.measure == s) & (K.contrast == L) & K.counted]
            if g.empty:
                continue
            pos, neg = int((g.significant & (g["diff"] > 0)).sum()), int((g.significant & (g["diff"] < 0)).sum())
            v = "effect, positive" if pos >= need[s] else "effect, negative" if neg >= need[s] else "no effect detected"
            c = chk[(chk.dataset == dataset[s]) & (chk.contrast == L) & chk.model.isin(counted[s])]
            verdicts[f"{L}|{s}"] = {"verdict": v, "n_significant_positive": pos, "n_significant_negative": neg,
                                    "needed": need[s], "n_counted": len(g),
                                    "tpw_check_failed_models": c[~c.check_passed].model.tolist(),
                                    "ci_holm_disagreements": g[g.ci_holm_disagree].model.tolist()}
    write_json(out / "verdict.json", verdicts,
               {"registered": "RESULTS.md 2026-10-22 (romanization ladder)", "lower_scheme": f"e09 {SCHEME}",
                "m4c_split_seed": SEED, "counted_retrieval": COUNT_RETRIEVAL, "counted_accuracy": COUNT_ACC,
                "tpw_tolerance": TOL})
    pd.set_option("display.width", 250)
    print(K.drop(columns=["ci"]).round(3).to_string(index=False))
    print(json.dumps(verdicts, indent=1))


if __name__ == "__main__":
    {"pilot": do_pilot, "forward": do_forward, "score": do_score, "analyse": do_analyse}[sys.argv[1]]()
