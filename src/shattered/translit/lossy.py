"""Controlled lossy romanization, derived deterministically from ITRANS units.

Starting from ITRANS, it collapses long vowels to short, retroflex to dental, aspirated to unaspirated, and anusvara
variants to m/n, then lowercases. Lossiness is therefore the only difference from ITRANS. Raw runs (Latin text in the
source) are copied unchanged; Kannada digits become ASCII digits; separators and ZWJ/ZWNJ are dropped.

Information loss is measured by `LossyBackMapper`: each lossy word is mapped back to the most frequent native word
that produces it in a training corpus, and CER is computed against the original.
"""
from __future__ import annotations

from collections import Counter, defaultdict

from .scheme import ITRANS, KANNADA_DIGITS, Unit

# ITRANS spelling -> lossy spelling (before lowercasing). Unlisted spellings are kept, then lowercased.
LOSSY_FROM_ITRANS = {
    # long -> short vowels
    "A": "a", "I": "i", "U": "u", "E": "e", "O": "o", "RRi": "ri", "RRI": "ri", "L^i": "li", "L^I": "li",
    # retroflex -> dental (and retroflex+aspirated -> plain dental)
    "T": "t", "Th": "t", "D": "d", "Dh": "d", "N": "n", "L": "l", "Sh": "sh", "zh": "l", "R": "r",
    # aspirated -> unaspirated
    "kh": "k", "gh": "g", "Ch": "ch", "jh": "j", "th": "t", "dh": "d", "ph": "p", "bh": "b",
    # nasals and other signs
    "~N": "n", "~n": "n", "H": "h", ".N": "n", ".a": "", "^": "", "^^": "", "|": ".", "||": ".",
}
LABIALS = {"ಪ", "ಫ", "ಬ", "ಭ", "ಮ", "ವ"}


def _anusvara(next_unit: Unit | None) -> str:
    """Anusvara -> m before a labial or at a word end, else n."""
    if next_unit is None or next_unit.kind != "C":
        return "m"
    return "m" if next_unit.native in LABIALS else "n"


def to_lossy(text: str) -> str:
    units = ITRANS.units(text)
    out = []
    for i, u in enumerate(units):
        if u.kind == "RAW":
            out.append(u.native)
        elif u.kind == "LIT":
            out.append(u.native)
        elif u.kind == "DIG":
            out.append("".join(KANNADA_DIGITS[c] for c in u.native))
        elif u.kind == "S" and u.native == "ಂ":
            out.append(_anusvara(units[i + 1] if i + 1 < len(units) else None))
        else:
            sp = ITRANS._spell(u)
            out.append(LOSSY_FROM_ITRANS.get(sp, sp).lower())
    return "".join(out)


def char_error_rate(hyp: str, ref: str) -> float:
    """Levenshtein distance / len(ref)."""
    if not ref:
        return float(len(hyp) > 0)
    prev = list(range(len(hyp) + 1))
    for i, rc in enumerate(ref, 1):
        cur = [i] + [0] * len(hyp)
        for j, hc in enumerate(hyp, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (rc != hc))
        prev = cur
    return prev[-1] / len(ref)


class LossyBackMapper:
    """Best-possible word-level inversion of `to_lossy`, learned from a native corpus.

    Each lossy word maps to its most frequent native source word in the training corpus. Unseen lossy words fall back
    to decoding them as ITRANS (all-short, all-dental reading).
    """

    def __init__(self) -> None:
        self.table: dict[str, str] = {}

    def fit(self, native_texts) -> LossyBackMapper:
        counts: dict[str, Counter] = defaultdict(Counter)
        for t in native_texts:
            for w in t.split():
                counts[to_lossy(w)][w] += 1
        self.table = {lw: c.most_common(1)[0][0] for lw, c in counts.items()}
        return self

    def invert(self, lossy_text: str) -> str:
        return " ".join(self.table.get(w) or self._fallback(w) for w in lossy_text.split())

    @staticmethod
    def _fallback(word: str) -> str:
        try:
            return ITRANS.decode(word)
        except (ValueError, KeyError):
            return word

    def coverage(self, lossy_text: str) -> float:
        words = lossy_text.split()
        return sum(w in self.table for w in words) / max(len(words), 1)
