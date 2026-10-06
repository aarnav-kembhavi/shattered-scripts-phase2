"""Reversible romanization schemes for Kannada.

A scheme maps Kannada units (consonants, vowels, signs) to Latin spellings. The encoder inserts a separator wherever
greedy longest-match decoding would otherwise mis-segment, so any scheme that passes `Scheme.validate()` round-trips
exactly. ITRANS is one such scheme; E9 searches over others with the same engine.

Romanized text grammar (for a scheme with separator "_"):
  - spelling tokens, decoded by longest match. A consonant token directly followed by a vowel token takes that vowel
    as its vowel sign; a consonant token followed by anything else gets a virama.
  - "_" separator: decodes to nothing; it only breaks a merge or a consonant-vowel attachment.
  - "{...}" raw run: copied verbatim (inside, "{", "}" and "\\" are backslash-escaped). Used for Latin letters and any
    character that would otherwise be read as a spelling or delimiter.
  - "#...#" Kannada digit run, written with ASCII digits. ASCII digits in the source pass through unchanged.
  - any other character is a literal.
"""
from __future__ import annotations

from dataclasses import dataclass, field

VIRAMA = "್"
NUKTA = "಼"
ZWNJ = "‌"
ZWJ = "‍"
INHERENT_A = "ಅ"  # ಅ, key for the inherent vowel

# Dependent vowel sign -> independent vowel (the key used in scheme tables).
MATRA_TO_VOWEL = {
    "ಾ": "ಆ", "ಿ": "ಇ", "ೀ": "ಈ", "ು": "ಉ", "ೂ": "ಊ",
    "ೃ": "ಋ", "ೄ": "ೠ", "ೢ": "ಌ", "ೣ": "ೡ", "ೆ": "ಎ",
    "ೇ": "ಏ", "ೈ": "ಐ", "ೊ": "ಒ", "ೋ": "ಓ", "ೌ": "ಔ",
}
VOWEL_TO_MATRA = {v: m for m, v in MATRA_TO_VOWEL.items()}
VOWEL_TO_MATRA[INHERENT_A] = ""

KANNADA_DIGITS = {chr(0x0CE6 + d): str(d) for d in range(10)}
ASCII_TO_KANNADA_DIGIT = {v: k for k, v in KANNADA_DIGITS.items()}

RAW_OPEN, RAW_CLOSE, RAW_ESC, DIGIT_DELIM = "{", "}", "\\", "#"


def is_kannada(ch: str) -> bool:
    return "ಀ" <= ch <= "೿"


@dataclass(frozen=True)
class Unit:
    kind: str  # "C" consonant, "V" vowel attached to preceding C, "IV" independent vowel, "S" sign,
    #            "DIG" Kannada digit run, "RAW" raw run, "LIT" literal char
    native: str  # native text this unit came from (for C/V/IV/S: the table key)


@dataclass
class Scheme:
    """A romanization scheme: native key -> Latin spelling, for consonants, vowels and signs."""

    name: str
    consonants: dict[str, str]
    vowels: dict[str, str]  # keyed by independent vowel char; spelling used both independent and as vowel sign
    signs: dict[str, str]
    separator: str = "_"
    _rev: dict[str, tuple[str, str]] = field(init=False, repr=False)
    _maxlen: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        errors = self.validate()
        if errors:
            raise ValueError(f"invalid scheme {self.name}: " + "; ".join(errors))
        self._rev = {}
        for kind, table in (("C", self.consonants), ("V", self.vowels), ("S", self.signs)):
            for native, sp in table.items():
                self._rev[sp] = (kind, native)
        self._maxlen = max(len(s) for s in self._rev)

    # ---------------------------------------------------------------- validation
    def validate(self) -> list[str]:
        errors = []
        reserved = {RAW_OPEN, RAW_CLOSE, RAW_ESC, DIGIT_DELIM, self.separator}
        spellings: dict[str, str] = {}
        for table in (self.consonants, self.vowels, self.signs):
            for native, sp in table.items():
                if not sp:
                    errors.append(f"empty spelling for {native!r}")
                elif any(c in reserved for c in sp):
                    errors.append(f"spelling {sp!r} for {native!r} uses a reserved char")
                elif any(c.isdigit() for c in sp):
                    errors.append(f"spelling {sp!r} for {native!r} contains a digit")
                elif sp in spellings:
                    errors.append(f"spelling {sp!r} used for both {spellings[sp]!r} and {native!r}")
                spellings[sp] = native
        if INHERENT_A not in self.vowels:
            errors.append("no spelling for the inherent vowel")
        if len(self.separator) != 1:
            errors.append("separator must be one character")
        return errors

    # ---------------------------------------------------------------- native -> units
    def _needs_raw(self, ch: str) -> bool:
        if ch.isascii() and ch.isalpha():
            return True
        if ch in (RAW_OPEN, RAW_CLOSE, RAW_ESC, DIGIT_DELIM, self.separator):
            return True
        if ch in self._rev:  # a literal that is itself a complete spelling would be decoded as that unit
            return True
        return is_kannada(ch)  # any Kannada char not handled as a unit (orphan signs, unmapped letters)

    def units(self, text: str) -> list[Unit]:
        out: list[Unit] = []
        i, n = 0, len(text)
        while i < n:
            ch = text[i]
            if ch in self.consonants or (i + 1 < n and text[i + 1] == NUKTA and ch + NUKTA in self.consonants):
                key, j = ch, i + 1
                if j < n and text[j] == NUKTA:
                    if ch + NUKTA in self.consonants:
                        key, j = ch + NUKTA, j + 1
                    else:  # consonant+nukta with no spelling: keep the whole cluster raw
                        j += 1
                        if j < n and (text[j] in MATRA_TO_VOWEL or text[j] == VIRAMA):
                            j += 1
                        out.append(Unit("RAW", text[i:j]))
                        i = j
                        continue
                out.append(Unit("C", key))
                if j < n and text[j] in MATRA_TO_VOWEL:
                    out.append(Unit("V", MATRA_TO_VOWEL[text[j]]))
                    j += 1
                elif j < n and text[j] == VIRAMA:
                    j += 1
                else:
                    out.append(Unit("V", INHERENT_A))
                i = j
            elif ch in self.vowels:
                out.append(Unit("IV", ch))
                i += 1
            elif ch in self.signs:
                out.append(Unit("S", ch))
                i += 1
            elif ch in KANNADA_DIGITS:
                j = i
                while j < n and text[j] in KANNADA_DIGITS:
                    j += 1
                out.append(Unit("DIG", text[i:j]))
                i = j
            elif self._needs_raw(ch):
                out.append(Unit("RAW", ch))
                i += 1
            else:
                out.append(Unit("LIT", ch))
                i += 1
        return _merge_raw(out)

    # ---------------------------------------------------------------- encode
    def _spell(self, u: Unit) -> str:
        if u.kind == "C":
            return self.consonants[u.native]
        if u.kind in ("V", "IV"):
            return self.vowels[u.native]
        if u.kind == "S":
            return self.signs[u.native]
        if u.kind == "DIG":
            return DIGIT_DELIM + "".join(KANNADA_DIGITS[c] for c in u.native) + DIGIT_DELIM
        if u.kind == "RAW":
            esc = u.native.replace(RAW_ESC, RAW_ESC * 2).replace(RAW_OPEN, RAW_ESC + RAW_OPEN)
            return RAW_OPEN + esc.replace(RAW_CLOSE, RAW_ESC + RAW_CLOSE) + RAW_CLOSE
        return u.native  # LIT

    def _match_len(self, text: str, pos: int) -> int:
        """Length of the longest spelling starting at pos (0 if none)."""
        for length in range(min(self._maxlen, len(text) - pos), 0, -1):
            if text[pos:pos + length] in self._rev:
                return length
        return 0

    def encode(self, text: str) -> str:
        buf = ""
        recent: list[tuple[int, int]] = []  # (start, expected match length) of recent spelling/literal tokens
        prev_kind = None
        for u in self.units(text):
            tok = self._spell(u)
            need_sep = u.kind == "IV" and prev_kind == "C"  # consonant with virama, then independent vowel
            if not need_sep and u.kind not in ("RAW", "DIG"):
                cand = buf + tok
                need_sep = any(self._match_len(cand, s) != L for s, L in recent if s + self._maxlen > len(buf))
            if need_sep:
                buf += self.separator
                recent = []
            if u.kind in ("RAW", "DIG"):
                recent = []  # delimiters are reserved, so nothing merges across a run
            else:
                recent.append((len(buf), len(tok) if u.kind != "LIT" else 0))
                recent = [(s, L) for s, L in recent if s + 2 * self._maxlen > len(buf)]
            buf += tok
            prev_kind = u.kind
        return buf

    # ---------------------------------------------------------------- decode
    def decode(self, text: str) -> str:
        out: list[str] = []
        pending: str | None = None  # consonant waiting to learn its vowel

        def flush() -> None:
            nonlocal pending
            if pending is not None:
                out.append(pending + VIRAMA)
                pending = None

        i, n = 0, len(text)
        while i < n:
            ch = text[i]
            if ch == RAW_OPEN:
                flush()
                j, buf = i + 1, []
                while j < n and text[j] != RAW_CLOSE:
                    if text[j] == RAW_ESC and j + 1 < n:
                        j += 1
                    buf.append(text[j])
                    j += 1
                if j >= n:
                    raise ValueError(f"unterminated raw run at {i}")
                out.append("".join(buf))
                i = j + 1
                continue
            if ch == DIGIT_DELIM:
                flush()
                j = text.index(DIGIT_DELIM, i + 1)
                out.append("".join(ASCII_TO_KANNADA_DIGIT[c] for c in text[i + 1:j]))
                i = j + 1
                continue
            if ch == self.separator:
                flush()
                i += 1
                continue
            length = self._match_len(text, i)
            if length == 0:
                flush()
                out.append(ch)
                i += 1
                continue
            kind, native = self._rev[text[i:i + length]]
            if kind == "C":
                flush()
                pending = native
            elif kind == "V":
                if pending is not None:
                    out.append(pending + VOWEL_TO_MATRA[native])
                    pending = None
                else:
                    out.append(native)
            else:
                flush()
                out.append(native)
            i += length
        flush()
        return "".join(out)

    def roundtrips(self, text: str) -> bool:
        return self.decode(self.encode(text)) == text


def _merge_raw(units: list[Unit]) -> list[Unit]:
    """Merge RAW runs separated only by spaces into one run ("{WhatsApp Web}" rather than "{WhatsApp} {Web}")."""
    out: list[Unit] = []
    for u in units:
        if u.kind == "RAW" and out and out[-1].kind == "RAW":
            out[-1] = Unit("RAW", out[-1].native + u.native)
        elif u.kind == "RAW" and len(out) >= 2 and out[-2].kind == "RAW" and all(
                x.kind == "LIT" and x.native == " " for x in out[-1:]):
            gap = out.pop()
            out[-1] = Unit("RAW", out[-1].native + gap.native + u.native)
        else:
            out.append(u)
    return out


# ---------------------------------------------------------------- ITRANS (ASCII, Dravidian e/E o/O convention)
ITRANS_CONSONANTS = {
    "ಕ": "k", "ಖ": "kh", "ಗ": "g", "ಘ": "gh", "ಙ": "~N",
    "ಚ": "ch", "ಛ": "Ch", "ಜ": "j", "ಝ": "jh", "ಞ": "~n",
    "ಟ": "T", "ಠ": "Th", "ಡ": "D", "ಢ": "Dh", "ಣ": "N",
    "ತ": "t", "ಥ": "th", "ದ": "d", "ಧ": "dh", "ನ": "n",
    "ಪ": "p", "ಫ": "ph", "ಬ": "b", "ಭ": "bh", "ಮ": "m",
    "ಯ": "y", "ರ": "r", "ಱ": "R", "ಲ": "l", "ಳ": "L", "ೞ": "zh", "ವ": "v",
    "ಶ": "sh", "ಷ": "Sh", "ಸ": "s", "ಹ": "h",
    "ಫ" + NUKTA: "f", "ಜ" + NUKTA: "z",
}
ITRANS_VOWELS = {
    "ಅ": "a", "ಆ": "A", "ಇ": "i", "ಈ": "I", "ಉ": "u", "ಊ": "U",
    "ಋ": "RRi", "ೠ": "RRI", "ಌ": "L^i", "ೡ": "L^I",  # L^i not LLi: LLi would collide with ಳ್ಳಿ (very common)
    "ಎ": "e", "ಏ": "E", "ಐ": "ai", "ಒ": "o", "ಓ": "O", "ಔ": "au",
}
ITRANS_SIGNS = {
    "ಂ": "M",   # anusvara
    "ಃ": "H",   # visarga
    "ಁ": ".N",  # candrabindu
    "ಽ": ".a",  # avagraha
    ZWNJ: "^",
    ZWJ: "^^",
    "।": "|",   # danda
    "॥": "||",  # double danda
}

ITRANS = Scheme("itrans", ITRANS_CONSONANTS, ITRANS_VOWELS, ITRANS_SIGNS)
