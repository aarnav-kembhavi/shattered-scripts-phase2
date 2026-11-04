"""X7-A (exploratory; added 2026-11-03, after the X7 bits-per-byte result was known): the Phase 1 MDL word-assembly probes on the 18 X7 factorized-embedding control runs.

Same word set and occurrences as Phase 1 (`results/m1_tiny_mdl/words.json`, the 300 words), same probe (`mdl_curve`, `bootstrap_mdl_detok`, fraction 0.9) as `scripts/m1_tiny_mdl.py`; only the
checkpoints differ: `checkpoints/e05/x7_v{V}_s{S}/final.safetensors` with the model configuration (including `emb_dim`) from `results/e05_pretrain/x7_v{V}_s{S}/final.json`, tokenizers
`data/processed/e05/tokenizer_{V}.json` (unchanged).

Decision rule (registered before the run; exploratory): SUPPORTED if, in each of the 3 seeds, the MDL detokenization layer at V = 256 exceeds the layer at V = 4096 by at least 1 (paired by seed);
REFUTED if it is not larger in any seed (difference <= 0 in all three); otherwise INCONCLUSIVE (also if a detokenization layer is undefined in any of the six runs involved).
Reported next to the Phase 1 layers. Usage: python scripts/x7a_mdl.py [--check]   (--check: load one run and run the forward pass on CPU, no probes; for tests)
Output: results/phase2/x7a/run_v{V}_s{S}.json, analysis.json
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
from safetensors.torch import load_file

sys.path.insert(0, str(Path(__file__).resolve().parent))
import m1_tiny_mdl as M  # noqa: E402

from shattered.interp.probes import PROBE, bootstrap_mdl_detok, erasure_curve, mdl_curve  # noqa: E402
from shattered.pretrain.data import load_tokenizer  # noqa: E402
from shattered.pretrain.model import GPT, GPTConfig  # noqa: E402
from shattered.runlog import REPO, results_dir, write_json  # noqa: E402

VOCABS, SEEDS = [256, 384, 512, 768, 1024, 4096], [0, 1, 2]
OUT = results_dir("phase2/x7a")


def load_x7(v: int, s: int, device: str):
    fin = json.load(open(REPO / "results" / "e05_pretrain" / f"x7_v{v}_s{s}" / "final.json"))
    model = GPT(GPTConfig(**fin["model_config"]))
    model.load_state_dict(load_file(str(REPO / "checkpoints" / "e05" / f"x7_v{v}_s{s}" / "final.safetensors")))
    return model.to(device).eval(), fin["ctx_tokens"], fin["model_config"].get("emb_dim")


def phase1_layer(v: int, s: int):
    d = json.load(open(REPO / "results" / "m1_tiny_mdl" / f"run_v{v}_s{s}.json"))
    return d["mdl"]["detok_layer"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    data = json.load(open(REPO / "results" / "m1_tiny_mdl" / "words.json"))
    labels = np.array([o["label"] for o in data["occurrences"]])
    K = int(labels.max()) + 1
    if a.check:
        model, ctx, emb = load_x7(256, 0, "cpu")
        states, ntok, off = M.collect(model, load_tokenizer(M.tok_path(256)), ctx, data, "cpu")
        print("check ok: emb_dim", emb, "states", states.shape, "mean tokens per word", round(float(ntok.mean()), 3))
        return
    for v in VOCABS:
        for s in SEEDS:
            path = OUT / f"run_v{v}_s{s}.json"
            if path.exists():
                continue
            t0 = time.time()
            model, ctx, emb = load_x7(v, s, "cuda")
            states, ntok, off = M.collect(model, load_tokenizer(M.tok_path(v)), ctx, data, "cuda")
            t1 = time.time()
            mdl = mdl_curve(states, labels, seed=0)
            er = {str(-d): erasure_curve(states, off[:, j], off[:, j] >= 0, labels, seed=0) for j, d in enumerate((1, 2))}
            res = {"vocab": v, "seed": s, "emb_dim": emb, "mdl": bootstrap_mdl_detok(mdl["costs"], K), "codelength_bits": mdl["codelength"].tolist(), "uniform_bits": mdl["uniform"],
                   "erasure": er, "tokens_per_word": float(ntok.mean()), "frac_ge3_tokens": float((ntok >= 3).mean()), "seconds_forward": t1 - t0, "seconds_probes": time.time() - t1,
                   "phase1_detok_layer_same_vocab_seed": phase1_layer(v, s)}
            write_json(path, res, {"checkpoint": f"checkpoints/e05/x7_v{v}_s{s}/final.safetensors", "probe": PROBE, "registration": "X7-A (exploratory)"})
            print(f"v{v} s{s}: detok {res['mdl']['detok_layer']} [{res['mdl']['ci_low']}, {res['mdl']['ci_high']}] (Phase 1 {res['phase1_detok_layer_same_vocab_seed']}) {time.time() - t0:.0f}s", flush=True)
            del model
            torch.cuda.empty_cache()
    runs = {(v, s): json.load(open(OUT / f"run_v{v}_s{s}.json")) for v in VOCABS for s in SEEDS}
    layer = {k: r["mdl"]["detok_layer"] for k, r in runs.items()}
    diffs = [None if layer[(256, s)] is None or layer[(4096, s)] is None else layer[(256, s)] - layer[(4096, s)] for s in SEEDS]
    if any(d is None for d in diffs):
        verdict = "inconclusive"
    elif all(d >= 1 for d in diffs):
        verdict = "supported"
    elif all(d <= 0 for d in diffs):
        verdict = "refuted"
    else:
        verdict = "inconclusive"
    by_v = {v: {"seeds": [layer[(v, s)] for s in SEEDS], "mean": float(np.mean([layer[(v, s)] for s in SEEDS if layer[(v, s)] is not None])),
                "phase1_seeds": [phase1_layer(v, s) for s in SEEDS]} for v in VOCABS}
    write_json(OUT / "analysis.json", {"detok_layer_by_vocab": by_v, "differences_256_minus_4096_by_seed": diffs, "verdict": verdict,
                                       "rule": "supported: each seed difference >= 1; refuted: no seed difference > 0; else inconclusive"}, {"registration": "X7-A (exploratory)"})
    print(json.dumps({"differences_256_minus_4096_by_seed": diffs, "verdict": verdict, "by_vocab": by_v}, indent=1))


if __name__ == "__main__":
    main()
