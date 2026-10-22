"""NC1 and ladder post hoc analyses (post hoc descriptive, 2026-10-22, no verdict). CPU only; stored NC1 scores and
activations, tokenizers; no model is run.

1. Independent piece-frequency reference. The earlier proxy (scripts/nc1_piece_frequency.py) counted pieces on the
   evaluation texts themselves (partly circular). Here the reference excludes every evaluation item:
   - romanized Kannada: Dakshina `kn` romanized Wikipedia sentences (HF mirror
     Anvesh-Lankala/Copy_Dakshina_Google_research_dataset, data/raw/dakshina), as written; sentences whose native text
     equals, contains or is contained in any evaluation native text (>= 20 chars) are dropped;
   - English: whole articles from the local English Wikipedia shard (20231101.en, shard 0), shuffled with seed 0 and
     taken until their characters match the Dakshina part; articles containing any evaluation English text (>= 20
     chars) are skipped.
   Canonical tokenization per tokenizer; mean ln(count + 1) and share unseen for NC1 (a), (b), (c) per model x dataset.
2. Item-level decomposition (counted models). Item score: sentiment and SIB, gold-label log-prob margin (gold minus best
   other, calibrated as the primary rule: avg3 content-free with the raw fallback); retrieval, cosine to the correct
   English sentence minus the best distractor (unmapped, M4c test half, train-half centring, at the layer the NC1
   analysis selected for (a), the same layer for all conditions). For (b) and (c) pooled: OLS of (score - score in (a))
   on extra pieces vs canonical and the change in mean piece ln-frequency vs (a) (step 1 reference), item-clustered SEs.
3. Ladder piece familiarity: mean piece ln-frequency (step 1 reference) and tokens per word for ITRANS, lowercase,
   lossy, natural per model on M4c 496 and sentiment (natural: 198 clean items).

Usage: python scripts/nc1_posthoc.py
Outputs: results/nc1_posthoc/{reference.json, piece_frequency_independent.csv, decomposition.csv,
         ladder_piece_familiarity.csv}
"""
import sys
from collections import Counter

import numpy as np
import pandas as pd

from shattered.runlog import REPO, results_dir, write_json
from shattered.translit import to_lossy

sys.path.insert(0, str(REPO / "scripts"))
import e0b_familiarity as e0b  # noqa: E402
import l_ladder as lad  # noqa: E402
import nc1  # noqa: E402
from m4b_mapping import ACT  # noqa: E402
from m4c_natural_flores import SEED  # noqa: E402

DAKSHINA = REPO / "data/raw/dakshina/data/kn-00000-of-00001.parquet"
WIKI_EN = REPO / "data/raw/wikipedia_en/20231101.en/train-00000-of-00041.parquet"
MIN_MATCH = 20
OUT = results_dir("nc1_posthoc")


def eval_texts() -> tuple[set, set]:
    """All native and English evaluation texts (FLORES+ dev+devtest incl. SIB/M4c, sentiment, XNLI)."""
    from m14_full import flores_forms
    F = flores_forms()
    native, english = set(F["native"]), set(F["english"])
    for its in lad.e0b_items().values():
        for it in its:
            native |= set(it["forms"]["native"].values())
            english |= set(it["forms"]["english"].values())
    return {t.strip() for t in native}, {t.strip() for t in english}


def reference() -> tuple[list[str], dict]:
    native_ev, english_ev = eval_texts()
    long_nat = [t for t in native_ev if len(t) >= MIN_MATCH]
    D = pd.read_parquet(DAKSHINA)
    keep = []
    for nat in D.native.str.strip():
        hit = nat in native_ev or any(t in nat for t in long_nat) or (len(nat) >= MIN_MATCH and
                                                                         any(nat in t for t in long_nat))
        keep.append(not hit)
    D = D[np.array(keep)]
    rom = D.romanized.tolist()
    budget = sum(len(t) for t in rom)
    W = pd.read_parquet(WIKI_EN, columns=["text"])
    long_en = [t for t in english_ev if len(t) >= MIN_MATCH]
    en, n_chars, skipped = [], 0, 0
    for i in np.random.default_rng(0).permutation(len(W)):
        t = W.text.iat[i]
        if any(s in t for s in long_en):
            skipped += 1
            continue
        en.append(t)
        n_chars += len(t)
        if n_chars >= budget:
            break
    info = {"dakshina_sentences_total": 10000, "dakshina_dropped_overlap": int((~np.array(keep)).sum()),
            "dakshina_sentences": len(rom), "dakshina_chars": budget,
            "dakshina_words": sum(len(t.split()) for t in rom),
            "dakshina_uppercase_char_share": sum(c.isupper() for t in rom for c in t) / budget,
            "english_articles": len(en), "english_chars": n_chars, "english_articles_skipped_overlap": skipped,
            "english_source": "wikimedia/wikipedia 20231101.en shard 0 (local), seed-0 shuffle"}
    return rom + en, info


def ln_freq(freq: Counter, pieces) -> np.ndarray:
    return np.log(np.array([freq.get(p, 0) for p in pieces], dtype=float) + 1)


def span_pieces(cond) -> list:
    return [p for u in cond[1] for p in u["pieces"]]


def calibrated_margins(m: str, task: str, group_dir, cf: dict, use_raw: bool) -> dict:
    """{cond: {id: gold margin}} from the NC1 score files."""
    out = {}
    for c in nc1.CONDITIONS:
        g = pd.concat([pd.read_parquet(p) for p in nc1.SCORES.glob(f"{m}__nc_{c}__*.parquet")])
        g = g[g.task == task]
        off = 0 if use_raw else np.mean([cf[i][task] for i in e0b.CONTENT_FREE], axis=0)
        mg = {}
        for i, lab, lp in zip(g.id, g.label, g.logprobs):
            x = np.asarray(lp) - off
            mg[i] = x[lab] - np.delete(x, lab).max()
        out[c] = mg
    return out


def retrieval_margins(m: str, keep, idx, layer: int) -> dict:
    n = len(idx)
    order = np.random.default_rng(SEED).permutation(n)
    tr, te = np.sort(order[: n // 2]), np.sort(order[n // 2:])
    E = np.load(ACT / m / "english.npz")["flores_states"][idx][:, layer].astype(np.float64)
    Y = E[te] - E[tr].mean(0)
    Y /= np.linalg.norm(Y, axis=1, keepdims=True) + 1e-8
    out = {}
    for c in nc1.CONDITIONS:
        X = np.load(nc1.NC_ACT / m / f"{c}500.npz")["flores_states"][keep][:, layer].astype(np.float64)
        P = X[te] - X[tr].mean(0)
        P /= np.linalg.norm(P, axis=1, keepdims=True) + 1e-8
        S = P @ Y.T
        diag = np.diag(S).copy()
        np.fill_diagonal(S, -np.inf)
        out[c] = {"margin": dict(zip(idx[te].tolist(), diag - S.max(1))),
                  "hit": float((diag > S.max(1)).mean())}
    return out


def regress(rows: list[dict]) -> dict:
    import statsmodels.api as sm
    D = pd.DataFrame(rows)
    X = sm.add_constant(D[["extra_pieces", "d_ln_freq"]])
    fit = sm.OLS(D.y, X).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(D.item)[0]})
    ci = fit.conf_int()
    out = {"n_items": D.item.nunique(), "n_obs": len(D), "corr_extra_dfreq": D.extra_pieces.corr(D.d_ln_freq)}
    for k in ("extra_pieces", "d_ln_freq"):
        out.update({f"{k}_coef": fit.params[k], f"{k}_ci_low": ci.loc[k, 0], f"{k}_ci_high": ci.loc[k, 1],
                    f"{k}_p": fit.pvalues[k], f"{k}_sd": D[k].std()})
    return out


def main() -> None:
    import json
    from transformers import AutoTokenizer
    from shattered.interp.load import MODELS as REPOS
    from m14_full import flores_forms
    ref, info = reference()
    print(info, flush=True)
    R, keep, native = lad.m4c_sample()
    idx = np.array([r["index"] for r in R])[keep]
    tasks = nc1.score_items()
    itrans = flores_forms()["itrans"]
    m4c_forms = {"itrans": [], "lower": [], "lossy": [], "natural": []}
    for r, k, t in zip(R, keep, native):
        if k:
            m4c_forms["itrans"].append(itrans[r["index"]]); m4c_forms["lower"].append(lad.to_lower(t))
            m4c_forms["lossy"].append(to_lossy(t)); m4c_forms["natural"].append(r["natural"])
    sent = lad.e0b_items()["sentiment"]
    ladder_sets = {"m4c496": m4c_forms,
                   "sentiment": {f: [v for it in sent if not (f == "natural" and it.get("natural_defective"))
                                     for v in it["forms"][f].values()] for f in m4c_forms}}
    lad_tpw = pd.read_csv(REPO / "results/l_ladder/tokens_per_word.csv").set_index(["model", "dataset", "form"])
    nc_layers = pd.read_csv(REPO / "results/nc1/retrieval.csv").set_index(["model", "condition"])
    fb_rows = []
    for d in (lad.E0B_DIR, lad.E0C_DIR):
        B = pd.concat([pd.read_parquet(d / f"{m}__english.parquet") for m in lad.ACC_MODELS])
        cf = {m: json.load(open(d / f"cf_{m}.json")) for m in lad.ACC_MODELS}
        fb_rows.append(e0b.apply_calibration(B, cf)[1])
    fb = pd.concat(fb_rows).set_index(["model", "task"])

    freq_rows, lad_rows, dec_rows = [], [], []
    for m in lad.ACC_MODELS:
        tok = AutoTokenizer.from_pretrained(REPOS[m])
        V = nc1.Vocab(tok)
        freq = Counter(s for x in tok(ref, add_special_tokens=False)["input_ids"] for s in tok.convert_ids_to_tokens(x))
        info[f"reference_tokens_{m}"] = sum(freq.values())
        Q = nc1.m4c_conditions(V, m, R, native)
        sets = {"m4c496": [q[3] for q, k in zip(Q, keep) if k]}
        ids = {"m4c496": idx.tolist()}
        for t, its in tasks:
            sets[t] = [nc1.prompt_conditions(V, m, it["id"], t, it["forms"]["lossy"], it["forms"]["lower"])
                       for it in its]
            ids[t] = [it["id"] for it in its]
        for d, items in sets.items():
            for c in nc1.CONDITIONS:
                lf = ln_freq(freq, [p for it in items for p in span_pieces(it[c])])
                freq_rows.append({"model": m, "dataset": d, "condition": c, "n_items": len(items), "n_pieces": len(lf),
                                  "mean_ln_freq": lf.mean(), "median_ln_freq": float(np.median(lf)),
                                  "share_unseen": float((lf == 0).mean())})
        # step 3: ladder forms, canonical tokenization
        for d, forms in ladder_sets.items():
            for f, T in forms.items():
                toks = [tok.convert_ids_to_tokens(x) for x in tok(T, add_special_tokens=False)["input_ids"]]
                lf = ln_freq(freq, [p for x in toks for p in x])
                tpw = sum(map(len, toks)) / sum(len(x.split()) for x in T)
                assert np.isclose(tpw, lad_tpw.loc[(m, d, f), "tokens_per_word"]), (m, d, f)
                lad_rows.append({"model": m, "dataset": d, "form": f, "n_texts": len(T), "tokens_per_word": tpw,
                                 "mean_ln_freq": lf.mean(), "share_unseen": float((lf == 0).mean())})
        # step 2: item-level decomposition, counted models
        per_item = {d: {i: {c: (len(it[c][0]), ln_freq(freq, span_pieces(it[c])).mean()) for c in nc1.CONDITIONS}
                        for i, it in zip(ids[d], items)} for d, items in sets.items()}
        measures = {}
        if m in lad.COUNT_RETRIEVAL:
            layer = int(nc_layers.loc[(m, "a"), "unmapped_layer"])
            rm = retrieval_margins(m, keep, idx, layer)
            assert np.isclose(rm["a"]["hit"], nc_layers.loc[(m, "a"), "unmapped_test"]), m
            measures["retrieval"] = ("m4c496", {c: rm[c]["margin"] for c in nc1.CONDITIONS}, layer)
        if m in lad.COUNT_ACC:
            for t, d in (("sentiment", lad.E0B_DIR), ("sib", lad.E0C_DIR)):
                cf = json.load(open(d / f"cf_{m}.json"))
                measures[t] = (t, calibrated_margins(m, t, d, cf, bool(fb.loc[(m, t), "use_raw"])), None)
        for s, (d, mg, layer) in measures.items():
            rows = []
            for i in mg["a"]:
                ta, fa = per_item[d][i]["a"]
                for c in ("b", "c"):
                    tc, fc = per_item[d][i][c]
                    rows.append({"item": i, "cond": c, "y": mg[c][i] - mg["a"][i], "extra_pieces": tc - ta,
                                 "d_ln_freq": fc - fa})
            dec_rows.append({"model": m, "measure": s, "score": "cosine margin" if s == "retrieval"
                             else "calibrated gold log-prob margin", "layer": layer, **regress(rows)})
        print(m, "done", flush=True)

    pd.DataFrame(freq_rows).to_csv(OUT / "piece_frequency_independent.csv", index=False)
    pd.DataFrame(lad_rows).to_csv(OUT / "ladder_piece_familiarity.csv", index=False)
    pd.DataFrame(dec_rows).to_csv(OUT / "decomposition.csv", index=False)
    write_json(OUT / "reference.json", info, {"status": "post hoc descriptive, 2026-10-22, no verdict",
                                              "log": "natural log of (count + 1)", "min_overlap_chars": MIN_MATCH})


if __name__ == "__main__":
    main()
