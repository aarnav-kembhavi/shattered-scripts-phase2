"""E5 controlled pretraining entry point.

  python scripts/e05_pretrain.py prepare            # tokenizers + token streams for all vocabs (idempotent)
  python scripts/e05_pretrain.py bench              # per-condition step-time micro-benchmark
  python scripts/e05_pretrain.py pilot              # pilot runs (2 conditions, 1 seed, 10% budget) + extrapolation
  python scripts/e05_pretrain.py train --vocab 4096 --seed 1 [--fraction 1.0]   # one run (resumable)

The full grid is never launched by this script automatically: it needs the pilot GATE.
"""
import argparse
import json
import time

import numpy as np
import torch
import yaml

from shattered.pretrain import data, evals
from shattered.pretrain.model import GPT, GPTConfig
from shattered.pretrain.train import _amp, context_tokens, train_run
from shattered.runlog import results_dir, write_json


def load_cfg(path: str) -> dict:
    return yaml.safe_load(open(path, encoding="utf-8"))


def get_meta(cfg: dict) -> dict:
    d = cfg["data"]
    return data.prepare(cfg["vocabs"], d["train_bytes"], d["tokenizer_train_bytes"], d["data_seed"])


def run_cfg(cfg: dict, vocab: int, seed: int, fraction: float, tag: str) -> dict:
    return {**cfg["train"], "vocab": vocab, "seed": seed, "fraction": fraction, "model": cfg["model"],
            "train_bytes": cfg["data"]["train_bytes"], "run_name": f"{tag}_v{vocab}_s{seed}"}


def bench(cfg: dict, meta: dict) -> dict:
    """Seconds per optimizer step for each vocab at its context length (random tokens, same shapes)."""
    device = "cuda"
    out = {}
    for v in cfg["vocabs"]:
        m = meta[str(v)]
        ctx = context_tokens(cfg["train"]["target_ctx_bytes"], m["bytes_per_token_train"])
        model = GPT(GPTConfig(vocab_size=m["vocab_with_eos"], max_ctx=ctx, **cfg["model"])).to(device)
        opt = torch.optim.AdamW(model.parameters(), lr=1e-4, fused=True)
        x = torch.randint(0, m["vocab_with_eos"], (cfg["train"]["batch_seqs"], ctx), device=device)
        mb = cfg["train"].get("micro_batch_seqs") or cfg["train"]["batch_seqs"]
        times = []
        for i in range(cfg["pilot"]["bench_steps"] + 3):
            torch.cuda.synchronize()
            t0 = time.time()
            for j in range(0, x.shape[0], mb):
                with torch.autocast("cuda", dtype=_amp("cuda")[0]):
                    _, loss, _ = model(x[j:j + mb], x[j:j + mb])
                (loss / x.numel()).backward()
            opt.step()
            opt.zero_grad(set_to_none=True)
            torch.cuda.synchronize()
            if i >= 3:
                times.append(time.time() - t0)
        out[str(v)] = {"ctx_tokens": ctx, "seconds_per_step": float(np.median(times)),
                       "peak_mem_gb": torch.cuda.max_memory_allocated() / 2**30}
        print(f"vocab {v:6d} ctx {ctx:5d}: {out[str(v)]['seconds_per_step'] * 1000:.0f} ms/step")
        del model, opt
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
    return out


def eval_minimal_pairs(cfg: dict, meta: dict, run_name: str, vocab: int) -> dict:
    """Score the final weights of a finished run on the templated minimal pairs."""
    from safetensors.torch import load_file
    from shattered.runlog import REPO
    m = meta[str(vocab)]
    ctx = context_tokens(cfg["train"]["target_ctx_bytes"], m["bytes_per_token_train"])
    model = GPT(GPTConfig(vocab_size=m["vocab_with_eos"], max_ctx=max(ctx, 128), **cfg["model"])).to("cuda")
    model.load_state_dict(load_file(str(REPO / "checkpoints" / "e05" / run_name / "final.safetensors")))
    tok = data.load_tokenizer(REPO / m["tokenizer"])
    return evals.score_minimal_pairs(model, tok, evals.minimal_pairs(), "cuda")


def full_steps(cfg: dict, meta: dict, v: int) -> int:
    m = meta[str(v)]
    ctx = context_tokens(cfg["train"]["target_ctx_bytes"], m["bytes_per_token_train"])
    return ((m["train_tokens"] - 1) // ctx) // cfg["train"]["batch_seqs"]


def pilot(cfg: dict, meta: dict) -> None:
    p = cfg["pilot"]
    out_dir = results_dir("e05_pretrain")
    bench_res = bench(cfg, meta)
    runs = {}
    for v in p["vocabs"]:
        t0 = time.time()
        res = train_run(run_cfg(cfg, v, p["seed"], p["fraction"], "pilot"), meta)
        res["wall_seconds_total"] = time.time() - t0
        res["minimal_pairs"] = eval_minimal_pairs(cfg, meta, f"pilot_v{v}_s{p['seed']}", v)
        runs[str(v)] = res
        print(f"pilot vocab {v}: {res['steps']} steps, val BPB {res.get('val_bpb_full'):.4f}, "
              f"wall {res['wall_seconds_total'] / 60:.1f} min")
    # Extrapolation: measured pilot wall time per step (includes evals) scaled by the bench ratio for other vocabs.
    n_seeds = len(cfg["seeds"])
    overhead = np.mean([runs[k]["wall_seconds_total"] / runs[k]["steps"] / bench_res[k]["seconds_per_step"]
                        for k in runs])
    grid = {}
    for v in cfg["vocabs"]:
        k = str(v)
        sps = (runs[k]["wall_seconds_total"] / runs[k]["steps"]) if k in runs else \
            bench_res[k]["seconds_per_step"] * overhead
        steps = full_steps(cfg, meta, v)
        grid[k] = {"full_steps": steps, "wall_seconds_per_step": sps, "hours_per_seed": steps * sps / 3600,
                   "hours_all_seeds": steps * sps * n_seeds / 3600,
                   "source": "pilot measurement" if k in runs else "bench x pilot overhead"}
    total_h = sum(g["hours_all_seeds"] for g in grid.values())
    payload = {"device": torch.cuda.get_device_name(0), "bench": bench_res, "pilot_runs": runs,
               "pilot_overhead_factor": overhead, "extrapolated_full_grid": grid,
               "extrapolated_full_grid_hours": total_h,
               "note": "Measured on the local GPU, not a Kaggle T4; T4 timing still has to be measured there."}
    write_json(out_dir / "pilot_report.json", payload, cfg)
    print(json.dumps({k: round(g["hours_all_seeds"], 2) for k, g in grid.items()}), f"total {total_h:.1f} h")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["prepare", "bench", "pilot", "train"])
    ap.add_argument("--config", default="configs/e05_pretrain.yaml")
    ap.add_argument("--vocab", type=int)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--fraction", type=float, default=1.0)
    ap.add_argument("--max-minutes", type=float)
    args = ap.parse_args()
    cfg = load_cfg(args.config)
    meta = get_meta(cfg)
    if args.cmd == "prepare":
        print(json.dumps({k: {f: v[f] for f in ("train_tokens", "bytes_per_token_train")} for k, v in meta.items()
                          if not k.startswith("_")}, indent=1))
        write_json(results_dir("e05_pretrain") / "data_meta.json", meta, cfg)
    elif args.cmd == "bench":
        write_json(results_dir("e05_pretrain") / "bench.json", bench(cfg, meta), cfg)
    elif args.cmd == "pilot":
        pilot(cfg, meta)
    else:
        rc = run_cfg(cfg, args.vocab, args.seed, args.fraction, "run")
        if args.max_minutes:
            rc["max_minutes"] = args.max_minutes
        print(train_run(rc, meta))


if __name__ == "__main__":
    main()
