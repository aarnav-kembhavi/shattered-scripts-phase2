"""GPU safety rule (Aarnav, 2026-10-23): before every model load, total GPU memory in use must be <= 500 MB.

Under the WDDM driver nvidia-smi reports no per-process memory, so anything above the desktop baseline (~150 MB) before
our own load belongs to another process (e.g. a job from another project). Call `wait_gpu_free()` in a fresh process,
before CUDA is initialized: once this process holds a CUDA context, its own memory would count.
"""
from __future__ import annotations

import subprocess
import time

LIMIT_MB = 500
MIN_FREE_DISK_GB = 25  # Aarnav, 2026-11-01: refuse to start a GPU job below this much free disk
RETRY_S = 300


def gpu_used_mb() -> int | None:
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=60).stdout
        return int(out.strip().splitlines()[0])
    except Exception:  # noqa: BLE001 - treated as busy and retried
        return None


def gpu_apps() -> str:
    try:
        return subprocess.run(["nvidia-smi", "--query-compute-apps=pid,process_name", "--format=csv,noheader"],
                              capture_output=True, text=True, timeout=60).stdout.strip().replace("\n", "; ")
    except Exception:  # noqa: BLE001
        return "?"


def require_free_disk(min_gb: float = MIN_FREE_DISK_GB, path: str = ".") -> float:
    """Exits (does not wait) if the free disk under `path` is below min_gb."""
    import shutil
    free = shutil.disk_usage(path).free / 1e9
    if free < min_gb:
        raise SystemExit(f"disk guard: {free:.1f} GB free < {min_gb} GB; refusing to start a GPU job")
    return free


def wait_gpu_free(limit_mb: int = LIMIT_MB, retry_s: int = RETRY_S) -> int:
    """Blocks until GPU memory in use <= limit_mb, logging every wait; returns the memory in use at the check."""
    require_free_disk()
    import torch
    assert not torch.cuda.is_initialized(), "wait_gpu_free must run before this process initializes CUDA"
    while True:
        used = gpu_used_mb()
        if used is not None and used <= limit_mb:
            print(f"gpuguard: {used} MB in use <= {limit_mb} MB; loading", flush=True)
            return used
        print(f"gpuguard {time.strftime('%F %T')}: {used} MB in use > {limit_mb} MB; GPU processes: {gpu_apps()}; "
              f"retry in {retry_s} s", flush=True)
        time.sleep(retry_s)
