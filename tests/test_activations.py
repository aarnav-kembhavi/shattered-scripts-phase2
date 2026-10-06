import pytest
import torch

from shattered.interp.activations import ActivationCache

transformers = pytest.importorskip("transformers")


@pytest.fixture(scope="module")
def tiny():
    try:
        tok = transformers.AutoTokenizer.from_pretrained("openai-community/gpt2")
    except OSError:
        pytest.skip("gpt2 tokenizer unavailable")
    torch.manual_seed(0)
    cfg = transformers.GPT2Config(n_layer=2, n_embd=32, n_head=2, vocab_size=tok.vocab_size, n_positions=256)
    model = transformers.GPT2LMHeadModel(cfg).eval()
    return model, tok


def test_cache_shape_and_reuse(tiny, tmp_path):
    model, tok = tiny
    cache = ActivationCache("tiny-gpt2", root=tmp_path)
    acts, meta = cache.get(model, tok, "ಕನ್ನಡ ಭಾಷೆ", "native", "item1")
    assert acts.shape == (3, len(meta["input_ids"]), 32) and acts.dtype == torch.float16
    acts2, _ = cache.get(model, tok, "ಕನ್ನಡ ಭಾಷೆ", "native", "item1")
    assert cache.n_forward == 1 and torch.equal(acts, acts2)


def test_cache_selected_positions_match_full(tiny, tmp_path):
    model, tok = tiny
    cache = ActivationCache("tiny-gpt2", root=tmp_path)
    full, _ = cache.get(model, tok, "hello brave new world", "en", "x")
    sel, meta = cache.get(model, tok, "hello brave new world", "en", "x",
                          positions=lambda ids, enc: [0, len(ids) - 1], pos_tag="first_last")
    assert meta["positions"] == [0, full.shape[1] - 1]
    assert torch.equal(sel, full[:, [0, -1]])
    assert cache.n_forward == 2  # different pos_tag -> separate entry
