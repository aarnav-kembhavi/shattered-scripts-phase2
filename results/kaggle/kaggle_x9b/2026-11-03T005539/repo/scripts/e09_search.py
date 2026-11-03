"""E9 search: tokenizer-optimal reversible romanization schemes for Kannada (local tokenizers only).

Jobs = targets x variants x restarts. Variants: "free" (any candidate spelling) and "lower" (lowercase-only lossless
candidates). Restarts: deterministic init (ITRANS, or first lowercase spellings) plus random valid inits.

Usage: python scripts/e09_search.py [--words 50513] [--workers 6] [--restarts 4]
Outputs: results/e09_romanize/search_jobs.json (every job), best_schemes.json (best per target x variant)
"""
import argparse
import json
import os
import time
from multiprocessing import Pool

import numpy as np
import pandas as pd

from shattered.runlog import REPO, results_dir, write_json

TOKENIZERS = {
    "o200k": {"id": "o200k_base", "kind": "tiktoken"},
    "gemma4": {"id": "google/gemma-4-E2B-it", "kind": "hf"},
    "qwen3.5": {"id": "Qwen/Qwen3.5-9B", "kind": "hf"},
    "qwen3": {"id": "Qwen/Qwen3-8B", "kind": "hf"},
}
TARGETS = {"o200k": ["o200k"], "gemma4": ["gemma4"], "qwen3.5": ["qwen3.5"], "qwen3": ["qwen3"],
           "universal": ["o200k", "gemma4", "qwen3.5", "qwen3"]}


def _low_priority() -> None:
    """Pool initializer: run search workers below normal priority so concurrent GPU training keeps its CPU."""
    import psutil
    p = psutil.Process()
    p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if os.name == "nt" else 10)


def run_job(job: dict) -> dict:
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    from shattered.romanize_opt.search import (WordObjective, all_candidates, coordinate_descent,
                                               itrans_assignment, lowercase_init, random_valid_init)
    from shattered.tok.registry import load_counter
    from shattered.translit import ITRANS
    df = pd.read_parquet(REPO / "data" / "processed" / "kn_wiki_wordfreq.parquet").head(job["n_words"])
    counters = {n: load_counter(TOKENIZERS[n]) for n in TARGETS[job["target"]]}
    obj = WordObjective(df.word.tolist(), df["count"].to_numpy(), counters, ITRANS)
    cands = all_candidates(lowercase_only=job["variant"] == "lower")
    base = itrans_assignment()
    if len(counters) > 1:  # universal: normalize each tokenizer by its ITRANS total
        obj.norm = obj.total(obj.counts(obj.scheme(base)))[1]
    det_init = base if job["variant"] == "free" else {**base, **lowercase_init(cands)}
    inits = [det_init] if job["restart"] == 0 else \
        [{**base, **random_valid_init(cands, seed=1000 * job["restart"] + k, base=base)} for k in range(50)]
    t0 = time.time()
    init = None
    for cand_init in inits:  # an init must encode the whole word list (some tables are not separable)
        try:
            obj.counts(obj.scheme(cand_init))
            init = cand_init
            break
        except ValueError:
            continue
    if init is None:
        return {**job, "error": "no encodable init found"}
    res = coordinate_descent(obj, init, cands, seed=job["restart"], log=lambda *_: None)
    itr_val, itr_tok = obj.total(obj.counts(obj.scheme(base)))
    return {**job, "objective": res.objective, "per_tokenizer": res.per_tokenizer, "itrans_objective": itr_val,
            "itrans_per_tokenizer": itr_tok, "history": res.history, "evaluations": res.evaluations,
            "seconds": time.time() - t0,
            "assignment": [[t, n, s] for (t, n), s in sorted(res.assignment.items())]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--words", type=int, default=50513, help="top-N Wikipedia words (default: all with count>=30)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--restarts", type=int, default=4)
    args = ap.parse_args()
    jobs = [{"target": t, "variant": v, "restart": r, "n_words": args.words}
            for t in TARGETS for v in ("free", "lower") for r in range(args.restarts)]
    out = results_dir("e09_romanize")
    results = []
    with Pool(args.workers, initializer=_low_priority) as pool:
        for res in pool.imap_unordered(run_job, jobs):
            results.append(res)
            if "error" in res:
                print(f"{res['target']:9} {res['variant']:5} r{res['restart']}: {res['error']}", flush=True)
                continue
            print(f"{res['target']:9} {res['variant']:5} r{res['restart']}: {res['objective']:.6g} "
                  f"(ITRANS {res['itrans_objective']:.6g}) {res['seconds']:.0f}s", flush=True)
            (out / "search_jobs.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    best = {}
    for r in results:
        if "error" in r:
            continue
        k = f"{r['target']}|{r['variant']}"
        if k not in best or r["objective"] < best[k]["objective"]:
            best[k] = r
    write_json(out / "best_schemes.json", {"best": best}, {"n_words": args.words, "restarts": args.restarts,
                                                            "tokenizers": TOKENIZERS, "targets": TARGETS,
                                                            "corpus": "wikipedia kn 20231101 word list"})
    for k, r in best.items():
        print(k, round(r["objective"] / r["itrans_objective"], 4) if r["target"] != "universal" else r["objective"])


if __name__ == "__main__":
    main()
