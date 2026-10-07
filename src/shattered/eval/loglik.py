"""Log-likelihood scoring of label verbalizers for open models (no free generation)."""
from __future__ import annotations

from pathlib import Path

import torch

TEMPLATES = Path(__file__).resolve().parents[1] / "llm" / "templates"
VERBALIZERS = {"xnli": [" yes", " maybe", " no"],          # entailment, neutral, contradiction
               "sentiment": [" negative", " positive"]}     # label 0, 1


def build_prompt(task: str, fields: dict, version: str = "v1") -> str:
    return (TEMPLATES / f"e0_{task}_{version}.txt").read_text(encoding="utf-8").format(**fields)


@torch.no_grad()
def choice_logprobs(model, tok, prompt: str, choices: list[str]) -> tuple[list[float], int]:
    """Sum of log-probs of each choice's tokens after the prompt; also returns the prompt length in tokens.

    Continuation tokens are taken from tokenizing prompt+choice jointly; the prompt prefix must tokenize identically
    (checked), otherwise the choice is tokenized on its own and appended.
    """
    bos = [tok.bos_token_id] if tok.bos_token_id is not None and getattr(tok, "add_bos_token", True) else []
    p_ids = bos + tok(prompt, add_special_tokens=False)["input_ids"]
    seqs, conts = [], []
    for c in choices:
        full = bos + tok(prompt + c, add_special_tokens=False)["input_ids"]
        if full[: len(p_ids)] == p_ids:
            cont = full[len(p_ids):]
        else:
            cont = tok(c, add_special_tokens=False)["input_ids"]
        seqs.append(p_ids + cont)
        conts.append(len(cont))
    L = max(len(s) for s in seqs)
    pad = tok.pad_token_id if tok.pad_token_id is not None else 0
    ids = torch.tensor([s + [pad] * (L - len(s)) for s in seqs], device=model.device)
    att = torch.tensor([[1] * len(s) + [0] * (L - len(s)) for s in seqs], device=model.device)
    logits = model(input_ids=ids, attention_mask=att).logits.float()
    logp = torch.log_softmax(logits[:, :-1], -1)
    out = []
    for b, (s, n) in enumerate(zip(seqs, conts)):
        tgt = torch.tensor(s[len(s) - n:], device=model.device)
        pos = torch.arange(len(s) - n - 1, len(s) - 1, device=model.device)
        out.append(float(logp[b, pos, tgt].sum()))
    return out, len(p_ids)
