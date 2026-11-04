"""Cache residual-stream activations per layer for open models, so probes and CKA never re-run the model.

One file per (model, input form, item, position spec), stored as float16 safetensors with shape
[n_layers + 1, n_positions, d_model]. Index 0 is the embedding output; index L is the output of block L, taken from
HF `output_hidden_states`. Note that for many HF models the last entry already has the final norm applied.

Storing only selected positions (e.g. each word's last token, or the readout position) keeps the cache small; pass
`positions=None` to store every position.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable
from pathlib import Path

import torch
from safetensors.torch import load_file, save_file

from ..runlog import REPO

DEFAULT_ROOT = REPO / "activations"


def _slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s)


class ActivationCache:
    def __init__(self, model_id: str, root: Path | str = DEFAULT_ROOT) -> None:
        self.model_id = model_id
        self.dir = Path(root) / _slug(model_id)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.n_forward = 0  # forward passes actually run (for tests and logging)

    def path(self, form: str, item_id: str, pos_tag: str) -> Path:
        h = hashlib.sha256(f"{form}|{item_id}|{pos_tag}".encode()).hexdigest()[:16]
        return self.dir / _slug(form) / f"{_slug(str(item_id))[:60]}_{h}.safetensors"

    def has(self, form: str, item_id: str, pos_tag: str = "all") -> bool:
        return self.path(form, item_id, pos_tag).exists()

    def load(self, form: str, item_id: str, pos_tag: str = "all") -> tuple[torch.Tensor, dict]:
        p = self.path(form, item_id, pos_tag)
        from safetensors import safe_open
        with safe_open(str(p), "pt") as f:
            meta = json.loads(f.metadata()["meta"])
        return load_file(str(p))["acts"], meta

    @torch.no_grad()
    def get(self, model, tokenizer, text: str, form: str, item_id: str,
            positions: Callable[[list[int], dict], list[int]] | None = None, pos_tag: str = "all",
            extra_meta: dict | None = None) -> tuple[torch.Tensor, dict]:
        """Return cached activations, computing them once if missing.

        `positions(input_ids, enc)` picks token positions to store; `pos_tag` must identify that choice, because it is
        part of the cache key.
        """
        if self.has(form, item_id, pos_tag):
            return self.load(form, item_id, pos_tag)
        enc = tokenizer(text, return_tensors="pt", return_offsets_mapping=getattr(tokenizer, "is_fast", False))
        offsets = enc.pop("offset_mapping", None)
        ids = enc["input_ids"][0].tolist()
        out = model(**{k: v.to(model.device) for k, v in enc.items()}, output_hidden_states=True)
        self.n_forward += 1
        hs = torch.stack(out.hidden_states, dim=0)[:, 0]  # [L+1, T, d]
        pos = list(range(len(ids))) if positions is None else list(positions(ids, {"offsets": offsets}))
        acts = hs[:, pos].to(torch.float16).cpu().contiguous()
        meta = {"model": self.model_id, "form": form, "item_id": str(item_id), "pos_tag": pos_tag,
                "text": text, "input_ids": ids, "positions": pos, **(extra_meta or {})}
        p = self.path(form, item_id, pos_tag)
        p.parent.mkdir(parents=True, exist_ok=True)
        save_file({"acts": acts}, str(p), metadata={"meta": json.dumps(meta, ensure_ascii=False)})
        return acts, meta
