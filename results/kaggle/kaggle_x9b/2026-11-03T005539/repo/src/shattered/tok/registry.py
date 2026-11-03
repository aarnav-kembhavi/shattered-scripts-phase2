"""Load tokenizers (tiktoken encodings or HF tokenizer files only, never weights) behind one counting interface."""
from __future__ import annotations

import os
from collections.abc import Callable

from dotenv import load_dotenv

from ..runlog import REPO

load_dotenv(REPO / ".env")


def load_counter(spec: dict) -> Callable[[list[str]], list[int]]:
    """Return f(texts) -> token counts (no special tokens). Raises if the tokenizer needs remote code."""
    if spec["kind"] == "tiktoken":
        import tiktoken
        enc = tiktoken.get_encoding(spec["id"])
        return lambda texts: [len(x) for x in enc.encode_ordinary_batch(texts)]
    tok = load_hf_tokenizer(spec["id"])
    return lambda texts: [len(x) for x in tok(texts, add_special_tokens=False)["input_ids"]]


def load_hf_tokenizer(repo: str):
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained(repo, token=os.environ.get("HF_TOKEN"), trust_remote_code=False)
