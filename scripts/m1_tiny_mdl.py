"""Step 3b: MDL (online code) word-identity probes and Feucht-style erasure probes on the 18 E5 tiny models.
Pre-registered in RESULTS.md (2026-10-15).

Words: the 300 most frequent space-preceded alphabetic validation words that are >= 3 tokens under vocab 768, up to
40 occurrences each (at most 2 per story, first 800 characters of each story), identical across all 18 models.

Usage: python scripts/m1_tiny_mdl.py [--pilot]
Outputs (results/m1_tiny_mdl/): words.json, run_v{V}_s{S}.json, per_run.csv, summary.csv, analysis.json
"""
import argparse
import json
import random
import re
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from scipy import stats

sys.path.insert(0, str(Path(__file__).parent))
from m1_tiny_probes import E5, SEEDS, VOCABS, load_model  # noqa: E402

from shattered.interp.probes import MDL_FRACS, PROBE, bootstrap_mdl_detok, erasure_curve, mdl_curve  # noqa: E402
from shattered.pretrain.data import load_tokenizer, read_stories  # noqa: E402
from shattered.runlog import REPO, results_dir, write_json  # noqa: E402

N_WORDS, MAX_OCC, MAX_PER_STORY, MAX_CHARS, MIN_TOKENS, SELECT_VOCAB = 300, 40, 2, 700, 3, 768
WORD_RE = re.compile(r"(?<= )[A-Za-z]{3,}(?![A-Za-z])")


def tok_path(v: int) -> Path:
    return REPO / "data" / "processed" / "e05" / f"tokenizer_{v}.json"


def build_occurrences() -> dict:
    stories = read_stories("valid")
    random.Random(0).shuffle(stories)
    stories = [s[:MAX_CHARS].rsplit(" ", 1)[0] if len(s) > MAX_CHARS else s for s in stories]
    freq = Counter(m.group() for s in stories for m in WORD_RE.finditer(s))
    sel = load_tokenizer(tok_path(SELECT_VOCAB))
    words = [w for w, n in freq.most_common() if n >= MAX_OCC and len(sel.encode(" " + w).ids) >= MIN_TOKENS][:N_WORDS]
    wid = {w: i for i, w in enumerate(words)}
    occ, count, used = [], Counter(), []
    for si, s in enumerate(stories):
        per, hit = Counter(), False
        for m in WORD_RE.finditer(s):
            w = m.group()
            if w in wid and count[w] < MAX_OCC and per[w] < MAX_PER_STORY:
                occ.append({"story": len(used), "start": m.start(), "end": m.end(), "word": w, "label": wid[w]})
                count[w] += 1
                per[w] += 1
                hit = True
        if hit:
            used.append(s)
        if all(count[w] >= MAX_OCC for w in words):
            break
    return {"words": words, "stories": used, "occurrences": occ, "min_occ": min(count.values()),
            "select_vocab": SELECT_VOCAB, "min_tokens": MIN_TOKENS}


@torch.no_grad()
def collect(model, tok, ctx, data, device):
    """states [n, L+1, d] at each word's last token, n_tokens [n], and token ids at offsets -1/-2 inside the word
    (-1 where the offset falls outside the word)."""
    by_story = {}
    for k, o in enumerate(data["occurrences"]):
        by_story.setdefault(o["story"], []).append(k)
    n = len(data["occurrences"])
    states, ntok, off = None, np.zeros(n, int), np.full((n, 2), -1)
    for si, ks in by_story.items():
        enc = tok.encode(data["stories"][si])
        ids, offs = enc.ids, enc.offsets
        assert len(ids) <= ctx, (len(ids), ctx)
        _, _, hidden = model(torch.tensor([ids], device=device), return_hidden=True)
        H = torch.stack([h[0] for h in hidden]).float().cpu().numpy()
        if states is None:
            states = np.zeros((n, H.shape[0], H.shape[2]), np.float32)
        for k in ks:
            o = data["occurrences"][k]
            toks = [i for i, (a, b) in enumerate(offs) if a >= o["start"] - 1 and b <= o["end"]]
            assert toks and offs[toks[-1]][1] == o["end"], o
            states[k] = H[:, toks[-1]]
            ntok[k] = len(toks)
            for j, d in enumerate((1, 2)):
                if len(toks) > d:
                    off[k, j] = ids[toks[-1 - d]]
    return states, ntok, off


def analyse(out) -> None:
    runs = [json.load(open(p)) for p in sorted(out.glob("run_v*_s*.json"))]
    t6 = pd.read_csv(E5 / "T6.csv").set_index("vocab")
    ref = t6.loc[4096, "val_bpb_mean"]
    rows = []
    for r in runs:
        e1, e2 = r["erasure"]["-1"], r["erasure"]["-2"]
        rows.append({"vocab": r["vocab"], "seed": r["seed"], "mdl_detok": r["mdl"]["detok_layer"],
                     "mdl_ci_low": r["mdl"]["ci_low"], "mdl_ci_high": r["mdl"]["ci_high"],
                     "compression_layer0": r["mdl"]["compression"][0], "compression_max": max(r["mdl"]["compression"]),
                     "erasure1_layer": e1["erasure_layer"] if e1 else None,
                     "erasure1_magnitude": e1["magnitude"] if e1 else None, "erasure1_peak": e1["peak_layer"] if e1 else None,
                     "erasure1_n_test": e1["n_test"] if e1 else 0,
                     "erasure2_layer": e2["erasure_layer"] if e2 else None,
                     "erasure2_magnitude": e2["magnitude"] if e2 else None,
                     "tokens_per_word_probed": r["tokens_per_word"], "tokens_per_word_valid": t6.loc[r["vocab"], "tokens_per_word"],
                     "bpb_gap_vs_4096": t6.loc[r["vocab"], "val_bpb_mean"] - ref})
    df = pd.DataFrame(rows).sort_values(["vocab", "seed"])
    df.to_csv(out / "per_run.csv", index=False)
    num = df.drop(columns="seed")
    agg = num.groupby("vocab").agg(["mean", "std"])
    agg.columns = [f"{a}_{b}" for a, b in agg.columns]
    agg = agg.reset_index()
    agg.to_csv(out / "summary.csv", index=False)
    payload = {"summary": agg.to_dict("records")}
    if len(agg) == len(VOCABS):
        x, y = agg.tokens_per_word_valid_mean, agg.mdl_detok_mean
        r1, r2 = stats.spearmanr(x, y), stats.spearmanr(y, agg.bpb_gap_vs_4096_mean)
        a = agg.set_index("vocab")
        gap = a.loc[256, "mdl_detok_mean"] - a.loc[4096, "mdl_detok_mean"]
        gap_ok = gap > max(a.loc[256, "mdl_detok_std"], a.loc[4096, "mdl_detok_std"])
        q1 = "confirmed" if r1.statistic >= 0.8 and gap_ok else "refuted" if not r1.statistic > 0 else "inconclusive"
        q2 = "confirmed" if r2.statistic >= 0.8 else "refuted" if not r2.statistic > 0 else "inconclusive"
        er = agg[agg.erasure1_n_test_mean >= 50]
        mags = er.erasure1_magnitude_mean
        if len(er) >= 2 and er.erasure1_layer_mean.notna().all():
            r3 = stats.spearmanr(er.tokens_per_word_valid_mean, er.erasure1_layer_mean).statistic
        else:
            r3 = None
        q3 = ("refuted" if (mags < 0.05).all() else
              "confirmed" if (mags >= 0.2).all() and r3 is not None and r3 >= 0.8 else "inconclusive")
        payload.update({"Q1b": {"spearman_tpw_vs_mdl_detok": r1.statistic, "p": r1.pvalue, "v256_minus_v4096": gap,
                                "gap_exceeds_seed_sd": bool(gap_ok), "verdict": q1},
                        "Q2b": {"spearman_mdl_detok_vs_bpb_gap": r2.statistic, "p": r2.pvalue, "verdict": q2},
                        "Q3b": {"conditions": er.vocab.tolist(), "magnitudes": mags.tolist(),
                                "spearman_tpw_vs_erasure_layer": r3, "verdict": q3}})
    write_json(out / "analysis.json", payload, {"probe": PROBE, "mdl_fracs": MDL_FRACS, "frac": 0.9})
    print(agg.round(3).to_string(index=False))
    print(json.dumps({k: v for k, v in payload.items() if k != "summary"}, indent=1, default=float))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    args = ap.parse_args()
    out = results_dir("m1_tiny_mdl")
    wpath = out / "words.json"
    if not wpath.exists():
        wpath.write_text(json.dumps(build_occurrences(), indent=0))
    data = json.load(open(wpath))
    labels = np.array([o["label"] for o in data["occurrences"]])
    print(f"{len(data['words'])} words, {len(labels)} occurrences, {len(data['stories'])} stories, "
          f"min occ/word {data['min_occ']}", flush=True)
    grid = [(256, 0), (4096, 0)] if args.pilot else [(v, s) for v in VOCABS for s in SEEDS]
    for v, s in grid:
        path = out / f"run_v{v}_s{s}.json"
        if path.exists():
            continue
        t0 = time.time()
        model, ctx = load_model(v, s, "cuda")
        states, ntok, off = collect(model, load_tokenizer(tok_path(v)), ctx, data, "cuda")
        t1 = time.time()
        mdl = mdl_curve(states, labels, seed=0)
        K = int(labels.max()) + 1
        er = {str(-d): erasure_curve(states, off[:, j], off[:, j] >= 0, labels, seed=0) for j, d in enumerate((1, 2))}
        res = {"vocab": v, "seed": s, "mdl": bootstrap_mdl_detok(mdl["costs"], K),
               "codelength_bits": mdl["codelength"].tolist(), "uniform_bits": mdl["uniform"], "erasure": er,
               "tokens_per_word": float(ntok.mean()), "frac_ge3_tokens": float((ntok >= 3).mean()),
               "seconds_forward": t1 - t0, "seconds_probes": time.time() - t1}
        write_json(path, res, {"checkpoint": f"checkpoints/e05/run_v{v}_s{s}/final.safetensors", "probe": PROBE})
        e1 = er["-1"]
        print(f"v{v} s{s}: MDL detok {res['mdl']['detok_layer']} [{res['mdl']['ci_low']}, {res['mdl']['ci_high']}] "
              f"compression {np.round(res['mdl']['compression'], 2).tolist()} | erasure-1 "
              f"{None if e1 is None else np.round(e1['acc'], 2).tolist()} | {t1 - t0:.0f}s fwd + "
              f"{time.time() - t1:.0f}s probes", flush=True)
        del model
        torch.cuda.empty_cache()
    if not args.pilot:
        analyse(out)


if __name__ == "__main__":
    main()
