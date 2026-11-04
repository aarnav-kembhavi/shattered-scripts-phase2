"""Resumable training loop for E5.

One epoch over the condition's pre-tokenized stream (same text for every condition). Context length in tokens is set
so each window covers ~target_ctx_bytes bytes; batch size in sequences is fixed, so every condition takes ~the same
number of steps over the same bytes. Checkpoints are written atomically every `ckpt_every` steps and on a time limit;
re-running the same config resumes from the last checkpoint.
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
import torch

from ..runlog import REPO, provenance
from .model import GPT, GPTConfig, train_flops_per_token

LN2 = math.log(2)


def context_tokens(target_ctx_bytes: int, bytes_per_token: float) -> int:
    return max(32, int(round(target_ctx_bytes / bytes_per_token / 8)) * 8)


def _amp(device: str):
    if device == "cuda" and torch.cuda.is_bf16_supported():
        return torch.bfloat16, None
    if device == "cuda":
        return torch.float16, torch.amp.GradScaler("cuda")
    return torch.bfloat16, None


@torch.no_grad()
def eval_bpb(model: GPT, stream: np.ndarray, n_bytes: int, ctx: int, device: str, batch: int = 32) -> float:
    """Bits per byte over a token stream: every token after the first is predicted exactly once (non-overlapping
    windows of ctx tokens, each condition's window spans ~the same number of bytes)."""
    model.eval()
    n = (len(stream) - 1) // ctx
    x_all = torch.from_numpy(stream[: n * ctx].astype(np.int64)).view(n, ctx)
    y_all = torch.from_numpy(stream[1: n * ctx + 1].astype(np.int64)).view(n, ctx)
    dtype, _ = _amp(device)
    total = 0.0
    for i in range(0, n, batch):
        x, y = x_all[i:i + batch].to(device), y_all[i:i + batch].to(device)
        with torch.autocast(device_type=device, dtype=dtype):
            _, loss, _ = model(x, y)
        total += float(loss)
    model.train()
    return total / LN2 / n_bytes


def _lr(step: int, total: int, peak: float, warmup_frac: float, min_frac: float) -> float:
    warm = max(1, int(total * warmup_frac))
    if step < warm:
        return peak * (step + 1) / warm
    prog = (step - warm) / max(1, total - warm)
    return peak * (min_frac + (1 - min_frac) * 0.5 * (1 + math.cos(math.pi * prog)))


def train_run(cfg: dict, meta: dict) -> dict:
    """cfg: vocab, seed, fraction, train_bytes, target_ctx_bytes, batch_seqs, lr, warmup_frac, min_lr_frac,
    weight_decay, eval_every, eval_bytes, ckpt_every, max_minutes, run_name, model{n_layer,d_model,n_head,emb_dim}."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    m = meta[str(cfg["vocab"])]
    out = REPO / "results" / "e05_pretrain" / cfg["run_name"]
    ck_dir = REPO / "checkpoints" / "e05" / cfg["run_name"]
    out.mkdir(parents=True, exist_ok=True)
    ck_dir.mkdir(parents=True, exist_ok=True)

    stream = np.load(REPO / m["train_stream"], mmap_mode="r")
    valid = np.load(REPO / m["valid_stream"], mmap_mode="r")
    ctx = cfg.get("ctx_tokens") or context_tokens(cfg["target_ctx_bytes"], m["bytes_per_token_train"])  # ctx_tokens: fixed context (X9a, equal to the Phase 1 vocabulary-1,024 runs)
    n_use = int(len(stream) * cfg.get("fraction", 1.0))
    n_seq = (n_use - 1) // ctx
    steps = n_seq // cfg["batch_seqs"]
    bytes_used = m["train_bytes"] * (steps * cfg["batch_seqs"] * ctx) / len(stream)  # ~ bytes actually seen

    # evaluation subset of the validation stream (~eval_bytes)
    ev_tokens = int(cfg["eval_bytes"] / m["bytes_per_token_valid"])
    ev_stream = np.ascontiguousarray(valid[:ev_tokens + 1])
    ev_bytes = m["bytes_per_token_valid"] * ev_tokens  # approximate bytes of the subset (exact for full eval)

    torch.manual_seed(cfg["seed"])
    mc = GPTConfig(vocab_size=m["vocab_with_eos"], max_ctx=ctx, **cfg["model"])
    model = GPT(mc).to(device)
    counts = model.param_counts()
    decay = [p for n, p in model.named_parameters() if p.dim() >= 2]
    opt = torch.optim.AdamW([{"params": decay, "weight_decay": cfg["weight_decay"]}], lr=cfg["lr"],
                            betas=(0.9, 0.95), fused=device == "cuda")
    dtype, scaler = _amp(device)

    step, log_path, ck = 0, out / "log.jsonl", ck_dir / "last.pt"
    if ck.exists():
        state = torch.load(ck, map_location=device, weights_only=False)
        model.load_state_dict(state["model"])
        opt.load_state_dict(state["opt"])
        if scaler and state.get("scaler"):
            scaler.load_state_dict(state["scaler"])
        torch.set_rng_state(state["rng_cpu"].cpu())
        step = state["step"]
        if log_path.exists():  # drop log lines written after the checkpoint
            lines = [ln for ln in log_path.read_text().splitlines() if json.loads(ln)["step"] <= step]
            log_path.write_text("".join(ln + "\n" for ln in lines))
        print(f"resumed {cfg['run_name']} at step {step}/{steps}")
        if step >= steps and (out / "final.json").exists():
            return {"status": "done", **json.loads((out / "final.json").read_text())}

    def save_ckpt() -> None:
        tmp = ck.with_suffix(".tmp")
        torch.save({"model": model.state_dict(), "opt": opt.state_dict(), "step": step,
                    "scaler": scaler.state_dict() if scaler else None, "rng_cpu": torch.get_rng_state()}, tmp)
        tmp.replace(ck)

    from safetensors.torch import save_file

    from . import evals
    from .data import load_tokenizer
    mp_pairs = evals.minimal_pairs() if cfg.get("mp_during_training", True) else None
    mp_tok = load_tokenizer(REPO / m["tokenizer"]) if mp_pairs else None
    snapshot_steps = {max(1, int(round(steps * f))): f for f in cfg.get("snapshot_fracs", [])}
    flops_tok = train_flops_per_token(mc, ctx, counts["non_embedding"])
    info = {"ctx_tokens": ctx, "steps": steps, "tokens_per_step": cfg["batch_seqs"] * ctx,
            "train_tokens": steps * cfg["batch_seqs"] * ctx, "train_bytes_seen": bytes_used,
            "bytes_per_token": m["bytes_per_token_train"], "params": counts,
            "flops_per_token": flops_tok, "train_flops": flops_tok * steps * cfg["batch_seqs"] * ctx,
            "device": torch.cuda.get_device_name(0) if device == "cuda" else "cpu", "amp_dtype": str(dtype)}
    (out / "run_info.json").write_text(json.dumps({"provenance": provenance(cfg), **info}, indent=2))

    t_start, t_train, start_step = time.time(), 0.0, step
    model.train()
    with log_path.open("a") as log:
        while step < steps:
            if cfg.get("max_minutes") and (time.time() - t_start) / 60 > cfg["max_minutes"]:
                save_ckpt()
                print(f"time limit reached at step {step}; checkpoint saved")
                return {"status": "paused", "step": step, **info}
            t0 = time.time()
            lo = step * cfg["batch_seqs"] * ctx
            chunk = torch.from_numpy(stream[lo: lo + cfg["batch_seqs"] * ctx + 1].astype(np.int64))
            x = chunk[:-1].view(cfg["batch_seqs"], ctx).to(device, non_blocking=True)
            y = chunk[1:].view(cfg["batch_seqs"], ctx).to(device, non_blocking=True)
            lr = _lr(step, steps, cfg["lr"], cfg["warmup_frac"], cfg["min_lr_frac"])
            for g in opt.param_groups:
                g["lr"] = lr
            opt.zero_grad(set_to_none=True)
            # gradient accumulation over micro-batches: same optimizer step, smaller activation memory
            mb = cfg.get("micro_batch_seqs") or cfg["batch_seqs"]
            loss_total = 0.0
            for j in range(0, cfg["batch_seqs"], mb):
                with torch.autocast(device_type=device, dtype=dtype):
                    _, loss_sum, _ = model(x[j:j + mb], y[j:j + mb])
                part = loss_sum / y.numel()
                (scaler.scale(part) if scaler else part).backward()
                loss_total += part.detach()
            loss = loss_total
            if scaler:
                scaler.unscale_(opt)
            gn = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            if scaler:
                scaler.step(opt)
                scaler.update()
            else:
                opt.step()
            if device == "cuda":
                torch.cuda.synchronize()
            t_train += time.time() - t0
            step += 1
            loss_val = loss.item()
            rec = {"step": step, "loss": loss_val, "train_bpb_approx": loss_val / LN2 / m["bytes_per_token_train"],
                   "lr": lr, "grad_norm": float(gn), "train_seconds": t_train}
            if step % cfg["eval_every"] == 0 or step == steps:
                rec["val_bpb_subset"] = eval_bpb(model, ev_stream, ev_bytes, ctx, device)
                if mp_pairs:
                    mp = evals.score_minimal_pairs(model, mp_tok, mp_pairs, device)
                    model.train()
                    rec["mp_acc"] = {k: v["acc_total_logprob"] for k, v in mp.items()}
                    rec["mp_acc_per_byte"] = {k: v["acc_per_byte"] for k, v in mp.items()}
            if step in snapshot_steps:
                save_file({k: v.contiguous() for k, v in model.state_dict().items()},
                          str(ck_dir / f"snapshot_step{step}.safetensors"))
            if step % 50 == 0 or "val_bpb_subset" in rec:
                log.write(json.dumps(rec) + "\n")
                log.flush()
            if step % cfg["ckpt_every"] == 0:
                save_ckpt()
    save_ckpt()

    final = {"val_bpb_full": eval_bpb(model, np.ascontiguousarray(valid), m["valid_bytes"], ctx, device),
             "train_seconds_this_session": t_train, "wall_seconds_this_session": time.time() - t_start,
             "seconds_per_step": t_train / max(1, steps - start_step)}
    save_file({k: v.contiguous() for k, v in model.state_dict().items()}, str(ck_dir / "final.safetensors"))
    if mp_pairs:
        final["minimal_pairs"] = evals.score_minimal_pairs(model, mp_tok, mp_pairs, device)
    (out / "final.json").write_text(json.dumps({"provenance": provenance(cfg), **info, **final,
                                                "model_config": mc.to_dict()}, indent=2))
    return {"status": "done", **info, **final}
