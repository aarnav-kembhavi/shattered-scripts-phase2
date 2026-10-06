"""Reversible romanization schemes for Brahmic scripts (Kannada first; also Tamil, Telugu, Malayalam, Hindi, Bangla).

A scheme maps a script's units (consonants, vowels, signs) to Latin spellings. The encoder inserts a separator wherever
greedy longest-match decoding would otherwise mis-segment, so any scheme that passes `Scheme.validate()` round-trips
exactly. ITRANS is one such scheme; E9 searches over others with the same engine.

Romanized text grammar (for a scheme with separator "_"):
  - spelling tokens, decoded by longest match. A consonant token directly followed by a vowel token takes that vowel
    as its vowel sign; a consonant token followed by anything else gets a virama.
  - "_" separator: decodes to nothing; it only breaks a merge or a consonant-vowel attachment.
  - "{...}" raw run: copied verbatim (inside, "{", "}" and "\\" are backslash-escaped). Used for Latin letters and any
    character that would otherwise be read as a spelling or delimiter.
  - "#...#" native digit run, written with ASCII digits. ASCII digits in the source pass through unchanged.
  - any other character is a literal.

Inputs are expected to be NFC-normalized (experiments normalize first); non-NFC sequences still round-trip, but via
raw runs.
"""
from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field

ZWNJ = "‌"
ZWJ = "‍"
RAW_OPEN, RAW_CLOSE, RAW_ESC, DIGIT_DELIM = "{", "}", "\\", "#"


@dataclass(frozen=True)
class Script:
    """Script-specific code points the engine needs."""

    name: str              # Unicode name prefix, e.g. "KANNADA"
    base: int              # start of the Unicode block
    virama: str
    nukta: str | None
    inherent: str          # independent letter A, key for the inherent vowel
    matra_to_vowel: dict   # dependent vowel sign -> vowel key (normally the independent vowel)
    digits: dict           # native digit -> ASCII digit

    @property
    def vowel_to_matra(self) -> dict:
        d = {v: m for m, v in self.matra_to_vowel.items()}
        d[self.inherent] = ""
        return d

    @property
    def ascii_to_digit(self) -> dict:
        return {v: k for k, v in self.digits.items()}

    def in_block(self, ch: str) -> bool:
        return self.base <= ord(ch) < self.base + 0x80


def _char(base: int, offset: int, prefix: str, suffix: str) -> str | None:
    """Character at base+offset if its Unicode name is '<prefix> <suffix>'."""
    c = chr(base + offset)
    return c if unicodedata.name(c, "") == f"{prefix} {suffix}" else None


def make_script(prefix: str, base: int, extra_matras: dict | None = None) -> Script:
    """Build a Script; each vowel sign 'X VOWEL SIGN Y' maps to the letter 'X LETTER Y'."""
    by_name = {unicodedata.name(chr(base + o), ""): chr(base + o) for o in range(0x80)}
    sign_prefix = f"{prefix} VOWEL SIGN "
    matras = {ch: by_name[f"{prefix} LETTER {name[len(sign_prefix):]}"] for name, ch in by_name.items()
              if name.startswith(sign_prefix) and f"{prefix} LETTER {name[len(sign_prefix):]}" in by_name}
    matras.update(extra_matras or {})
    digits = {chr(base + 0x66 + d): str(d) for d in range(10)}
    return Script(prefix, base, chr(base + 0x4D), _char(base, 0x3C, prefix, "SIGN NUKTA"), chr(base + 0x05),
                  matras, digits)


KANNADA = make_script("KANNADA", 0x0C80)
TAMIL = make_script("TAMIL", 0x0B80)
TELUGU = make_script("TELUGU", 0x0C00)
MALAYALAM = make_script("MALAYALAM", 0x0D00, {"ൗ": "ഔ", "ൌ": "ൌ"})  # see MALAYALAM overrides
DEVANAGARI = make_script("DEVANAGARI", 0x0900)
BENGALI = make_script("BENGALI", 0x0980)

# Back-compatible Kannada constants
VIRAMA = KANNADA.virama
NUKTA = KANNADA.nukta
INHERENT_A = KANNADA.inherent
MATRA_TO_VOWEL = KANNADA.matra_to_vowel
VOWEL_TO_MATRA = KANNADA.vowel_to_matra
KANNADA_DIGITS = KANNADA.digits


@dataclass(frozen=True)
class Unit:
    kind: str  # "C" consonant, "V" vowel attached to preceding C, "IV" independent vowel, "S" sign,
    #            "DIG" native digit run, "RAW" raw run, "LIT" literal char
    native: str  # native text this unit came from (for C/V/IV/S: the table key)


@dataclass
class Scheme:
    """A romanization scheme: native key -> Latin spelling, for consonants, vowels and signs."""

    name: str
    consonants: dict[str, str]
    vowels: dict[str, str]  # keyed by vowel key; spelling used both independent and as vowel sign
    signs: dict[str, str]
    separator: str = "_"
    script: Script = KANNADA
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
        self._v2m = self.script.vowel_to_matra
        self._a2d = self.script.ascii_to_digit

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
        if self.script.inherent not in self.vowels:
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
        return self.script.in_block(ch)  # any script char not handled as a unit (orphan signs, unmapped letters)

    def units(self, text: str) -> list[Unit]:
        sc = self.script
        nukta, virama, m2v, digits = sc.nukta, sc.virama, sc.matra_to_vowel, sc.digits
        out: list[Unit] = []
        i, n = 0, len(text)
        while i < n:
            ch = text[i]
            has_nukta = nukta is not None and i + 1 < n and text[i + 1] == nukta
            if ch in self.consonants or (has_nukta and ch + nukta in self.consonants):
                key, j = ch, i + 1
                if has_nukta:
                    if ch + nukta in self.consonants:
                        key, j = ch + nukta, j + 1
                    else:  # consonant+nukta with no spelling: keep the whole cluster raw
                        j += 1
                        if j < n and (text[j] in m2v or text[j] == virama):
                            j += 1
                        out.append(Unit("RAW", text[i:j]))
                        i = j
                        continue
                out.append(Unit("C", key))
                if j < n and text[j] in m2v:
                    out.append(Unit("V", m2v[text[j]]))
                    j += 1
                elif j < n and text[j] == virama:
                    j += 1
                else:
                    out.append(Unit("V", sc.inherent))
                i = j
            elif ch in self.vowels:
                out.append(Unit("IV", ch))
                i += 1
            elif ch in self.signs:
                out.append(Unit("S", ch))
                i += 1
            elif ch in digits:
                j = i
                while j < n and text[j] in digits:
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
            return DIGIT_DELIM + "".join(self.script.digits[c] for c in u.native) + DIGIT_DELIM
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
        toks: list[str] = []
        kinds: list[str] = []
        for u in self.units(text):
            if u.kind == "IV" and kinds and kinds[-1] == "C":  # consonant with virama, then independent vowel
                toks.append(self.separator)
                kinds.append("SEP")
            toks.append(self._spell(u))
            kinds.append(u.kind)
            if u.kind not in ("RAW", "DIG"):
                self._fix_tail(toks, kinds)
        return "".join(toks)

    def _fix_tail(self, toks: list[str], kinds: list[str]) -> None:
        """Insert separators so greedy longest-match decoding of the tail reproduces the intended tokens.

        Delimiters (separator, raw and digit runs) are reserved characters, so no spelling spans them; tokens further
        back than 2 * maxlen characters cannot be affected by the newly appended token.
        """
        for _ in range(16):
            w, length = len(toks) - 1, len(toks[-1])
            while w > 0 and kinds[w - 1] not in ("SEP", "RAW", "DIG") and length < 2 * self._maxlen:
                w -= 1
                length += len(toks[w])
            window = "".join(toks[w:])
            pos, bad = 0, None
            for i in range(w, len(toks)):
                expected = 0 if kinds[i] == "LIT" else len(toks[i])
                if self._match_len(window, pos) != expected:
                    bad = i
                    break
                pos += len(toks[i])
            if bad is None:
                return
            # separate right after the token that was over-read, but never between a consonant and its vowel sign
            for b in range(bad + 1, len(toks)):
                if not (kinds[b - 1] == "C" and kinds[b] == "V"):
                    toks.insert(b, self.separator)
                    kinds.insert(b, "SEP")
                    break
            else:
                raise ValueError(f"scheme {self.name}: cannot separate {window!r}")
        raise ValueError(f"scheme {self.name}: separator insertion did not converge")

    # ---------------------------------------------------------------- decode
    def decode(self, text: str) -> str:
        out: list[str] = []
        pending: str | None = None  # consonant waiting to learn its vowel
        virama = self.script.virama

        def flush() -> None:
            nonlocal pending
            if pending is not None:
                out.append(pending + virama)
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
                out.append("".join(self._a2d[c] for c in text[i + 1:j]))
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
                    out.append(pending + self._v2m[native])
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
        elif (u.kind == "RAW" and len(out) >= 2 and out[-2].kind == "RAW" and out[-1].kind == "LIT"
              and out[-1].native == " "):
            gap = out.pop()
            out[-1] = Unit("RAW", out[-1].native + gap.native + u.native)
        else:
            out.append(u)
    return out


# ---------------------------------------------------------------- ITRANS (ASCII, Dravidian e/E o/O convention)
NUKTA_KN = "಼"
ITRANS_CONSONANTS = {
    "ಕ": "k", "ಖ": "kh", "ಗ": "g", "ಘ": "gh", "ಙ": "~N",
    "ಚ": "ch", "ಛ": "Ch", "ಜ": "j", "ಝ": "jh", "ಞ": "~n",
    "ಟ": "T", "ಠ": "Th", "ಡ": "D", "ಢ": "Dh", "ಣ": "N",
    "ತ": "t", "ಥ": "th", "ದ": "d", "ಧ": "dh", "ನ": "n",
    "ಪ": "p", "ಫ": "ph", "ಬ": "b", "ಭ": "bh", "ಮ": "m",
    "ಯ": "y", "ರ": "r", "ಱ": "R", "ಲ": "l", "ಳ": "L", "ೞ": "zh", "ವ": "v",
    "ಶ": "sh", "ಷ": "Sh", "ಸ": "s", "ಹ": "h",
    "ಫ" + NUKTA_KN: "f", "ಜ" + NUKTA_KN: "z",
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


def _project(text: str, script: Script) -> str | None:
    """Map Kannada characters to the same-named characters of `script` (None if any has no counterpart)."""
    out = []
    for ch in text:
        if not KANNADA.in_block(ch):
            out.append(ch)
            continue
        suffix = unicodedata.name(ch)[len("KANNADA "):]
        if suffix == "LETTER FA":  # Unicode calls ೞ "FA"; it is the retroflex approximant, handled by overrides
            return None
        c = _char(script.base, ord(ch) - KANNADA.base, script.name, suffix)
        if c is None:
            return None
        out.append(c)
    return "".join(out)


# Script-specific ITRANS entries: {table: {native: spelling or None to delete}}
_OVERRIDES = {
    "TAMIL": {"consonants": {"ன": "n~", "ழ": "zh"}},  # ன, ழ
    "TELUGU": {"consonants": {"ఴ": "zh"}},
    "MALAYALAM": {
        "consonants": {"ഩ": "n^", "ഴ": "zh"},  # ഩ, ഴ
        # ൗ (U+0D57, au length mark used alone as the au sign) is far more common in FLORES than ൌ (U+0D4C), so it
        # gets the plain "au" via the matra map; ൌ becomes a pseudo-vowel spelled "au~".
        "vowels": {"ൌ": "au~"},
        "signs": {"ൺ": "N~", "ൻ": "n~", "ർ": "r~", "ൽ": "l~", "ൾ": "L~", "ൿ": "k~",
                  "ൔ": "m~", "ൕ": "y~", "ൖ": "zh~", "ൎ": "r^"},  # chillus, dot reph
    },
    "DEVANAGARI": {
        # Hindi has no short/long e,o contrast: plain e/o for the common letters; the rare short forms get e~/o~.
        "vowels": {"ए": "e", "ओ": "o", "ऎ": "e~", "ऒ": "o~", "ऍ": "E", "ऑ": "O"},
        "consonants": {"क़": "q", "ख़": "K", "ग़": "G", "ड़": ".D",
                       "ढ़": ".Dh", "य़": "Y", "ळ": "L", "ऴ": "zh"},
        "signs": {"ॐ": "OM"},
    },
    "BENGALI": {
        "vowels": {"এ": "e", "ও": "o"},
        "consonants": {"ড়": ".D", "ঢ়": ".Dh", "য়": "Y"},
        "signs": {"ৎ": "t~"},  # khanda ta
    },
}


def itrans_for(script: Script) -> Scheme:
    """ITRANS scheme for `script`, projected from the Kannada tables by Unicode name, plus script overrides."""
    if script is KANNADA:
        return ITRANS
    tables = {}
    for tname, table in (("consonants", ITRANS_CONSONANTS), ("vowels", ITRANS_VOWELS), ("signs", ITRANS_SIGNS)):
        proj = {}
        for k, sp in table.items():
            pk = _project(k, script)
            if pk is not None:
                proj[pk] = sp
        for k, sp in _OVERRIDES.get(script.name, {}).get(tname, {}).items():
            proj = {pk: s for pk, s in proj.items() if not (s == sp and pk != k)}  # override wins the spelling
            if sp is None:
                proj.pop(k, None)
            else:
                proj[k] = sp
        tables[tname] = proj
    return Scheme(f"itrans-{script.name.lower()}", tables["consonants"], tables["vowels"], tables["signs"],
                  script=script)


SCRIPTS = {"kan_Knda": KANNADA, "tam_Taml": TAMIL, "tel_Telu": TELUGU, "mal_Mlym": MALAYALAM,
           "hin_Deva": DEVANAGARI, "ben_Beng": BENGALI}
