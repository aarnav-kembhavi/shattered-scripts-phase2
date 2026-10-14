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


def wikipedia(lang: str = "kn", dump: str = "20231101", shard: str = "00000-of-00001") -> list[str]:
    """Articles of one parquet shard (Kannada has a single shard; English has 41, shard 0 is used for M1)."""
    import pyarrow.parquet as pq
    p = _download(WIKI_REPO, f"{dump}.{lang}/train-{shard}.parquet", WIKI_REV, f"wikipedia_{lang}")
    return pq.read_table(p, columns=["text"]).column("text").to_pylist()


# Meta's original FLORES-200 release (CC-BY-SA 4.0, public, not gated). Used for draft runs while FLORES+ access is
# pending. sha256 of the tarball as downloaded on 2026-10-07.
FLORES200_URL = "https://dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz"
FLORES200_SHA256 = "b8b0b76783024b85797e5cc75064eb83fc5288b41e9654dabc7be6ae944011f6"
FLORES_LANGS = ["eng_Latn", "kan_Knda", "tam_Taml", "tel_Telu", "mal_Mlym", "hin_Deva", "ben_Beng"]


def flores200(lang: str, split: str) -> list[str]:
    """Sentences of FLORES-200 for lang (e.g. 'kan_Knda'), split 'dev' or 'devtest'. Downloads the tarball once."""
    import hashlib
    import tarfile
    import urllib.request
    root = RAW / "flores200"
    path = root / "flores200_dataset" / split / f"{lang}.{split}"
    if not path.exists():
        root.mkdir(parents=True, exist_ok=True)
        tgz = root / "flores200_dataset.tar.gz"
        if not tgz.exists():
            urllib.request.urlretrieve(FLORES200_URL, tgz)
        if hashlib.sha256(tgz.read_bytes()).hexdigest() != FLORES200_SHA256:
            raise ValueError("FLORES-200 tarball checksum mismatch")
        with tarfile.open(tgz) as tf:
            tf.extractall(root, filter="data")
    return path.read_text(encoding="utf-8").splitlines()


def flores_any(lang: str, split: str, source: str = "flores200", nfc: bool = False) -> list[str]:
    """Sentences from 'flores200' (public) or 'flores_plus' (gated, preferred once access is granted).

    Experiments pass nfc=True: 17 of 2009 FLORES-200 Kannada sentences are not NFC-normalized.
    """
    import unicodedata
    texts = [r["text"] for r in flores(lang, split)] if source == "flores_plus" else flores200(lang, split)
    return [unicodedata.normalize("NFC", t) for t in texts] if nfc else texts
