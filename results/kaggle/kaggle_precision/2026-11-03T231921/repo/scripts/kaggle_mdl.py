"""Kaggle MDL assembly-layer job (X13 after scoring; X12 contrast 2, descriptive): the Phase 1 word-assembly measures on the same 300 Kannada probe words
(`results/m14_full/words.json`, 30 occurrences each in Kannada Wikipedia sentences, shipped in the package), forms native and ITRANS, model sharded over both T4s in
float16 (no quantization; a model must have passed A1-P first, enforced by the caller). The forward pass, the MDL curve, the probe curve, the erasure probes and the
bootstrap are the Phase 1 functions (`scripts/m14_full.py: wiki_inputs, measures`), so the output files have the Phase 1 layout and the Phase 1 analysis applies
unchanged: out/<model>/<form>.json (curves, MDL detok layer with CI) and out/<model>/items_<form>.npz (per-occurrence costs for the word-clustered CIs).
Usage: python scripts/kaggle_mdl.py --out DIR --models qwen3-8b [--forms native itrans] [--limit-words N]
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from m14_full import measures, wiki_inputs  # noqa: E402
from shattered.interp.collect import collect  # noqa: E402
from shattered.interp.load import load, n_layers  # noqa: E402
from shattered.interp.probes import MDL_FRACS, PROBE  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--forms", nargs="+", default=["native", "itrans"])
    ap.add_argument("--limit-words", type=int, default=0, help="smoke test: keep only the first N probe words")
    a = ap.parse_args()
    out = Path(a.out)
    W = json.load(open(REPO / "results" / "m14_full" / "words.json", encoding="utf-8"))
    if a.limit_words:
        keep = set(W["kn_words"][:a.limit_words])
        pairs = [(s, [w for w in t if w in keep]) for s, t in zip(W["kn_sentences"], W["kn_targets"])]
        pairs = [(s, t) for s, t in pairs if t]
        W["kn_words"] = W["kn_words"][:a.limit_words]
        W["kn_sentences"], W["kn_targets"] = [p[0] for p in pairs], [p[1] for p in pairs]
    print(f"{len(W['kn_words'])} probe words, {len(W['kn_sentences'])} sentences", flush=True)
    for m in a.models:
        mdir = out / m
        mdir.mkdir(parents=True, exist_ok=True)
        todo = [f for f in a.forms if not (mdir / f"{f}.json").exists()]
        if not todo:
            continue
        t0 = time.time()
        dev = "auto" if torch.cuda.is_available() else "cpu"
        model, tok = load(m, dev, dtype=torch.float16 if dev == "auto" else torch.float32)
        L = n_layers(model)
        acts = {}
        for f in todo:
            c = collect(model, tok, wiki_inputs(W, f))
            acts[f] = {"word_states": c["word_states"], "word_meta": np.asarray([json.dumps(x, ensure_ascii=False) for x in c["word_meta"]])}
            print(m, f, "forward done", f"{time.time() - t0:.0f}s", flush=True)
        del model
        torch.cuda.empty_cache()
        for f in todo:
            res, items = measures(acts[f], f, W)
            res["n_layers"] = L
            res["dtype"] = "float16" if dev == "auto" else "float32"
            np.savez_compressed(mdir / f"items_{f}.npz", **items)
            (mdir / f"{f}.json").write_text(json.dumps({**res, "model": m, "form": f, "probe": PROBE, "mdl_fracs": MDL_FRACS, "frac": 0.9}, indent=1, default=str))
            print(f"{m}/{f}: MDL detok layer {res['mdl']['detok_layer']} [{res['mdl']['ci_low']}, {res['mdl']['ci_high']}] of {L}", flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()
