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
    "llama-3.2-1b": "NousResearch/Llama-3.2-1B",  # X6 (deviation X6-D1: mirror of the gated meta-llama/Llama-3.2-1B)
    "oro-1.7b": "ashtok897/oroZ-1.7B-Indic-v1",  # X6
    "sarvam-1": "sarvamai/sarvam-1",
    "qwen3-0.6b": "Qwen/Qwen3-0.6B",  # tests only
    # Phase 2 Kaggle models (X12, X13; loaded with device="auto" over 2 x T4)
    "qwen3-8b": "Qwen/Qwen3-8B",
    "ambari-7b-base": "Cognitive-Lab/Ambari-7B-base-v0.1",
    "ambari-7b-instruct-v0.1": "Cognitive-Lab/Ambari-7B-Instruct-v0.1",
    "ambari-7b-instruct-v0.2": "Cognitive-Lab/Ambari-7B-Instruct-v0.2",
    "llama-2-7b": "meta-llama/Llama-2-7b-hf",
    "llama-3.1-8b": "meta-llama/Llama-3.1-8B",
}


PICKLE_ONLY = {"ambari-7b-instruct-v0.2"}


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


PLE_KEY = "model.embed_tokens_per_layer.weight"


def _load_gemma4_text(repo: str, device: str, dtype, token):
    """Low-memory, text-only Gemma 4 load.

    The checkpoint is multimodal (keys under `model.language_model.`). The text-only model is built on the meta device
    and only language-model tensors are streamed from the safetensors files, one at a time, straight to their final
    device; vision/audio tensors are never read. The per-layer embedding table stays on CPU and runs there (CPULookup);
    everything else goes to `device`. Peak CPU RAM is about the per-layer table (~4.7 GB) plus one tensor.
    """
    import json

    from accelerate import init_empty_weights
    from accelerate.utils import set_module_tensor_to_device
    from huggingface_hub import hf_hub_download, snapshot_download
    from safetensors import safe_open
    from transformers import AutoConfig, Gemma4ForCausalLM

    cfg = AutoConfig.from_pretrained(repo, token=token).text_config
    with init_empty_weights():
        model = Gemma4ForCausalLM(cfg)
    expected = set(model.state_dict().keys())
    local = snapshot_download(repo, token=token, allow_patterns=["*.json", "*.safetensors"])
    try:
        files = sorted(set(json.load(open(hf_hub_download(repo, "model.safetensors.index.json", token=token)))
                           ["weight_map"].values()))
    except Exception:  # noqa: BLE001 - single-file checkpoint
        files = ["model.safetensors"]
    loaded = set()
    for f in files:
        with safe_open(f"{local}/{f}", framework="pt", device="cpu") as st:
            for k in st.keys():
                if not k.startswith("model.language_model."):
                    continue  # vision/audio towers and their projections
                tk = "model." + k[len("model.language_model."):]
                if tk not in expected:
                    continue
                dev = "cpu" if (tk == PLE_KEY or device != "cuda") else device
                set_module_tensor_to_device(model, tk, dev, value=st.get_tensor(k), dtype=dtype)
                loaded.add(tk)
    if "lm_head.weight" in expected and "lm_head.weight" not in loaded:  # tied to the input embedding
        model.tie_weights()
        loaded.add("lm_head.weight")
    missing = expected - loaded
    if missing:
        raise RuntimeError(f"gemma4: {len(missing)} weights not found in checkpoint, e.g. {sorted(missing)[:3]}")
    # non-persistent buffers (e.g. rotary inv_freq) are still on meta: rebuild them on the target device
    for mod_name, mod in model.named_modules():
        for b_name, buf in list(mod.named_buffers(recurse=False)):
            if buf.is_meta:
                raise RuntimeError(f"gemma4: buffer {mod_name}.{b_name} left on meta device")
    if device == "cuda":
        # swap in the CPU-side lookup first (unregistered, so .to() skips it), then move buffers to the GPU
        ple = model.model.embed_tokens_per_layer
        model.model.embed_tokens_per_layer = CPULookup(ple, device)
        model.to(device)
    return model


# Gated models are mounted from PRIVATE Kaggle datasets (a kernel pushed through the API cannot read the HF_TOKEN secret; RESULTS.md 2026-11-04)
KAGGLE_DATASETS = {"llama-2-7b": "shattered-llama-2-7b-hf", "llama-3.1-8b": "shattered-llama-3-1-8b", "ambari-7b-instruct-v0.1": "shattered-ambari-instruct-v0-1"}


def model_source(name: str) -> str:
    """The Kaggle dataset mount for a gated model when present (Kaggle only), else the Hugging Face repo id."""
    if name in KAGGLE_DATASETS and os.path.isdir("/kaggle/working"):
        import glob
        hits = glob.glob(f"/kaggle/input/**/{KAGGLE_DATASETS[name]}/config.json", recursive=True)
        if hits:
            return _local_copy(os.path.dirname(hits[0]), KAGGLE_DATASETS[name])
    return MODELS[name]


def _local_copy(src: str, slug: str) -> str:
    """Copy a model mounted from a private dataset to local disk with parallel reads before loading it (decided 2026-11-04 after Llama-3.1-8B took 48 minutes to load from the mount versus 11 minutes
    for Llama-2 on account 1). Copied once per session (marker file); falls back to the mount if the disk is too small or the copy fails. SHATTERED_COPY_MODEL=0 switches it off."""
    import shutil
    import time
    from concurrent.futures import ThreadPoolExecutor
    if os.environ.get("SHATTERED_COPY_MODEL", "1") == "0":
        return src
    dst = f"/tmp/shattered_models/{slug}"
    if os.path.exists(os.path.join(dst, ".done")):
        return dst
    try:
        files = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]
        size = sum(os.path.getsize(os.path.join(src, f)) for f in files)
        os.makedirs(dst, exist_ok=True)
        if shutil.disk_usage(dst).free < size * 1.15:
            print(f"[model_source] not enough local disk for {slug} ({size / 2**30:.1f} GiB); loading from the mount", flush=True)
            return src
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=8) as ex:
            list(ex.map(lambda f: shutil.copyfile(os.path.join(src, f), os.path.join(dst, f)), files))
        open(os.path.join(dst, ".done"), "w").write("ok")
        print(f"[model_source] copied {slug}: {size / 2**30:.1f} GiB in {time.time() - t0:.0f}s to local disk", flush=True)
        return dst
    except Exception as e:  # noqa: BLE001 - fall back to the mount
        print(f"[model_source] copy failed ({e!r}); loading from the mount", flush=True)
        return src


def load(name: str, device: str | None = None, dtype=torch.bfloat16, quant: str | None = None, offload: bool = False):
    """device "auto" shards over all visible GPUs (Phase 2 Kaggle 7-9B models); quant "8bit" or "4bit" uses bitsandbytes (never for retrieval).
    offload=True (A1-P-D1, float32 reference): 12 GiB per GPU, the rest of the weights stay in system RAM (up to 22 GiB)."""
    from transformers import AutoModelForCausalLM, AutoTokenizer
    if name in PICKLE_ONLY:
        # pickle .bin weights (no safetensors): Kaggle only, and torch.load is forced to weights_only=True (decided 2026-11-02)
        if not os.path.isdir("/kaggle/working"):
            raise RuntimeError(f"{name} ships pickle weights only; it is loaded on Kaggle only, never on the laptop")
        import functools
        torch.load = functools.partial(torch.load, weights_only=True)
    repo = model_source(name)
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    token = os.environ.get("HF_TOKEN")
    tok = AutoTokenizer.from_pretrained(repo, token=token)
    if name.startswith("gemma4"):
        model = _load_gemma4_text(repo, device, dtype, token)
    else:
        kw = {}
        if quant:
            from transformers import BitsAndBytesConfig
            kw["quantization_config"] = (BitsAndBytesConfig(load_in_8bit=True) if quant == "8bit" else
                                         BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=dtype))  # X11: NF4 with double quantisation
        if device == "auto":
            kw["max_memory"] = {i: "14.5GiB" for i in range(torch.cuda.device_count())}
            if offload:
                kw["max_memory"] = {i: "12GiB" for i in range(torch.cuda.device_count())} | {"cpu": "22GiB"}
        model, info = AutoModelForCausalLM.from_pretrained(repo, dtype=dtype, device_map="auto" if device == "auto" else {"": device},
                                                           token=token, output_loading_info=True, **kw)
        _check_loaded(name, info)
    model.eval()
    return model, tok


def n_layers(model) -> int:
    cfg = model.config
    return getattr(cfg, "num_hidden_layers", None) or cfg.text_config.num_hidden_layers
