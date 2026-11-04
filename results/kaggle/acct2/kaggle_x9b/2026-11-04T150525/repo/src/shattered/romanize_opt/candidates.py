"""Candidate Latin spellings for each Kannada unit (E9 search space).

Drawn from ITRANS, Harvard-Kyoto, Velthuis, IAST-ASCII and common informal spellings, plus a few spare letters
(q, x, c, w) so every unit with an uppercase ITRANS spelling has lowercase alternatives. Any combination is lossless by
construction: the scheme engine rejects duplicate spellings and inserts separators where greedy decoding would
otherwise go wrong (the cost of those separators is part of the objective).

Units that are fixed (not searched): the inherent vowel "a", the danda signs.
"""
from __future__ import annotations

from ..translit.scheme import ITRANS_CONSONANTS, ITRANS_SIGNS, ITRANS_VOWELS, ZWJ, ZWNJ

NUK = "಼"
VOWELS = {
    "ಆ": ["A", "aa"], "ಇ": ["i"], "ಈ": ["I", "ii", "ee", "iy"], "ಉ": ["u"], "ಊ": ["U", "uu", "oo", "uw"],
    # "ru"/"ri" (and "ruu"/"rii") are excluded: they make the very common ರು/ರಿ unencodable (r + vowel sign would
    # be read as the vocalic-r vowel, and a separator may not split a consonant from its vowel sign).
    "ಋ": ["RRi", "R^i", "rri", "rq"], "ೠ": ["RRI", "rrii", "rqq"],
    "ಌ": ["L^i", "lri", "lq"], "ೡ": ["L^I", "lrii", "lqq"],
    "ಎ": ["e"], "ಏ": ["E", "ee", "ae", "ey", "ei"], "ಐ": ["ai", "ei", "ay"],
    "ಒ": ["o"], "ಓ": ["O", "oo", "oa", "ow"], "ಔ": ["au", "ou", "aw"],
}
CONSONANTS = {
    "ಕ": ["k"], "ಖ": ["kh", "K", "q"], "ಗ": ["g"], "ಘ": ["gh", "G"], "ಙ": ["~N", "ng", "nq"],
    "ಚ": ["ch", "c"], "ಛ": ["Ch", "chh", "C", "cch"], "ಜ": ["j"], "ಝ": ["jh", "J"], "ಞ": ["~n", "ny", "nj", "gn"],
    "ಟ": ["T", "tt", "tx"], "ಠ": ["Th", "tth", "txh"], "ಡ": ["D", "dd", "dx"], "ಢ": ["Dh", "ddh", "dxh"],
    "ಣ": ["N", "nn", "nx"],
    "ತ": ["t", "th"], "ಥ": ["th", "tth", "thh"], "ದ": ["d", "dh"], "ಧ": ["dh", "ddh", "dhh"], "ನ": ["n"],
    "ಪ": ["p"], "ಫ": ["ph", "f", "P"], "ಬ": ["b"], "ಭ": ["bh", "B"], "ಮ": ["m"],
    "ಯ": ["y"], "ರ": ["r"], "ಱ": ["R", "rr", "rx"], "ಲ": ["l"], "ಳ": ["L", "ll", "lx", "lh"], "ೞ": ["zh", "zx"],
    "ವ": ["v", "w"], "ಶ": ["sh", "S", "x", "sx"], "ಷ": ["Sh", "shh", "ss", "sx"], "ಸ": ["s"], "ಹ": ["h"],
    "ಫ" + NUK: ["f", "fx", "F"], "ಜ" + NUK: ["z", "zz", "Z"],
}
SIGNS = {
    "ಂ": ["M", "mq", "nq", "q", "x", "m.", "n."],   # anusvara
    "ಃ": ["H", "h:", ":", "hq"],                     # visarga
    "ಁ": [".N", "n~"],                               # candrabindu
    "ಽ": [".a", "'"],                                # avagraha
    ZWNJ: ["^", "~"], ZWJ: ["^^", "~~"],
}
FIXED_VOWELS = {"ಅ": "a"}
FIXED_SIGNS = {"।": "|", "॥": "||"}


def all_candidates(lowercase_only: bool = False) -> dict[tuple[str, str], list[str]]:
    """{(table, native): [spellings]} for every searchable unit."""
    out = {}
    for table, cands in (("vowels", VOWELS), ("consonants", CONSONANTS), ("signs", SIGNS)):
        for native, sps in cands.items():
            sps = [s for s in sps if not lowercase_only or s == s.lower()]
            assert sps, f"no lowercase candidate for {native}"
            out[(table, native)] = sps
    return out


def itrans_assignment() -> dict[tuple[str, str], str]:
    a = {}
    for table, src in (("vowels", ITRANS_VOWELS), ("consonants", ITRANS_CONSONANTS), ("signs", ITRANS_SIGNS)):
        for native, sp in src.items():
            if (table == "vowels" and native in FIXED_VOWELS) or (table == "signs" and native in FIXED_SIGNS):
                continue
            a[(table, native)] = sp
    return a


def tables(assign: dict[tuple[str, str], str]) -> tuple[dict, dict, dict]:
    v = {**FIXED_VOWELS, **{n: s for (t, n), s in assign.items() if t == "vowels"}}
    c = {n: s for (t, n), s in assign.items() if t == "consonants"}
    g = {**FIXED_SIGNS, **{n: s for (t, n), s in assign.items() if t == "signs"}}
    return c, v, g
