"""One forward pass per (model, form, sentence) feeding both M1 (word-level probes) and M4 (sentence alignment).

For every sentence we keep, at every layer (0 = embeddings):
  - the residual at each target word's last token (for word-identity probes, M1), and
  - the mean residual over the sentence's content tokens (for retrieval / CKA, M4).
Stored as float16 arrays in an .npz per (model, form, corpus) so analyses never re-run the model.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch

from ..tok.align import word_spans


@dataclass
class Sentence:
    sid: str
    text: str
    targets: list[str]  # words whose last-token states are wanted (must appear as whitespace words)


@torch.no_grad()
def collect(model, tok, sentences: list[Sentence], word_pattern: str = r"\S+", max_tokens: int = 512) -> dict:
    """Returns dict with
      word_states [n_occ, L+1, d] f16, word_meta list of (sid, word, n_tokens),
      sent_states [n_sent, L+1, d] f16 (mean over content tokens), sent_ids list,
      n_tokens per sentence."""
    bos = [tok.bos_token_id] if tok.bos_token_id is not None else []
    word_states, word_meta, sent_states, sent_ids, n_toks = [], [], [], [], []
    for s in sentences:
        enc = tok(s.text, return_offsets_mapping=True, add_special_tokens=False)
        ids, offs = enc["input_ids"][:max_tokens], enc["offset_mapping"][:max_tokens]
        x = torch.tensor([bos + ids], device=model.device)
        hs = model(input_ids=x, output_hidden_states=True).hidden_states
        H = torch.stack([h[0] for h in hs])  # [L+1, T, d]
        off = len(bos)
        sent_states.append(H[:, off:].float().mean(1).half().cpu().numpy())
        sent_ids.append(s.sid)
        n_toks.append(len(ids))
        want = set(s.targets)
        for span in word_spans(s.text, offs, word_pattern):
            if span.word in want and span.tok_end <= len(ids):
                word_states.append(H[:, off + span.last_token].half().cpu().numpy())
                word_meta.append((s.sid, span.word, span.n_tokens))
    d = model.config.hidden_size if hasattr(model.config, "hidden_size") else model.config.text_config.hidden_size
    return {"word_states": np.stack(word_states) if word_states else np.zeros((0, 0, d), np.float16),
            "word_meta": word_meta, "sent_states": np.stack(sent_states), "sent_ids": sent_ids,
            "n_tokens": np.asarray(n_toks)}
