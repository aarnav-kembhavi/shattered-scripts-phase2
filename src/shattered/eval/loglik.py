"""Log-likelihood scoring of label verbalizers for open models (no free generation)."""
from __future__ import annotations

from pathlib import Path

import torch

TEMPLATES = Path(__file__).resolve().parents[1] / "llm" / "templates"
VERBALIZERS = {"xnli": [" yes", " maybe", " no"],          # entailment, neutral, contradiction
               "sentiment": [" negative", " positive"]}     # label 0, 1


def build_prompt(task: str, fields: dict, version: str = "v1") -> str:
    return (TEMPLATES / f"e0_{task}_{version}.txt").read_text(encoding="utf-8").format(**fields)


def _prefix(tok) -> list[int]:
    """BOS whenever the model has one. Tokenizer flags are unreliable (Gemma 4 never adds it; Sarvam-1 adds it only via
    its post-processor while reporting add_bos_token=False), and these models degrade badly without it."""
    return [tok.bos_token_id] if tok.bos_token_id is not None else []


@torch.no_grad()
def choice_logprobs(model, tok, prompt: str, choices: list[str]) -> tuple[list[float], int]:
    """Sum of log-probs of each choice's tokens after the prompt; also returns the prompt length in tokens.

    Continuation tokens come from tokenizing prompt+choice jointly when the prompt prefix tokenizes identically,
    otherwise the choice is tokenized on its own. Each choice is scored in its own forward pass and only the logits of
    the continuation positions are materialized (`logits_to_keep`), so memory does not grow with
    prompt length x vocabulary size.
    """
    bos = _prefix(tok)
    p_ids = bos + tok(prompt, add_special_tokens=False)["input_ids"]
    out = []
    for c in choices:
        full = bos + tok(prompt + c, add_special_tokens=False)["input_ids"]
        cont = full[len(p_ids):] if full[: len(p_ids)] == p_ids else tok(c, add_special_tokens=False)["input_ids"]
        seq = torch.tensor([p_ids + cont], device=model.device)
        n = len(cont)
        logits = model(input_ids=seq, logits_to_keep=n + 1).logits[0, :-1].float()  # predicts the n cont tokens
        logp = torch.log_softmax(logits, -1)
        out.append(float(logp[torch.arange(n), torch.tensor(cont, device=model.device)].sum()))
    return out, len(p_ids)
