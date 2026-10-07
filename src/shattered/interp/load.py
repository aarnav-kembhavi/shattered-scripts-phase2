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


class CPULookup(torch.nn.Module):
    """Runs an embedding module on CPU and returns its output on `device` (kept out of .to(); not a submodule)."""

    def __init__(self, emb: torch.nn.Module, device: str) -> None:
        super().__init__()
        object.__setattr__(self, "emb", emb)  # not registered: model.to(...) must not move it
        self.out_device = device

    def forward(self, ids: torch.Tensor) -> torch.Tensor:
        return self.emb(ids.to("cpu")).to(self.out_device)


def _check_loaded(name: str, info: dict) -> None:
    """Refuse silently random-initialized weights (tied lm_head is allowed)."""
    missing = [k for k in info.get("missing_keys", []) if k != "lm_head.weight"]
    if missing:
        raise RuntimeError(f"{name}: {len(missing)} weights missing from checkpoint, e.g. {missing[:3]}")


def load(name: str, device: str | None = None, dtype=torch.bfloat16):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    repo = MODELS[name]
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    token = os.environ.get("HF_TOKEN")
    tok = AutoTokenizer.from_pretrained(repo, token=token)
    if name.startswith("gemma4"):
        from transformers import AutoConfig, Gemma4ForCausalLM
        cfg = AutoConfig.from_pretrained(repo, token=token).text_config
        # the checkpoint is multimodal: map its language-model weights onto the text-only class
        model, info = Gemma4ForCausalLM.from_pretrained(
            repo, config=cfg, dtype=dtype, device_map={"": "cpu"}, token=token, output_loading_info=True,
            key_mapping={r"^model\.language_model\.": "model."})
        _check_loaded(name, info)
        if device == "cuda":
            # accelerate's "cpu" placement streams weights to the GPU on every call; instead keep the per-layer
            # table on CPU, run the lookup there, and move only its (small) output to the GPU
            ple = model.model.embed_tokens_per_layer
            model.model.embed_tokens_per_layer = None
            model.to(device)
            model.model.embed_tokens_per_layer = CPULookup(ple, device)
    else:
        model, info = AutoModelForCausalLM.from_pretrained(repo, dtype=dtype, device_map={"": device}, token=token,
                                                           output_loading_info=True)
        _check_loaded(name, info)
    model.eval()
    return model, tok


def n_layers(model) -> int:
    cfg = model.config
    return getattr(cfg, "num_hidden_layers", None) or cfg.text_config.num_hidden_layers
