"""X9b Kaggle job (Amendment 2): QLoRA continued pretraining of Sarvam-1 (primary, seeds 0 and 1) and Qwen3.5-2B (secondary, seed 0) on one of three equal-token
streams (ITRANS Kannada, native Kannada, English), evaluated on SIB-200 (native, ITRANS, English damage check) and unmapped FLORES+ retrieval (native, ITRANS)
against the untrained model in the same environment and dtype.

Modes
  pilot  (X9b-D1: timing on the training machine, the Kaggle T4). For each model and condition: largest micro-batch of 512-token sequences that fits, then 50
         micro-steps (forward + backward; an optimizer step every 32 sequences) -> tokens/s and peak VRAM. B per model = floor(0.9 x slowest tokens/s x 10,800 s) rounded
         down to a multiple of the tokens per optimizer step (16,384). Also: exclusion-scan check of the consumed articles, the retained-order sha256 against the CPU
         report, a pool-size estimate, and a short end-to-end evaluation smoke (adapter merged into the unquantized fp16 base). Writes out/pilot_done.json.
  full   the registered runs, one (model, condition, seed) after another, each: re-scan of the consumed stream (overlap must be 0 or the run does not start),
         training with a checkpoint every 100 optimizer steps (resumable), merge into the fp16 base, evaluation. B is read from results/phase2/x9b/pilot_done.json.
  smoke  CPU, tiny model, no quantization: exercises the whole path (laptop only, for tests).

Recipe (registered, not tuned): 4-bit NF4 with double quantisation; compute dtype fp16 with loss scaling on the T4; LoRA r 16, alpha 32, dropout 0.05 on all attention
and MLP projections; embeddings and norms frozen; gradient checkpointing; 512-token sequences; paged 8-bit AdamW; lr 2e-4, cosine to 10 percent, warmup 3 percent,
weight decay 0. Not in the registered text and fixed here before any pilot output: 32 sequences (16,384 tokens) per optimizer step; documents joined with the EOS token,
no BOS; "50 steps" in the timing run are 50 micro-steps. The tokenizer is not changed by training; its sha256 is reported before and after.
Usage: python scripts/kaggle_x9b.py --out DIR --mode pilot|full|smoke [--runs sarvam-1:itrans:0 ...]
"""
import argparse
import gc
import hashlib
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "src"))
from shattered.data import x9b_streams as S  # noqa: E402
from shattered.interp.load import MODELS  # noqa: E402

SEQ, SEQ_PER_STEP = 512, 32
TOK_PER_STEP = SEQ * SEQ_PER_STEP  # 16,384
SECONDS_3H = 10_800
CONDS = ["itrans", "native", "english"]
PRIMARY, SECONDARY = "sarvam-1", "qwen3.5-2b"
REPORT = REPO / "results" / "phase2" / "x9b"
LORA = dict(r=16, lora_alpha=32, lora_dropout=0.05, target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"], task_type="CAUSAL_LM")
LR, WARMUP, FLOOR = 2e-4, 0.03, 0.10


# ---------------------------------------------------------------------------------------------------------------- streams
class Pool:
    """Retained articles of both languages in the registered seeded order, verified against the CPU report (sha256) and, if given, the removed-id list."""

    def __init__(self) -> None:
        rep = json.loads((REPORT / "streams_report.json").read_text(encoding="utf-8"))
        rem = json.loads((REPORT / "removed_ids.json").read_text(encoding="utf-8"))
        self.rep = rep
        self.rows = {"kn": S.load_wiki("kn"), "en": S.load_wiki("en")}
        self.text = {k: dict(v) for k, v in self.rows.items()}
        self.order = {"kn": S.retained_order(self.rows["kn"], set(rem["kn"])), "en": S.retained_order(self.rows["en"], set(rem["en"]))}
        self.hash = {"kn": S.order_hash(self.order["kn"]), "en": S.order_hash(self.order["en"])}
        want = {"kn": rep["streams"]["native_kannada"]["order_sha256"], "en": rep["streams"]["english"]["order_sha256"]}
        if self.hash != want or not rep.get("all_overlap_zero"):
            raise RuntimeError(f"X9b stream order differs from the CPU report or its overlap is not 0: {self.hash} vs {want}")

    def docs(self, cond: str):
        lang = "en" if cond == "english" else "kn"
        for aid in self.order[lang]:
            t = self.text[lang][aid]
            yield aid, (S.render_itrans(t) if cond == "itrans" else t)


def build_stream(pool: Pool, cond: str, tok, n_tokens: int) -> tuple[torch.Tensor, dict]:
    """The first n_tokens tokens (a multiple of 512) of the stream under `tok`: documents joined by EOS; returns [n/512, 512] int32 and the consumption stats."""
    eos = tok.eos_token_id
    buf: list[int] = []
    used, words = [], 0
    for aid, t in pool.docs(cond):
        ids = tok(t, add_special_tokens=False)["input_ids"] + ([eos] if eos is not None else [])
        buf += ids
        used.append(aid)
        words += len(t.split())
        if len(buf) >= n_tokens:
            break
    if len(buf) < n_tokens:
        raise RuntimeError(f"{cond}: the retained pool has only {len(buf)} tokens under this tokenizer, B = {n_tokens}")
    arr = torch.tensor(buf[:n_tokens], dtype=torch.int32).view(-1, SEQ)
    return arr, {"articles": len(used), "words": words, "tokens": n_tokens, "ids": used}


def scan_consumed(pool: Pool, cond: str, ids: list[str], sets: dict) -> int:
    """Re-scan of the consumed articles with the registered function (ITRANS stream: against the ITRANS renderings too). Returns the number of overlapping articles."""
    lang = "en" if cond == "english" else "kn"
    rows = [(a, pool.text[lang][a]) for a in ids]
    n = len(S.scan(rows, sets, itrans=False, workers=3))
    if cond == "itrans":
        from shattered.translit import to_itrans
        iset = {k + "_itrans": [" ".join(to_itrans(w) for w in s.split()) for s in v] for k, v in sets.items() if k.endswith("_kn")}
        n += len(S.scan(rows, {**iset, "flores_en": sets["flores_en"], "sib_en": sets["sib_en"]}, itrans=True, workers=3))
    return n


def tok_hash(tok) -> str:
    return hashlib.sha256(json.dumps(sorted(tok.get_vocab().items()), ensure_ascii=False).encode()).hexdigest()


# ---------------------------------------------------------------------------------------------------------------- model
def load_train_model(name: str, device: str, quant: bool):
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    repo, token = MODELS[name], os.environ.get("HF_TOKEN")
    tok = AutoTokenizer.from_pretrained(repo, token=token)
    kw = {}
    if quant:
        kw["quantization_config"] = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True,
                                                       bnb_4bit_compute_dtype=torch.float16)
    model = AutoModelForCausalLM.from_pretrained(repo, dtype=torch.float16 if quant else torch.float32, device_map={"": 0} if device == "cuda" else None, token=token, **kw)
    if quant:
        from peft import prepare_model_for_kbit_training
        model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)  # embeddings and norms stay frozen; casts them to fp32
    else:
        model.gradient_checkpointing_enable()
        model.enable_input_require_grads()
    from peft import LoraConfig, get_peft_model
    model = get_peft_model(model, LoraConfig(**LORA))
    return model, tok


def make_opt(model, total_steps: int, cuda: bool):
    params = [p for p in model.parameters() if p.requires_grad]
    if cuda:
        import bitsandbytes as bnb
        opt = bnb.optim.PagedAdamW8bit(params, lr=LR, weight_decay=0.0)
    else:
        opt = torch.optim.AdamW(params, lr=LR, weight_decay=0.0)
    w = max(1, int(round(WARMUP * total_steps)))

    def lam(step: int) -> float:
        if step < w:
            return (step + 1) / w
        p = (step - w) / max(1, total_steps - w)
        return FLOOR + (1 - FLOOR) * 0.5 * (1 + math.cos(math.pi * p))
    return opt, torch.optim.lr_scheduler.LambdaLR(opt, lam)


def micro_step(model, batch: torch.Tensor, device: str, scaler, accum: int) -> float:
    ids = batch.to(device).long()
    with torch.autocast(device_type="cuda", dtype=torch.float16, enabled=(device == "cuda")):
        loss = model(input_ids=ids, labels=ids).loss / accum
    (scaler.scale(loss) if scaler is not None else loss).backward()
    return float(loss) * accum


def free_gpu() -> None:
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def find_micro_batch(model, seqs: torch.Tensor, device: str, scaler) -> int:
    model.train()  # gradient checkpointing is applied only in train mode: the search must run in the mode of the timed loop (fix of 2026-11-03)
    for mb in ((16, 8, 4, 2, 1) if device == "cuda" else (2,)):
        try:
            if device == "cuda":
                torch.cuda.reset_peak_memory_stats()
            micro_step(model, seqs[:mb], device, scaler, 1)
            model.zero_grad(set_to_none=True)
            return mb
        except torch.OutOfMemoryError:
            model.zero_grad(set_to_none=True)
            free_gpu()
    raise RuntimeError("not even a micro-batch of 1 sequence fits")


# ---------------------------------------------------------------------------------------------------------------- pilot
def pilot_one(pool: Pool, name: str, cond: str, device: str, quant: bool, steps: int) -> dict:
    model, tok = load_train_model(name, device, quant)
    scaler = torch.amp.GradScaler("cuda") if device == "cuda" else None
    seqs, st = build_stream(pool, cond, tok, SEQ * 16 * (steps + 12))  # more than enough sequences for the largest micro-batch
    mb = find_micro_batch(model, seqs, device, scaler)
    accum = SEQ_PER_STEP // mb
    opt, sch = make_opt(model, 10_000, device == "cuda")
    if device == "cuda":
        torch.cuda.reset_peak_memory_stats()
    losses, t_start, n_tok = [], None, 0
    model.train()
    for i in range(steps):
        if i == 5:  # the first micro-steps (allocation, kernel autotune) are not timed
            if device == "cuda":
                torch.cuda.synchronize()
            t_start, n_tok = time.time(), 0
        losses.append(micro_step(model, seqs[i * mb:(i + 1) * mb], device, scaler, accum))
        n_tok += mb * SEQ
        if (i + 1) % accum == 0:
            if scaler is not None:
                scaler.step(opt)
                scaler.update()
            else:
                opt.step()
            sch.step()
            opt.zero_grad(set_to_none=True)
    if device == "cuda":
        torch.cuda.synchronize()
    secs = time.time() - t_start
    res = {"micro_batch": mb, "grad_accum": accum, "micro_steps": steps, "timed_micro_steps": steps - 5, "tokens_per_s": n_tok / secs, "seconds_timed": secs,
           "peak_vram_gib": (torch.cuda.max_memory_allocated() / 2**30 if device == "cuda" else None), "loss_first": losses[0], "loss_last": losses[-1],
           "finite_loss": bool(np.isfinite(losses).all()), "consumed_articles": st["articles"], "consumed_words": st["words"], "tokenizer_sha256": tok_hash(tok)}
    ids = st["ids"]
    del model, opt, sch
    free_gpu()
    return res, ids


def pool_estimate(pool: Pool, name: str, tok) -> dict:
    """Pool tokens under this tokenizer, estimated from the first 300 retained articles of each stream (tokens per word x retained words)."""
    out = {}
    for cond in CONDS:
        n_t = n_w = 0
        for k, (aid, t) in enumerate(pool.docs(cond)):
            n_t += len(tok(t, add_special_tokens=False)["input_ids"])
            n_w += len(t.split())
            if k >= 299:
                break
        rw = pool.rep["streams"]["english" if cond == "english" else "native_kannada"]["retained_words"]
        out[cond] = {"tokens_per_word": n_t / n_w, "retained_words": rw, "estimated_pool_tokens": int(n_t / n_w * rw)}
    return out


def eval_model(name: str, adapter: Path | None, tag: str, out: Path, device: str, limit: int | None, retrieval: bool) -> None:
    """SIB-200 (native, ITRANS, English) and, if asked, retrieval on the unquantized fp16 base (+ merged adapter), the Phase 1 scorers (scripts/x_score.py)."""
    import x_score as XS
    from shattered.interp.load import load
    dtype = torch.float16 if device == "cuda" else torch.float32
    model, tok = load(name, device, dtype=dtype)
    if adapter is not None:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, str(adapter)).merge_and_unload()
    mdir = out / tag
    mdir.mkdir(parents=True, exist_ok=True)
    XS.score_sib(model, tok, tag, XS.sib_items(limit), ["english", "native", "itrans"], mdir)
    if retrieval:
        XS.score_retrieval(model, tok, tag, mdir)
    del model
    free_gpu()


def run_pilot(out: Path, device: str, quant: bool, steps: int, models: list[str]) -> None:
    pool = Pool()
    sets = S.eval_sentences()
    res = {"seq_len": SEQ, "tokens_per_optimizer_step": TOK_PER_STEP, "steps": steps, "device": device, "quantized": quant, "models": {},
           "order_sha256": pool.hash, "exclusion_rescan_overlap": {}, "streams_report": {k: v["final_overlap"] for k, v in pool.rep["streams"].items()}}
    t0 = time.time()
    for name in models:
        r = {"conditions": {}}
        first_ids = {}
        for cond in CONDS:
            r["conditions"][cond], first_ids[cond] = pilot_one(pool, name, cond, device, quant, steps)
            res["exclusion_rescan_overlap"][f"{name}:{cond}"] = scan_consumed(pool, cond, first_ids[cond], sets)
            print(name, cond, {k: v for k, v in r["conditions"][cond].items() if k != "tokenizer_sha256"}, flush=True)
            (out / f"pilot_{name}_{cond}.json").write_text(json.dumps({"model": name, "condition": cond, **r["conditions"][cond]}, indent=1))  # a timeout loses at most one combination
        slow = min(c["tokens_per_s"] for c in r["conditions"].values())
        r["slowest_tokens_per_s"] = slow
        r["B"] = int(math.floor(0.9 * slow * SECONDS_3H / TOK_PER_STEP) * TOK_PER_STEP)
        r["optimizer_steps_at_B"] = r["B"] // TOK_PER_STEP
        from transformers import AutoTokenizer
        tok = AutoTokenizer.from_pretrained(MODELS[name], token=os.environ.get("HF_TOKEN"))
        r["pool_estimate"] = pool_estimate(pool, name, tok)
        r["pool_covers_B"] = {c: bool(v["estimated_pool_tokens"] >= r["B"]) for c, v in r["pool_estimate"].items()}
        r["tokenizer_sha256"] = tok_hash(tok)
        res["models"][name] = r
    res["all_overlap_zero"] = all(v == 0 for v in res["exclusion_rescan_overlap"].values()) and all(v == 0 for v in res["streams_report"].values())
    # end-to-end smoke of the evaluation path on the first model: base (20 items) and a stand-in adapter is not available without a trained one, so the base
    # path is exercised here and the merge path is exercised in the first full run's first checkpoint evaluation
    res["eval_smoke_ok"] = None
    res["seconds"] = time.time() - t0
    (out / "pilot_done.json").write_text(json.dumps(res, indent=1))  # the timings are written first: an evaluation fault must not lose them
    t1 = time.time()
    try:
        eval_model(models[0], None, f"{models[0]}__base_smoke", out, device, 20, retrieval=False)
        res["eval_smoke_ok"] = True
    except Exception as e:  # noqa: BLE001 - recorded, the driver refuses the full runs until it is fixed
        res["eval_smoke_ok"], res["eval_smoke_error"] = False, repr(e)[:400]
    res["eval_smoke_seconds"] = time.time() - t1
    res["seconds"] = time.time() - t0
    (out / "pilot_done.json").write_text(json.dumps(res, indent=1))
    print("pilot_done", json.dumps({m: {"B": v["B"], "slowest_tokens_per_s": round(v["slowest_tokens_per_s"], 1)} for m, v in res["models"].items()}), flush=True)


# ---------------------------------------------------------------------------------------------------------------- full
def run_full(out: Path, device: str, quant: bool, runs: list[str], steps_override: int | None, rehearsal: bool = False, pilot_path: Path | None = None,
             retrieval: bool = True) -> None:
    pd_ = json.loads((pilot_path or REPORT / "pilot_done.json").read_text(encoding="utf-8"))
    if not pd_.get("all_overlap_zero"):
        raise RuntimeError("pilot_done.json: overlap is not 0; no full run starts")
    pool = Pool()
    sets = S.eval_sentences()
    for spec in runs:
        name, cond, seed = spec.split(":")
        seed = int(seed)
        tag = f"{name}+{cond}+s{seed}" + ("__rehearsal" if rehearsal else "")
        rdir = out / tag
        rdir.mkdir(parents=True, exist_ok=True)
        if (rdir / "done.json").exists():
            continue
        B = steps_override * TOK_PER_STEP if steps_override else pd_["models"][name]["B"]
        t0 = time.time()
        torch.manual_seed(seed)
        np.random.seed(seed)
        model, tok = load_train_model(name, device, quant)
        sha0 = tok_hash(tok)
        seqs, st = build_stream(pool, cond, tok, B)
        overlap = scan_consumed(pool, cond, st["ids"], sets)
        if overlap != 0:
            raise RuntimeError(f"{tag}: the consumed stream overlaps the evaluation sentences in {overlap} articles; the run does not start")
        total = B // TOK_PER_STEP
        scaler = torch.amp.GradScaler("cuda") if device == "cuda" else None
        mb = pd_["models"][name]["conditions"][cond]["micro_batch"] if "conditions" in pd_["models"][name] else 1
        accum = SEQ_PER_STEP // mb
        opt, sch = make_opt(model, total, device == "cuda")
        step, ck, resumed_without_opt = 0, rdir / "ckpt.pt", False
        if ck.exists():
            c = torch.load(ck, map_location="cpu", weights_only=False)
            model.load_state_dict(c["adapter"], strict=False)
            if c.get("opt") is not None:
                opt.load_state_dict(c["opt"])
            else:
                resumed_without_opt = True  # checkpoints of 2026-11-05 on the laptop carry no optimizer state (see below); the resume resets the Adam moments and is flagged in done.json
            sch.load_state_dict(c["sch"])
            if scaler is not None and c.get("scaler"):
                scaler.load_state_dict(c["scaler"])
            step = c["step"]
            print(tag, "resumed at step", step, flush=True)
        model.train()
        log = []
        while step < total:
            for j in range(accum):
                a = (step * SEQ_PER_STEP + j * mb)
                loss = micro_step(model, seqs[a:a + mb], device, scaler, accum)
            if scaler is not None:
                scaler.unscale_(opt)
                scaler.step(opt)
                scaler.update()
            else:
                opt.step()
            sch.step()
            opt.zero_grad(set_to_none=True)
            step += 1
            if step % 20 == 0:
                log.append({"step": step, "loss": loss, "lr": sch.get_last_lr()[0], "t": time.time() - t0})
                print(tag, log[-1], flush=True)
            if step % 100 == 0 or step == total:
                tmp = ck.with_suffix(".tmp")  # atomic: a power loss during the write (laptop, 2026-11-05) must not leave an unreadable checkpoint
                # the optimizer state is NOT saved (laptop, 2026-11-05): torch.save of the paged 8-bit AdamW state took more than 20 minutes per checkpoint on the 8 GB card; a resume after an interruption would reset the Adam
                # moments and the run is then flagged in done.json (uninterrupted runs are unaffected: the checkpoint is never read)
                torch.save({"adapter": {k: v for k, v in model.state_dict().items() if "lora_" in k}, "opt": None, "sch": sch.state_dict(),
                            "scaler": scaler.state_dict() if scaler is not None else None, "step": step}, tmp)
                os.replace(tmp, ck)
        model.save_pretrained(str(rdir / "adapter"))
        sha1 = tok_hash(tok)
        train_s = time.time() - t0
        del model, opt, sch
        free_gpu()
        eval_model(name, rdir / "adapter", tag, out, device, 100 if rehearsal else None, retrieval=retrieval)
        (rdir / "done.json").write_text(json.dumps({"tag": tag, "model": name, "condition": cond, "seed": seed, "B": B, "optimizer_steps": total, "micro_batch": mb,
                                                    "articles": st["articles"], "words": st["words"], "tokens": st["tokens"], "overlap_articles": overlap,
                                                    "tokenizer_sha256_before": sha0, "tokenizer_sha256_after": sha1, "tokenizer_unchanged": sha0 == sha1, "resumed_without_optimizer_state": resumed_without_opt,
                                                    "train_seconds": train_s, "seconds": time.time() - t0, "loss_log": log}, indent=1))
        ck.unlink(missing_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--mode", required=True, choices=["pilot", "full", "smoke"])
    ap.add_argument("--runs", nargs="*", default=[])
    ap.add_argument("--base-eval", nargs="*", default=[], help="models whose untrained base is evaluated (full mode, once per model)")
    ap.add_argument("--smoke-model", default="qwen3-0.6b")
    ap.add_argument("--rehearsal", action="store_true", help="full path on 20 optimizer steps and 100 SIB items (checks train, checkpoint, merge, eval); discarded")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if a.mode == "smoke":  # CPU, tiny: whole path, two optimizer steps per run
        device, quant = "cpu", False
        if a.runs:
            raise SystemExit("smoke takes no --runs")
        run_pilot(out, device, quant, steps=8, models=[a.smoke_model])
        run_full(out, device, quant, [f"{a.smoke_model}:itrans:0"], 1, True, pilot_path=out / "pilot_done.json", retrieval=False)  # one optimizer step: checkpoint, adapter, merge, eval
        return
    assert torch.cuda.is_available(), "X9b runs on the Kaggle T4"
    if a.mode == "pilot":
        run_pilot(out, "cuda", True, 50, [PRIMARY, SECONDARY])
    else:
        for m in a.base_eval:
            if not (out / f"{m}__base" / "retrieval.json").exists():
                eval_model(m, None, f"{m}__base", out, "cuda", None, retrieval=True)
        refp = REPO / "results" / "phase2" / "x9b" / "base_reference.json"
        if refp.exists():  # a new environment must reproduce the untrained-base numbers (the A1-R values) before any training starts (decided 2026-11-04, account 2)
            ref = json.loads(refp.read_text(encoding="utf-8"))
            for m in a.base_eval:
                if m in ref:
                    got = json.loads((out / f"{m}__base" / "retrieval.json").read_text(encoding="utf-8"))["forms"]
                    for f in ("native", "itrans"):
                        if abs(got[f]["acc_unmapped"] - ref[m][f]["acc_unmapped"]) > ref["tolerance_acc"]:
                            raise RuntimeError(f"base evaluation does not reproduce the reference: {m} {f} {got[f]['acc_unmapped']:.4f} vs {ref[m][f]['acc_unmapped']:.4f}; no training started")
                    print(f"base evaluation check passed for {m}", flush=True)
        run_full(out, "cuda", True, a.runs, 20 if a.rehearsal else None, a.rehearsal)


if __name__ == "__main__":
    main()
