"""Word-level language tags for Kanglish (Latin-script Kannada-English) and the Code Mixing Index.

Lexicons: English = wordfreq 3.1.1 top 50,000 English words; romanized Kannada = to_lossy() of the 50,000 most frequent
Kannada Wikipedia words (data/processed/kn_wiki_wordfreq.parquet). A lower-cased alphabetic token is English if it is
in the English lexicon only, ambiguous if in both, Kannada otherwise (out-of-lexicon tokens are far more often
informally spelled Kannada than rare English). Digits, punctuation and ambiguous tokens are language-independent (u).
CMI (Das and Gambäck 2014) = 100 * (1 - max(n_en, n_kn) / (n - u)), 0 if n == u.
English word share = n_en / (n_en + n_kn).
"""
from __future__ import annotations

import re
from functools import lru_cache

from ..runlog import REPO

N_LEX = 50_000
TOKEN = re.compile(r"[A-Za-z]+|\d+|[^\sA-Za-z\d]+")


@lru_cache(1)
def lexicons() -> tuple[frozenset, frozenset]:
    import pandas as pd
    import wordfreq
    from . import to_lossy
    en = frozenset(w for w in wordfreq.top_n_list("en", N_LEX) if w.isascii() and w.isalpha())
    kn_words = pd.read_parquet(REPO / "data" / "processed" / "kn_wiki_wordfreq.parquet", columns=["word", "rank"])
    kn_words = kn_words.nsmallest(N_LEX, "rank").word
    kn = frozenset(t for w in kn_words for t in re.findall(r"[a-z]+", to_lossy(w).lower()))
    return en, kn


def tag(text: str) -> list[tuple[str, str]]:
    en, kn = lexicons()
    out = []
    for t in TOKEN.findall(text):
        if not t.isalpha():
            out.append((t, "u"))
            continue
        w = t.lower()
        out.append((t, "u" if (w in en and w in kn) else "en" if w in en else "kn"))
    return out


def code_mixing(text: str) -> dict:
    tags = [g for _, g in tag(text)]
    n_en, n_kn, n = tags.count("en"), tags.count("kn"), len(tags)
    u = n - n_en - n_kn
    return {"n_en": n_en, "n_kn": n_kn, "n_u": u,
            "cmi": 100 * (1 - max(n_en, n_kn) / (n - u)) if n > u else 0.0,
            "english_share": n_en / (n_en + n_kn) if n_en + n_kn else 0.0}
