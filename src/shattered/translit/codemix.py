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


# ---------------------------------------------------------------- v2 (pre-data fix, RESULTS.md 2026-10-26; v1 above
# failed the Kanglish validity check: recall 0.883 < 0.9). v1 is kept unchanged for the record.
EN_ZIPF_OOV = 2.5  # a token in neither lexicon is English if its wordfreq English Zipf is at least this
KN_FORCE = frozenset({"ee"})  # lexicon correction (2026-10-26): ಈ is romanized "i" by to_lossy, so "ee" ("this") is missing


@lru_cache(1)
def ranks() -> tuple[dict, dict]:
    """English rank (position in the wordfreq top-50k list) and Kannada rank (best rank of a Kannada Wikipedia word
    whose to_lossy() romanization contains the token as an [a-z]+ run)."""
    import pandas as pd
    import wordfreq
    from . import to_lossy
    en = {}
    for k, w in enumerate(x for x in wordfreq.top_n_list("en", N_LEX) if x.isascii() and x.isalpha()):
        en.setdefault(w, k)
    kn_words = pd.read_parquet(REPO / "data" / "processed" / "kn_wiki_wordfreq.parquet", columns=["word", "rank"])
    kn = {}
    for w, r in kn_words.nsmallest(N_LEX, "rank").itertuples(index=False):
        for t in re.findall(r"[a-z]+", to_lossy(w).lower()):
            if t not in kn or r < kn[t]:
                kn[t] = r
    return en, kn


def names_in(english: str) -> set:
    """Lower-cased tokens that occur in the English sentence only in Title case and never sentence-initially."""
    title, other = set(), set()
    for m in re.finditer(r"[A-Za-z]+", english):
        t = m.group(0)
        start = re.search(r"(^|[.!?]\s+|[\"'(]\s*)$", english[:m.start()]) is not None
        if len(t) > 1 and t[0].isupper() and t[1:].islower() and not start:
            title.add(t.lower())
        else:
            other.add(t.lower())
    return title - other


def tag_v2(text: str, english: str = "") -> list[tuple[str, str]]:
    """v2: single letters u; names (Title case only, not sentence-initial, in the parallel English sentence) u; a token
    in both lexicons goes to the language where it ranks higher; a token in neither is English if its English Zipf
    >= EN_ZIPF_OOV, else Kannada. English stem + Kannada suffix stays Kannada (lower bound)."""
    from wordfreq import zipf_frequency
    en_r, kn_r = ranks()
    names = names_in(english) if english else set()
    out = []
    for t in TOKEN.findall(text):
        if not t.isalpha() or len(t) == 1:
            out.append((t, "u"))
            continue
        w = t.lower()
        if w in KN_FORCE:
            g = "kn"
        elif w in names:
            g = "u"
        elif w in en_r and w in kn_r:
            g = "en" if en_r[w] < kn_r[w] else "kn"
        elif w in en_r:
            g = "en"
        elif w in kn_r:
            g = "kn"
        else:
            g = "en" if zipf_frequency(w, "en") >= EN_ZIPF_OOV else "kn"
        out.append((t, g))
    return out


def code_mixing_v2(text: str, english: str = "") -> dict:
    tags = [g for _, g in tag_v2(text, english)]
    n_en, n_kn, n = tags.count("en"), tags.count("kn"), len(tags)
    u = n - n_en - n_kn
    return {"n_en": n_en, "n_kn": n_kn, "n_u": u,
            "cmi": 100 * (1 - max(n_en, n_kn) / (n - u)) if n > u else 0.0,
            "english_share": n_en / (n_en + n_kn) if n_en + n_kn else 0.0}
