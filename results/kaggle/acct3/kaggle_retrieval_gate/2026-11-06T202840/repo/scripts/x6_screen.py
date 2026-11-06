"""X6 screen (registered, Amendment 2; stage 1 = CPU and network, tokenizer files and Hub metadata only; stage 2 = laptop GPU forward-pass memory check for the shortlist).

Registered text: "Screen first (short jobs only): Llama 3.2 1B (base or instruct recorded with the reason; gated on HF, the token in .env is used) and a Hugging Face search for open decoder models of at most about
3B parameters with Indic pretraining or an Indic-extended tokenizer; names are not assumed: the screen lists parameters, license, tokenizer type, Kannada native and ITRANS tokens per word, and peak memory for a
forward pass with hidden states in bf16. Inclusion rule (at most two models): (1) fits 8 GB in bf16 for probing; (2) its Kannada native tokens per word, or its native/ITRANS ratio, differs by at least 20%
(relative) from every current model, or it is Indic-pretrained with an Indic-extended tokenizer; (3) it is counted only if its native SIB-200 CI lower bound is above 0.40."
Stage 1 here: candidates = Llama 3.2 1B (base) plus Hub search hits (text generation, searched terms below), at most 3.3B parameters by the Hub safetensors count; tokens per word on the 2,009 FLORES+ Kannada
sentences (native and ITRANS, as the Phase 1 gate E0); the four current accuracy models are the reference. "Indic-extended" is judged from the model card/name only as a flag for the reader (not automated).
Usage: python scripts/x6_screen.py stage1 | mem <repo ...>      Output: results/phase2/x6/screen.json (stage 1), mem.json (stage 2)
"""
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from m14_full import flores_forms  # noqa: E402

from shattered.runlog import REPO, results_dir, write_json  # noqa: E402

OUT = results_dir("phase2/x6")
CURRENT = {"qwen3-1.7b": "Qwen/Qwen3-1.7B", "qwen3.5-2b": "Qwen/Qwen3.5-2B", "sarvam-1": "sarvamai/sarvam-1", "gemma4-e2b": "google/gemma-4-E2B"}
SEARCH = ["kannada", "indic", "indian languages", "multilingual indic", "sarvam", "airavata", "navarasa", "gajendra", "krutrim", "llama-3.2-1b", "gemma-2b-it indic"]
MAX_PARAMS = 3.3e9


def tpw(tok, F) -> dict:
    out = {}
    for form in ("native", "itrans"):
        n = sum(len(x) for x in tok(F[form], add_special_tokens=False)["input_ids"])
        out[form] = n / sum(len(s.split()) for s in F[form])
    out["itrans_over_native"] = out["itrans"] / out["native"]
    return out


def stage1() -> None:
    from huggingface_hub import HfApi
    from transformers import AutoTokenizer
    api, tokn = HfApi(), os.environ.get("HF_TOKEN")
    F = flores_forms()
    cand = {"meta-llama/Llama-3.2-1B": "named in the registration (base chosen: no instruction tuning, as the other accuracy models)"}
    for q in SEARCH:
        try:
            for m in api.list_models(search=q, pipeline_tag="text-generation", sort="downloads", limit=40):
                cand.setdefault(m.id, f"search: {q}")
        except Exception as e:  # noqa: BLE001
            print("search failed", q, repr(e)[:100], flush=True)
    rows = {}
    for rid, why in {**{v: "current model" for v in CURRENT.values()}, **cand}.items():
        row = {"source": why}
        try:
            info = api.model_info(rid, token=tokn)
            row.update({"gated": info.gated, "license": (info.card_data or {}).get("license") if info.card_data else None, "params": getattr(getattr(info, "safetensors", None), "total", None),
                        "downloads": info.downloads})
        except Exception as e:  # noqa: BLE001
            row["metadata_error"] = repr(e)[:150]
            rows[rid] = row
            continue
        if row.get("params") and row["params"] > MAX_PARAMS and why != "current model":
            row["skipped"] = f"{row['params'] / 1e9:.1f}B parameters > 3.3B"
            rows[rid] = row
            continue
        try:
            tok = AutoTokenizer.from_pretrained(rid, token=tokn)
            row["tokenizer"] = type(tok).__name__
            row["vocab_size"] = len(tok)
            row["tpw"] = tpw(tok, F)
        except Exception as e:  # noqa: BLE001
            row["tokenizer_error"] = repr(e)[:150]
        rows[rid] = row
        print(rid, {k: row.get(k) for k in ("params", "license", "vocab_size")}, row.get("tpw"), flush=True)
    cur = {k: rows[v].get("tpw") for k, v in CURRENT.items() if rows.get(v, {}).get("tpw")}
    for rid, row in rows.items():
        if "tpw" not in row or row["source"] == "current model":
            continue
        rel = lambda a, b: abs(a - b) / b  # noqa: E731
        row["differs_20pct_from_every_current"] = bool(all(rel(row["tpw"]["native"], c["native"]) >= 0.2 or rel(row["tpw"]["itrans_over_native"], c["itrans_over_native"]) >= 0.2 for c in cur.values()))
        row["fits_8gb_bf16_by_params"] = bool(row.get("params") and row["params"] * 2 / 2**30 + 1.5 <= 8.0)
    short = [r for r, v in rows.items() if v.get("differs_20pct_from_every_current") and v.get("fits_8gb_bf16_by_params")]
    write_json(OUT / "screen.json", {"current_models": {k: {"repo": CURRENT[k], **(rows.get(CURRENT[k], {}).get("tpw") or {})} for k in CURRENT}, "candidates": rows, "rule2_and_rule1_by_params_shortlist_unordered": short,
                                     "note": "stage 1 only: rule (1) by parameter count (the measured forward-pass peak memory is stage 2); rule (3) needs a SIB-200 run; the registration allows at most two models and the choice among the shortlist is the operator's; the Indic-pretrained-with-extended-tokenizer alternative of rule (2) is a model-card reading, not automated"},
               {"registration": "RESULTS.md X6 (screen first)", "search_terms": SEARCH})
    print("shortlist (rules 1 and 2 by tokens per word):", short)


def mem(repos: list[str]) -> None:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tokn = os.environ.get("HF_TOKEN")
    F = flores_forms()
    res = {}
    for rid in repos:
        t0 = time.time()
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
        tok = AutoTokenizer.from_pretrained(rid, token=tokn)
        m = AutoModelForCausalLM.from_pretrained(rid, dtype=torch.bfloat16, device_map={"": "cuda"}, token=tokn).eval()
        ids = tok(F["native"][:16], return_tensors="pt", padding=True, truncation=True, max_length=256).to("cuda") if tok.pad_token else tok(F["native"][0], return_tensors="pt").to("cuda")
        with torch.no_grad():
            m(**ids, output_hidden_states=True)
        res[rid] = {"peak_gib": torch.cuda.max_memory_allocated() / 2**30, "seconds": time.time() - t0, "fits_8gb": bool(torch.cuda.max_memory_allocated() < 7.5 * 2**30)}
        print(rid, res[rid], flush=True)
        del m
        torch.cuda.empty_cache()
    write_json(OUT / "mem.json", res, {"registration": "RESULTS.md X6 screen, stage 2"})


if __name__ == "__main__":
    if sys.argv[1] == "stage1":
        stage1()
    else:
        mem(sys.argv[2:])
