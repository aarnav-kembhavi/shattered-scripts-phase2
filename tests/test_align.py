import pytest

from shattered.tok.align import tokenize_with_words, word_spans

KN = "ಬೆಂಗಳೂರು ಕರ್ನಾಟಕದ ರಾಜಧಾನಿ. Hello world"


def test_word_spans_mid_character_split():
    # "ಕನ" split into byte pieces: 3 tokens for ಕ, 2 for ನ (all carrying the char's offsets), then a space token
    text = "ಕನ ಅ"
    offsets = [(0, 1), (0, 1), (0, 1), (1, 2), (1, 2), (2, 3), (3, 4)]
    spans = word_spans(text, offsets)
    assert [(s.word, s.tok_start, s.tok_end) for s in spans] == [("ಕನ", 0, 5), ("ಅ", 6, 7)]
    assert not any(s.shares_token for s in spans)


def test_word_spans_leading_space_and_special_tokens():
    text = "ab cd"
    offsets = [(0, 0), (0, 2), (2, 5), (0, 0)]  # BOS, "ab", " cd", EOS
    spans = word_spans(text, offsets)
    assert [(s.word, s.tok_start, s.tok_end) for s in spans] == [("ab", 1, 2), ("cd", 2, 3)]


def test_word_spans_shared_token_and_char_range():
    text = "a.b c"
    spans = word_spans(text, [(0, 3), (3, 5)], word_pattern=r"\w+")
    assert [(s.word, s.tok_start, s.tok_end, s.shares_token) for s in spans] == [
        ("a", 0, 1, True), ("b", 0, 1, True), ("c", 1, 2, False)]
    assert [s.word for s in word_spans(text, [(0, 3), (3, 5)], char_range=(4, 5))] == ["c"]


TOKENIZERS = ["openai-community/gpt2", "TinyLlama/TinyLlama-1.1B-Chat-v1.0", "Qwen/Qwen2.5-0.5B-Instruct"]


@pytest.mark.parametrize("name", TOKENIZERS)
def test_real_tokenizers_cover_every_token_of_each_word(name):
    transformers = pytest.importorskip("transformers")
    try:
        tok = transformers.AutoTokenizer.from_pretrained(name)
    except OSError:
        pytest.skip(f"cannot load {name}")
    ids, spans = tokenize_with_words(tok, KN, add_special_tokens=False)
    assert [s.word for s in spans] == KN.split()
    # spans are disjoint, ordered, and decoding each span gives back the word (modulo surrounding whitespace)
    for a, b in zip(spans, spans[1:]):
        assert a.tok_end <= b.tok_start
    for s in spans:
        assert tok.decode(ids[s.tok_start:s.tok_end]).strip() == s.word
    # Kannada is fragmented: the first word needs many tokens under every one of these tokenizers
    assert spans[0].n_tokens >= 5
