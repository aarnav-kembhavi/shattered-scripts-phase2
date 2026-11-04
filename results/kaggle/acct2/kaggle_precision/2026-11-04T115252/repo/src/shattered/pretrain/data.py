"""E5 data: TinyStories V2 (GPT-4) stories, byte-level BPE tokenizers at several vocab sizes, pre-tokenized streams.

Every condition trains on exactly the same text: the first `train_bytes` bytes (cut at a story boundary) of the
training stories after a fixed document-level shuffle. Stories are joined with one EOS token; the separator counts as
one byte in all bits-per-byte computations.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

import numpy as np

from ..runlog import REPO

RAW = REPO / "data" / "raw" / "tinystories"
PROC = REPO / "data" / "processed" / "e05"
TS_REPO, TS_REV = "roneneldan/TinyStories", "f54c09fd23315a6f9c86f9dc80f725de7d8f9c64"
EOS = "<|endoftext|>"


def read_stories(split: str) -> list[str]:
    name = {"train": "TinyStoriesV2-GPT4-train.txt", "valid": "TinyStoriesV2-GPT4-valid.txt"}[split]
    text = (RAW / name).read_text(encoding="utf-8")
    return [s.strip() for s in text.split(EOS) if len(s.strip()) >= 50]


def training_stories(train_bytes: int, data_seed: int = 0) -> list[str]:
    """Shuffled stories whose UTF-8 size (plus one separator byte each) first reaches train_bytes."""
    stories = read_stories("train")
    random.Random(data_seed).shuffle(stories)
    out, total = [], 0
    for s in stories:
        if total >= train_bytes:
            break
        out.append(s)
        total += len(s.encode("utf-8")) + 1
    return out


def train_tokenizer(stories: list[str], vocab: int, path: Path):
    """Byte-level BPE with `vocab` byte/merge tokens plus one EOS special token (vocab=256 -> pure bytes)."""
    from tokenizers import Tokenizer, decoders, models, pre_tokenizers, trainers
    tok = Tokenizer(models.BPE())
    tok.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    tok.decoder = decoders.ByteLevel()
    trainer = trainers.BpeTrainer(vocab_size=vocab + 1, special_tokens=[EOS], show_progress=False,
                                  initial_alphabet=pre_tokenizers.ByteLevel.alphabet(), min_frequency=2)
    tok.train_from_iterator(stories, trainer=trainer)
    path.parent.mkdir(parents=True, exist_ok=True)
    tok.save(str(path))
    return tok


def load_tokenizer(path: Path):
    from tokenizers import Tokenizer
    return Tokenizer.from_file(str(path))


def tokenize_stream(tok, stories: list[str], batch: int = 20000) -> np.ndarray:
    """Concatenate stories with EOS between (and after the last) as a uint16 token stream."""
    eos = tok.token_to_id(EOS)
    parts = []
    for i in range(0, len(stories), batch):
        for enc in tok.encode_batch(stories[i:i + batch]):
            parts.append(np.asarray(enc.ids, dtype=np.uint16))
            parts.append(np.asarray([eos], dtype=np.uint16))
    return np.concatenate(parts)


def prepare(vocabs: list[int], train_bytes: int, tokenizer_train_bytes: int, data_seed: int = 0,
            valid_bytes: int | None = None) -> dict:
    """Train tokenizers and write token streams; idempotent (skips finished pieces). Returns metadata."""
    PROC.mkdir(parents=True, exist_ok=True)
    meta_path = PROC / f"meta_{train_bytes}.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    train = training_stories(train_bytes, data_seed)
    valid = read_stories("valid")
    if valid_bytes:
        cut, total = [], 0
        for s in valid:
            if total >= valid_bytes:
                break
            cut.append(s)
            total += len(s.encode("utf-8")) + 1
        valid = cut
    n_train_bytes = sum(len(s.encode("utf-8")) + 1 for s in train)
    n_valid_bytes = sum(len(s.encode("utf-8")) + 1 for s in valid)
    tok_corpus = training_stories(tokenizer_train_bytes, data_seed)  # prefix of the same shuffled stream
    for v in vocabs:
        key = str(v)
        tpath = PROC / f"tokenizer_{v}.json"
        tok = load_tokenizer(tpath) if tpath.exists() else train_tokenizer(tok_corpus, v, tpath)
        tr_path = PROC / f"train_{v}_{train_bytes}.npy"
        va_path = PROC / f"valid_{v}_{valid_bytes or 'all'}.npy"
        if not tr_path.exists():
            np.save(tr_path, tokenize_stream(tok, train))
        if not va_path.exists():
            np.save(va_path, tokenize_stream(tok, valid))
        n_tr, n_va = len(np.load(tr_path, mmap_mode="r")), len(np.load(va_path, mmap_mode="r"))
        meta[key] = {"vocab": v, "vocab_with_eos": tok.get_vocab_size(), "train_tokens": n_tr,
                     "valid_tokens": n_va, "train_bytes": n_train_bytes, "valid_bytes": n_valid_bytes,
                     "bytes_per_token_train": n_train_bytes / n_tr, "bytes_per_token_valid": n_valid_bytes / n_va,
                     "tokenizer": str(tpath.relative_to(REPO)), "train_stream": str(tr_path.relative_to(REPO)),
                     "valid_stream": str(va_path.relative_to(REPO))}
    meta["_data"] = {"repo": TS_REPO, "revision": TS_REV, "files": "TinyStoriesV2-GPT4-{train,valid}.txt",
                     "train_stories": len(train), "valid_stories": len(valid), "data_seed": data_seed,
                     "tokenizer_train_bytes": tokenizer_train_bytes}
    meta_path.write_text(json.dumps(meta, indent=2))
    return meta
