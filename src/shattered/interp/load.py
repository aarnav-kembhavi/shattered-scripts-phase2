"""Load the M-experiment models in bf16 on one 8 GB GPU (or CPU).

Gemma 4 E2B is loaded text-only (Gemma4ForCausalLM, no vision/audio towers) with its per-layer embedding table
(`model.embed_tokens_per_layer`, 2.35B params, a pure lookup) kept on CPU; everything else goes on the GPU (~4.6 GB).
"""
from __future__ import annotations

import os

import torch
from dotenv import load_dotenv

from ..runlog import REPO

load_dotenv(REPO / ".env")

MODELS = {
    "qwen3-1.7b": "Qwen/Qwen3-1.7B",
    "qwen2.5-1.5b": "Qwen/Qwen2.5-1.5B-Instruct",
    "qwen3.5-2b": "Qwen/Qwen3.5-2B",
    "gemma4-e2b": "google/gemma-4-E2B-it",
    "sarvam-1": "sarvamai/sarvam-1",
    "qwen3-0.6b": "Qwen/Qwen3-0.6B",  # tests only
}


def load(name: str, device: str | None = None, dtype=torch.bfloat16):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    repo = MODELS[name]
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    token = os.environ.get("HF_TOKEN")
    tok = AutoTokenizer.from_pretrained(repo, token=token)
    if name.startswith("gemma4"):
        from transformers import AutoConfig, Gemma4ForCausalLM
        cfg = AutoConfig.from_pretrained(repo, token=token).text_config
        dmap = {"": device, "model.embed_tokens_per_layer": "cpu"} if device == "cuda" else {"": "cpu"}
        model = Gemma4ForCausalLM.from_pretrained(repo, config=cfg, dtype=dtype, device_map=dmap, token=token)
    else:
        model = AutoModelForCausalLM.from_pretrained(repo, dtype=dtype, device_map={"": device}, token=token)
    model.eval()
    return model, tok


def n_layers(model) -> int:
    cfg = model.config
    return getattr(cfg, "num_hidden_layers", None) or cfg.text_config.num_hidden_layers
