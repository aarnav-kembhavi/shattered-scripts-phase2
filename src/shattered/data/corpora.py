"""Pinned loaders for raw text corpora. Revisions are pinned so results are reproducible."""
from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv

from ..runlog import REPO

load_dotenv(REPO / ".env")
RAW = REPO / "data" / "raw"

FLORES_REPO = "openlanguagedata/flores_plus"
FLORES_REV = "e707e62e762a9e2faca3933aa315f4665cc3cd8f"
WIKI_REPO = "wikimedia/wikipedia"
WIKI_REV = "b04c8d1ceb2f5cd4588862100d08de323dccfbaa"


def _download(repo: str, filename: str, revision: str, subdir: str) -> Path:
    from huggingface_hub import hf_hub_download
    return Path(hf_hub_download(repo, filename, repo_type="dataset", revision=revision,
                                token=os.environ.get("HF_TOKEN"), local_dir=RAW / subdir))


def flores(lang: str, split: str) -> list[dict]:
    """FLORES+ rows for e.g. lang='kan_Knda', split='dev' or 'devtest'. Gated: requires accepted terms on HF."""
    p = _download(FLORES_REPO, f"{split}/{lang}.jsonl", FLORES_REV, "flores_plus")
    return [json.loads(line) for line in p.open(encoding="utf-8")]


def wikipedia(lang: str = "kn", dump: str = "20231101") -> list[str]:
    import pyarrow.parquet as pq
    p = _download(WIKI_REPO, f"{dump}.{lang}/train-00000-of-00001.parquet", WIKI_REV, f"wikipedia_{lang}")
    return pq.read_table(p, columns=["text"]).column("text").to_pylist()
