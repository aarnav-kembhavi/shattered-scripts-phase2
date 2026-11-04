"""Map whitespace words to token spans using fast-tokenizer offset mappings.

Works for byte-level BPE and SentencePiece byte-fallback tokenizers. When a token splits a character mid-UTF-8, all of
its byte pieces carry that character's offsets, so they are assigned to the same word. Offsets are trimmed of
whitespace before assignment, so a leading-space token (" ಕ") belongs to the word it starts, and a bare space or "▁"
token belongs to no word.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class WordSpan:
    word: str
    char_start: int
    char_end: int
    tok_start: int  # first token index (inclusive)
    tok_end: int    # last token index + 1
    shares_token: bool  # True if a boundary token also covers another word

    @property
    def last_token(self) -> int:
        return self.tok_end - 1

    @property
    def n_tokens(self) -> int:
        return self.tok_end - self.tok_start


def word_spans(text: str, offsets: list[tuple[int, int]], word_pattern: str = r"\S+",
               char_range: tuple[int, int] | None = None) -> list[WordSpan]:
    """Token span of every word in `text` matching `word_pattern` (within `char_range` if given).

    Words that no token covers (impossible for a correct tokenizer) are omitted.
    """
    lo, hi = char_range or (0, len(text))
    words = [m for m in re.finditer(word_pattern, text) if m.start() >= lo and m.end() <= hi]
    char_to_word = {}
    for wi, m in enumerate(words):
        for c in range(m.start(), m.end()):
            char_to_word[c] = wi
    first: dict[int, int] = {}
    last: dict[int, int] = {}
    token_words: list[set[int]] = []
    for ti, (a, b) in enumerate(offsets):
        while a < b and text[a].isspace():
            a += 1
        while b > a and text[b - 1].isspace():
            b -= 1
        ws = {char_to_word[c] for c in range(a, b) if c in char_to_word}
        token_words.append(ws)
        for wi in ws:
            first.setdefault(wi, ti)
            last[wi] = ti
    spans = []
    for wi, m in enumerate(words):
        if wi not in first:
            continue
        s, e = first[wi], last[wi] + 1
        shared = len(token_words[s]) > 1 or len(token_words[e - 1]) > 1
        spans.append(WordSpan(m.group(), m.start(), m.end(), s, e, shared))
    return spans


def tokenize_with_words(tokenizer, text: str, word_pattern: str = r"\S+",
                        char_range: tuple[int, int] | None = None, add_special_tokens: bool = True):
    """Tokenize with a HF fast tokenizer; return (input_ids, word spans)."""
    if not getattr(tokenizer, "is_fast", False):
        raise ValueError("word alignment needs a fast tokenizer (offset mappings)")
    enc = tokenizer(text, return_offsets_mapping=True, add_special_tokens=add_special_tokens)
    return enc["input_ids"], word_spans(text, enc["offset_mapping"], word_pattern, char_range)
