"""Download a gated Hugging Face model on the laptop (the token in .env has the approved access) and upload it as a PRIVATE Kaggle dataset, so Kaggle kernels need no HF_TOKEN secret
(decided 2026-11-04: secrets cannot be attached through the kernels API). Dataset slugs are fixed in `shattered.interp.load.KAGGLE_DATASETS`; the loader uses the mounted copy on Kaggle.
Usage: python scripts/hf_to_kaggle.py <model name, e.g. llama-2-7b> [--keep-local]
Only config/tokenizer files and the safetensors weights are fetched. The local copy is deleted after a verified upload unless --keep-local. Credentials are never printed."""
import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import kaggle_runner as KR  # noqa: E402
from dotenv import load_dotenv  # noqa: E402
from huggingface_hub import snapshot_download  # noqa: E402

from shattered.interp.load import KAGGLE_DATASETS, MODELS  # noqa: E402
from shattered.runlog import REPO  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("model")
ap.add_argument("--keep-local", action="store_true")
a = ap.parse_args()
load_dotenv(REPO / ".env")
slug, repo = KAGGLE_DATASETS[a.model], MODELS[a.model]
d = REPO / "data" / "hf_local" / slug
t0 = time.time()
print(f"downloading {repo} to {d}", flush=True)
snapshot_download(repo, local_dir=str(d), token=os.environ["HF_TOKEN"], allow_patterns=["*.json", "*.safetensors", "tokenizer.model"])
files = sorted(p.name for p in d.iterdir() if p.is_file())
size = sum(p.stat().st_size for p in d.iterdir() if p.is_file())
print(f"downloaded {len(files)} files, {size / 2**30:.2f} GiB in {time.time() - t0:.0f}s: {files}", flush=True)
assert any(f.endswith(".safetensors") for f in files) and "config.json" in files
shutil.rmtree(d / ".cache", ignore_errors=True)
user = KR.env()["KAGGLE_USERNAME"]
(d / "dataset-metadata.json").write_text(json.dumps({"title": slug, "id": f"{user}/{slug}", "licenses": [{"name": "other"}], "isPrivate": True,
                                                    "subtitle": "Private copy of a gated model for own research"}))
t1 = time.time()
exists = slug in KR.kaggle("datasets", "list", "--mine", "-s", slug, check=False)
print(KR.kaggle("datasets", "version" if exists else "create", "-p", str(d), *(["-m", "refresh"] if exists else []), "--dir-mode", "tar"), flush=True)
s = ""
for _ in range(360):
    s = KR.kaggle("datasets", "status", f"{user}/{slug}", check=False)
    if "ready" in s.lower():
        break
    time.sleep(10)
else:
    raise SystemExit("dataset not ready after 60 minutes: " + s[-300:])
meta = KR.kaggle("datasets", "metadata", f"{user}/{slug}", "-p", str(REPO / "build"), check=False)
print(f"uploaded {user}/{slug} (private) in {time.time() - t1:.0f}s; status: {s.strip()[:80]}", flush=True)
if not a.keep_local:
    shutil.rmtree(d)
    print("local copy deleted", flush=True)
