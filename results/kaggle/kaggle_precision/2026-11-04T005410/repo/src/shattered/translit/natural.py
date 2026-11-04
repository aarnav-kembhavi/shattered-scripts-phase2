"""Natural (informal) romanization of Kannada via a free-tier LLM with a fixed, versioned prompt.

Realistic but noisy and not reversible. Calls are cached (see llm/cache.py), temperature 0.
"""
from __future__ import annotations

from pathlib import Path

from ..llm.client import LLMClient

TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "llm" / "templates"
PROMPT_VERSION = "natural_romanization_v1"
MODEL = "gemini-3.5-flash-lite"


def prompt(text: str, version: str = PROMPT_VERSION) -> str:
    return (TEMPLATE_DIR / f"{version}.txt").read_text(encoding="utf-8").format(text=text)


def make_client(rpm: float = 12, rpd: int = 1000) -> LLMClient:
    return LLMClient("gemini", MODEL, rpm=rpm, rpd=rpd)


def romanize(client: LLMClient, text: str, version: str = PROMPT_VERSION, attempt: int = 1) -> dict:
    """`attempt` > 1 re-asks the same model with the same prompt and temperature; it only changes the cache key (it is
    not sent to the API), so a defective cached answer can be regenerated without overwriting the first attempt."""
    extra = {"attempt": attempt} if attempt > 1 else {}
    r = client.generate(prompt(text, version), max_tokens=1024, temperature=0.0, **extra)
    out = r.text.strip()
    n_in, n_out = len(text.split()), len(out.split())
    return {"natural": out, "cached": r.cached, "finish_reason": r.finish_reason,
            "input_tokens": r.input_tokens, "output_tokens": r.output_tokens,
            "word_ratio": n_out / max(n_in, 1),
            "non_ascii_chars": sum(not c.isascii() for c in out),
            "attempt": attempt,
            "non_ascii_not_in_source": "".join(sorted({c for c in out if not c.isascii() and c not in text})),
            "indic_script_chars": "".join(sorted({c for c in out if "ऀ" <= c <= "෿"})),
            "flag": (not out) or not (0.7 <= n_out / max(n_in, 1) <= 1.3) or any("ಀ" <= c <= "೿" for c in out)}


def defective(row: dict) -> bool:
    """Output violates the prompt: any Indic-script character (U+0900-U+0DFF: leftover Kannada or another Indic script),
    or any other non-ASCII character not already in the source text (diacritics, IPA). Non-ASCII Latin copied from the
    source (e.g. "À la carte") is allowed."""
    return any("ऀ" <= c <= "෿" or (not c.isascii() and c not in row["native"]) for c in row["natural"])
