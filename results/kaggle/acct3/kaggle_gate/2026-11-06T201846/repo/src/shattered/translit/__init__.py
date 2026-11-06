"""Kannada transliteration: lossless ITRANS (ASCII), controlled lossy romanization, round-trip checks."""
from .lossy import LossyBackMapper, char_error_rate, to_lossy
from .scheme import ITRANS, Scheme


def to_itrans(text: str) -> str:
    return ITRANS.encode(text)


def from_itrans(text: str) -> str:
    return ITRANS.decode(text)


__all__ = ["ITRANS", "Scheme", "to_itrans", "from_itrans", "to_lossy", "LossyBackMapper", "char_error_rate"]
