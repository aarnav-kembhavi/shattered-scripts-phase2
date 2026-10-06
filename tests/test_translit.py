import glob

import pytest

from shattered.translit import ITRANS, LossyBackMapper, Scheme, char_error_rate, from_itrans, to_itrans, to_lossy
from shattered.translit.scheme import ITRANS_CONSONANTS, ITRANS_SIGNS, ITRANS_VOWELS

KNOWN = [
    ("ಎ ಏ ಕೆ ಕೇ ಒ ಓ ಕೊ ಕೋ", "e E ke kE o O ko kO"),          # short vs long e/o
    ("ಐ ಔ ಕೈ ಕೌ", "ai au kai kau"),
    ("ಬಾಳೆ ಹಳ್ಳಿ", "bALe haLLi"),                            # retroflex lateral; ಳ್ಳಿ must not read as vocalic L
    ("ೞ ಱ", "zha Ra"),
    ("ಫ಼ ಜ಼", "fa za"),                                      # nukta
    ("ಸಂತೋಷ ದುಃಖ", "saMtOSha duHkha"),
    ("ಸ್ತ್ರೀ ಕ್ಷೇತ್ರ ಜ್ಞಾನ", "strI kShEtra j~nAna"),
    ("ಮತ್", "mat"),
    ("ಬೆಂಗಳೂರು ಕರ್ನಾಟಕದ ರಾಜಧಾನಿ.", "beMgaLUru karnATakada rAjadhAni."),  # '.' must stay '.', not danda
    ("೦೧೨೩ 2024", "#0123# 2024"),                             # Kannada digits marked; ASCII digits pass through
    ("ಇದು WhatsApp Web", "idu {WhatsApp Web}"),               # Latin escaped as one raw run
]

AMBIGUOUS = [
    "ಅಇ ಕಇ ಅಉ ಕಅ",              # hiatus vs diphthong
    "ಕ್ಹ ಗ್ಹ ಸ್ಹ ನ್ಗ",          # C+virama+h vs aspirate
    "ಮತ್ಅ",                     # virama then independent vowel
    "ಸರಿ.ಅದು ಸರಿ.ಣ",           # '.' followed by avagraha/candrabindu prefixes
    "ಳ್‌ಇ",                # ZWNJ followed by i (L^i collision)
    "ಕ್‍ಷ ಕ್‌ಷ",
    "।। ॥",
    r"{x} #1 a_b \ | ^ ~",       # reserved characters in the source
    "ಕಁ ಽ ಋಷಿ ೠ ಌ ೡ",
    "್ಕ ಾಕ ಕೕ",   # orphan virama / vowel sign / length mark
    "ಡ಼ ಡ಼ಿ",                   # nukta on a consonant without a spelling
    "",
]


@pytest.mark.parametrize("native,itrans", KNOWN)
def test_known_itrans(native, itrans):
    assert to_itrans(native) == itrans
    assert from_itrans(itrans) == native


@pytest.mark.parametrize("native", AMBIGUOUS)
def test_ambiguous_round_trip(native):
    assert from_itrans(to_itrans(native)) == native


def test_itrans_is_ascii_for_kannada_text():
    s = "ಬೆಂಗಳೂರು ಕರ್ನಾಟಕದ ರಾಜಧಾನಿ. ಕೆ ಒ ೧೨"
    assert to_itrans(s).isascii()


def test_scheme_validation_rejects_duplicates_and_reserved():
    with pytest.raises(ValueError):
        Scheme("dup", {**ITRANS_CONSONANTS, "ಕ": "g"}, ITRANS_VOWELS, ITRANS_SIGNS)
    with pytest.raises(ValueError):
        Scheme("res", {**ITRANS_CONSONANTS, "ಕ": "k_"}, ITRANS_VOWELS, ITRANS_SIGNS)


def test_alternative_scheme_round_trips():
    """A deliberately collision-heavy scheme still round-trips because the encoder inserts separators."""
    cons = {**ITRANS_CONSONANTS, "ಖ": "k", "ಕ": "kk"}  # 'k'+'k' collides with 'kk'
    vow = {**ITRANS_VOWELS, "ಆ": "aa"}               # 'a'+'a' collides with 'aa'
    s = Scheme("weird", cons, vow, ITRANS_SIGNS)
    for t in ["ಖ್ಖ ಕ ಕಅ ಖಆ ಅಅ", "ಕನ್ನಡ ಖಾಸಗಿ"]:
        assert s.decode(s.encode(t)) == t


def test_lossy_rules():
    assert to_lossy("ಕೇಳು") == "kelu"          # long e -> short, retroflex L -> l
    assert to_lossy("ಭಾರತ") == "barata"        # aspirate -> plain, long a -> short
    assert to_lossy("ಕಂಬ ಸಂತೋಷ") == "kamba santosha"  # anusvara m before labial, n otherwise
    assert to_lossy("ಇದು WhatsApp ೨೦") == "idu WhatsApp 20"


def test_lossy_back_mapper_and_cer():
    corpus = ["ಕಳ ಕಳ ಕಲ", "ಬಾಳೆ"]
    bm = LossyBackMapper().fit(corpus)
    assert bm.invert(to_lossy("ಕಳ ಬಾಳೆ")) == "ಕಳ ಬಾಳೆ"   # most frequent source wins
    assert bm.invert(to_lossy("ಕಲ")) == "ಕಳ"              # ...so the minority form is lost
    assert char_error_rate("ಕಳ", "ಕಲ") == 0.5
    assert char_error_rate("abc", "abc") == 0.0


WIKI = glob.glob("data/raw/wikipedia_kn/**/*.parquet", recursive=True)


@pytest.mark.skipif(not WIKI, reason="Kannada Wikipedia not downloaded")
def test_wikipedia_sample_round_trip():
    import pyarrow.parquet as pq
    texts = pq.read_table(WIKI[0], columns=["text"]).column("text").to_pylist()[::60]  # ~520 articles
    bad = [t for t in texts if not ITRANS.roundtrips(t)]
    assert not bad, f"{len(bad)} articles fail round trip"
