"""Step 3: M1 word-identity probes on the 18 E5 tiny models (pre-registered in RESULTS.md, 2026-10-14).

Word set and occurrences are fixed once (validation stories, seed 0) and shared by all 18 models. For each model, one
forward pass per story; residual at each target word's last token at every layer; per-layer linear probes with a
random-label control; detokenization layer (90% of max) with a bootstrap CI over test occurrences.

Usage: python scripts/m1_tiny_probes.py [--pilot]    (--pilot: two models only, for timing)
Outputs (results/m1_tiny/): words.json, run_v{V}_s{S}.json, summary.csv, analysis.json
"""
import argparse
import json
import random
import re
import time
from collections import Counter

import numpy as np
import pandas as pd
import torch
from safetensors.torch import load_file
from scipy import stats

from shattered.interp.probes import PROBE, bootstrap_detok, layer_curve, split_by_word
from shattered.pretrain.data import load_tokenizer, read_stories
from shattered.pretrain.model import GPT, GPTConfig
from shattered.runlog import REPO, results_dir, write_json

VOCABS, SEEDS = [256, 384, 512, 768, 1024, 4096], [0, 1, 2]
N_WORDS, MAX_OCC, MAX_PER_STORY, MAX_CHARS, SCAN_STORIES = 300, 40, 2, 800, 6000
WORD_RE = re.compile(r"(?<= )[A-Za-z]{3,}(?![A-Za-z])")
CK = REPO / "checkpoints" / "e05"
E5 = REPO / "results" / "e05_pretrain"


def build_occurrences() -> dict:
    """Fixed word set (N_WORDS most frequent space-preceded alphabetic words, >= 3 letters, in the scanned validation
    stories) and up to MAX_OCC occurrences each (at most MAX_PER_STORY per story, inside the first MAX_CHARS chars)."""
    stories = read_stories("valid")
    random.Random(0).shuffle(stories)
    stories = [s[:MAX_CHARS].rsplit(" ", 1)[0] if len(s) > MAX_CHARS else s for s in stories[:SCAN_STORIES]]
    freq = Counter(m.group() for s in stories for m in WORD_RE.finditer(s))
    words = [w for w, _ in freq.most_common(N_WORDS)]
    wid = {w: i for i, w in enumerate(words)}
    occ, count, used = [], Counter(), set()
    for si, s in enumerate(stories):
        per = Counter()
        for m in WORD_RE.finditer(s):
            w = m.group()
            if w in wid and count[w] < MAX_OCC and per[w] < MAX_PER_STORY:
                occ.append({"story": si, "start": m.start(), "end": m.end(), "word": w, "label": wid[w]})
                count[w] += 1
                per[w] += 1
                used.add(si)
    keep = sorted(used)
    remap = {si: k for k, si in enumerate(keep)}
    for o in occ:
        o["story"] = remap[o["story"]]
    return {"words": words, "stories": [stories[i] for i in keep], "occurrences": occ,
            "min_occ": min(count.values()), "word_freq_in_scan": {w: freq[w] for w in words}}


def load_model(v: int, s: int, device: str):
    fin = json.load(open(E5 / f"run_v{v}_s{s}" / "final.json"))
    model = GPT(GPTConfig(**fin["model_config"]))
    model.load_state_dict(load_file(str(CK / f"run_v{v}_s{s}" / "final.safetensors")))
    return model.to(device).eval(), fin["ctx_tokens"]


@torch.no_grad()
def collect(model, tok, ctx: int, data: dict, device: str) -> tuple[np.ndarray, np.ndarray]:
    """Returns states [n_occ, L+1, d] (float32) and n_tokens [n_occ] for the word (with its leading space)."""
    by_story = {}
    for k, o in enumerate(data["occurrences"]):
        by_story.setdefault(o["story"], []).append(k)
    n = len(data["occurrences"])
    states, ntok = None, np.zeros(n, int)
    for si, ks in by_story.items():
        enc = tok.encode(data["stories"][si])
        ids, offs = enc.ids, enc.offsets
        assert len(ids) <= ctx, (len(ids), ctx)
        _, _, hidden = model(torch.tensor([ids], device=device), return_hidden=True)
        H = torch.stack([h[0] for h in hidden]).float().cpu().numpy()  # [L+1, T, d]
        if states is None:
            states = np.zeros((n, H.shape[0], H.shape[2]), np.float32)
        for k in ks:
            o = data["occurrences"][k]
            toks = [i for i, (a, b) in enumerate(offs) if a >= o["start"] - 1 and b <= o["end"]]
            last = [i for i in toks if offs[i][1] == o["end"]]
            assert last, (o, offs[toks[0]] if toks else None)
            states[k] = H[:, last[0]]
            ntok[k] = len(toks)
    return states, ntok


def analyse(out) -> None:
    runs = [json.load(open(p)) for p in sorted(out.glob("run_v*_s*.json"))]
    t6 = pd.read_csv(E5 / "T6.csv").set_index("vocab")
    ref = t6.loc[4096, "val_bpb_mean"]
    rows = []
    for r in runs:
        rows.append({"vocab": r["vocab"], "seed": r["seed"], "detok_layer": r["all"]["detok_layer"],
                     "detok_ci_low": r["all"]["ci_low"], "detok_ci_high": r["all"]["ci_high"],
                     "detok_layer_multitoken": r["multi_token"]["detok_layer"] if r["multi_token"] else None,
                     "acc_layer0": r["acc"][0], "acc_max": max(r["acc"]), "acc_control_max": max(r["acc_control"]),
                     "frac_multitoken_occ": r["frac_multitoken"], "tokens_per_word_probed": r["tokens_per_word"],
                     "tokens_per_word_valid": t6.loc[r["vocab"], "tokens_per_word"],
                     "bpb_gap_vs_4096": t6.loc[r["vocab"], "val_bpb_mean"] - ref})
    df = pd.DataFrame(rows).sort_values(["vocab", "seed"])
    df.to_csv(out / "per_run.csv", index=False)
    agg = df.groupby("vocab").agg(detok_mean=("detok_layer", "mean"), detok_sd=("detok_layer", "std"),
                                  detok_multi_mean=("detok_layer_multitoken", "mean"),
                                  detok_multi_sd=("detok_layer_multitoken", "std"),
                                  acc_layer0_mean=("acc_layer0", "mean"), acc_max_mean=("acc_max", "mean"),
                                  acc_control_max_mean=("acc_control_max", "mean"),
                                  frac_multitoken=("frac_multitoken_occ", "mean"),
                                  tokens_per_word_probed=("tokens_per_word_probed", "mean"),
                                  tokens_per_word_valid=("tokens_per_word_valid", "mean"),
                                  bpb_gap_vs_4096=("bpb_gap_vs_4096", "mean"), n_seeds=("seed", "size")).reset_index()
    agg.to_csv(out / "summary.csv", index=False)
    payload = {"summary": agg.to_dict("records")}
    if len(agg) == len(VOCABS):
        rho1 = stats.spearmanr(agg.tokens_per_word_valid, agg.detok_mean)
        rho2 = stats.spearmanr(agg.detok_mean, agg.bpb_gap_vs_4096)
        a256, a4k = agg.set_index("vocab").loc[256], agg.set_index("vocab").loc[4096]
        gap_ok = (a256.detok_mean - a4k.detok_mean) > max(a256.detok_sd, a4k.detok_sd)
        q1 = ("confirmed" if rho1.statistic >= 0.8 and gap_ok else
              "refuted" if not rho1.statistic > 0 else "inconclusive")
        q2 = "confirmed" if rho2.statistic >= 0.8 else "refuted" if not rho2.statistic > 0 else "inconclusive"
        payload.update({"Q1": {"spearman_tpw_vs_detok": rho1.statistic, "p": rho1.pvalue,
                               "v256_minus_v4096": a256.detok_mean - a4k.detok_mean, "gap_exceeds_seed_sd": bool(gap_ok),
                               "verdict": q1},
                        "Q2": {"spearman_detok_vs_bpb_gap": rho2.statistic, "p": rho2.pvalue, "verdict": q2},
                        "secondary_spearman_tpw_vs_acc_layer0": stats.spearmanr(agg.tokens_per_word_valid,
                                                                               agg.acc_layer0_mean).statistic})
    write_json(out / "analysis.json", payload, {"probe": PROBE, "frac": 0.9, "n_words": N_WORDS, "max_occ": MAX_OCC})
    print(agg.round(3).to_string(index=False))
    print({k: v for k, v in payload.items() if k != "summary"})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    args = ap.parse_args()
    out = results_dir("m1_tiny")
    wpath = out / "words.json"
    if not wpath.exists():
        wpath.write_text(json.dumps(build_occurrences(), indent=0))
    data = json.load(open(wpath))
    labels = np.array([o["label"] for o in data["occurrences"]])
    train = split_by_word(labels, 0.3, seed=0)
    print(f"{len(data['words'])} words, {len(labels)} occurrences, {len(data['stories'])} stories, "
          f"min occ/word {data['min_occ']}, test {int((~train).sum())}", flush=True)
    grid = [(256, 0), (4096, 0)] if args.pilot else [(v, s) for v in VOCABS for s in SEEDS]
    for v, s in grid:
        path = out / f"run_v{v}_s{s}.json"
        if path.exists():
            continue
        t0 = time.time()
        model, ctx = load_model(v, s, "cuda")
        tok = load_tokenizer(REPO / "data" / "processed" / "e05" / f"tokenizer_{v}.json")
        states, ntok = collect(model, tok, ctx, data, "cuda")
        t1 = time.time()
        cur = layer_curve(states, labels, train, seed=0)
        multi = ntok[~train] > 1
        res = {"vocab": v, "seed": s, "acc": cur["acc"].tolist(), "acc_control": cur["acc_control"].tolist(),
               "all": bootstrap_detok(cur["correct"]),
               "multi_token": bootstrap_detok(cur["correct"], subset=multi) if multi.sum() >= 50 else None,
               "n_multi_token_test": int(multi.sum()), "frac_multitoken": float((ntok > 1).mean()),
               "tokens_per_word": float(ntok.mean()), "seconds_forward": t1 - t0, "seconds_probe": time.time() - t1}
        write_json(path, res, {"checkpoint": f"checkpoints/e05/run_v{v}_s{s}/final.safetensors", "probe": PROBE})
        print(f"v{v} s{s}: detok {res['all']['detok_layer']} [{res['all']['ci_low']}, {res['all']['ci_high']}], "
              f"acc {np.round(cur['acc'], 3).tolist()}, ctrl max {max(res['acc_control']):.3f}, "
              f"{t1 - t0:.0f}s fwd + {time.time() - t1:.0f}s probes", flush=True)
        del model
        torch.cuda.empty_cache()
    if not args.pilot:
        analyse(out)


if __name__ == "__main__":
    main()
