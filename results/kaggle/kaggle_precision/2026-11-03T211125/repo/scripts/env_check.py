"""Print hardware, library versions and which API keys are configured.

Usage: python scripts/env_check.py
Never prints key values, only whether each key is set.
"""
from __future__ import annotations

import importlib
import os
import platform
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

LIBS = [
    "torch", "transformers", "accelerate", "bitsandbytes", "datasets", "tokenizers", "tiktoken",
    "sentencepiece", "safetensors", "huggingface_hub", "indic_transliteration", "aksharamukha",
    "sklearn", "scipy", "statsmodels", "numpy", "pandas", "pyarrow", "matplotlib", "seaborn",
    "wordfreq", "nnsight", "google.genai", "anthropic", "groq", "openai", "dotenv", "tqdm", "yaml",
]

API_KEYS = ["GEMINI_API_KEY", "GROQ_API_KEY", "OPENROUTER_API_KEY", "ANTHROPIC_API_KEY", "HF_TOKEN"]


def section(title: str) -> None:
    print(f"\n== {title} ==")


def lib_version(name: str) -> str:
    try:
        mod = importlib.import_module(name)
    except Exception as e:  # noqa: BLE001 - report any import failure
        return f"NOT AVAILABLE ({type(e).__name__}: {e})"
    for attr in ("__version__", "VERSION", "version"):
        v = getattr(mod, attr, None)
        if isinstance(v, str):
            return v
    try:
        from importlib.metadata import version
        dist = {"sklearn": "scikit-learn", "google.genai": "google-genai", "dotenv": "python-dotenv",
                "yaml": "pyyaml"}.get(name, name)
        return version(dist)
    except Exception:  # noqa: BLE001
        return "installed (version unknown)"


def main() -> None:
    section("System")
    print(f"Python      {sys.version.split()[0]} ({sys.executable})")
    print(f"Platform    {platform.platform()}")
    print(f"CPU         {platform.processor() or platform.machine()}")
    print(f"Cores       {os.cpu_count()} logical")
    try:
        import psutil
        vm = psutil.virtual_memory()
        print(f"Cores phys  {psutil.cpu_count(logical=False)}")
        print(f"RAM         {vm.total / 2**30:.1f} GiB total, {vm.available / 2**30:.1f} GiB available")
    except ImportError:
        print("RAM         (psutil not installed)")
    du = shutil.disk_usage(REPO)
    print(f"Disk        {du.free / 2**30:.0f} GiB free of {du.total / 2**30:.0f} GiB ({REPO.anchor})")

    section("GPU")
    try:
        import torch
        print(f"torch CUDA build  {torch.version.cuda}")
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                p = torch.cuda.get_device_properties(i)
                print(f"GPU {i}       {p.name}, {p.total_memory / 2**30:.1f} GiB VRAM, "
                      f"compute capability {p.major}.{p.minor}")
            print(f"bf16 support      {torch.cuda.is_bf16_supported()}")
            x = torch.randn(256, 256, device="cuda")
            print(f"CUDA smoke test   ok (matmul sum={float((x @ x).sum()):.1f})")
        else:
            print("No CUDA GPU available to torch.")
    except Exception as e:  # noqa: BLE001
        print(f"torch/GPU check failed: {type(e).__name__}: {e}")

    section("Libraries")
    for name in LIBS:
        print(f"{name:<22}{lib_version(name)}")

    section("API keys (.env)")
    env_path = REPO / ".env"
    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv(env_path)
        print(f".env found at {env_path}")
    else:
        print(f".env NOT found at {env_path} (copy .env.example to .env)")
    for k in API_KEYS:
        print(f"{k:<22}{'present' if os.environ.get(k) else 'missing'}")


if __name__ == "__main__":
    main()
