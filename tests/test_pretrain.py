import numpy as np
import torch

from shattered.pretrain.model import GPT, GPTConfig
from shattered.pretrain.train import _lr, context_tokens, eval_bpb


def test_gpt_shapes_hidden_and_params():
    cfg = GPTConfig(vocab_size=300, n_layer=2, d_model=32, n_head=4, max_ctx=16)
    m = GPT(cfg)
    x = torch.randint(0, 300, (3, 16))
    logits, loss, hidden = m(x, x, return_hidden=True)
    assert logits.shape == (3, 16, 300) and len(hidden) == 3 and loss.item() > 0
    pc = m.param_counts()
    assert pc["embedding"] == 300 * 32 and pc["total"] == pc["embedding"] + pc["non_embedding"]
    # non-embedding params do not depend on the vocabulary
    assert GPT(GPTConfig(vocab_size=5000, n_layer=2, d_model=32, n_head=4)).param_counts()["non_embedding"] == \
        pc["non_embedding"]


def test_factorized_embedding_equalizes_params():
    a = GPT(GPTConfig(vocab_size=257, n_layer=1, d_model=32, n_head=4, emb_dim=8)).param_counts()
    b = GPT(GPTConfig(vocab_size=16385, n_layer=1, d_model=32, n_head=4, emb_dim=8)).param_counts()
    assert b["embedding"] - a["embedding"] == (16385 - 257) * 8


def test_causality():
    torch.manual_seed(0)
    m = GPT(GPTConfig(vocab_size=50, n_layer=2, d_model=32, n_head=4, max_ctx=8)).eval()
    x = torch.randint(0, 50, (1, 8))
    y = x.clone()
    y[0, -1] = (y[0, -1] + 1) % 50
    a, _, _ = m(x)
    b, _, _ = m(y)
    assert torch.allclose(a[0, :-1], b[0, :-1], atol=1e-5)


def test_context_and_lr_schedule():
    assert context_tokens(1024, 1.0) == 1024
    assert context_tokens(1024, 4.2) == 240
    assert _lr(0, 100, 1.0, 0.1, 0.1) == 0.1
    assert abs(_lr(99, 100, 1.0, 0.1, 0.1) - 0.1) < 1e-3


def test_eval_bpb_uniform_model():
    """A model with zero logits predicts uniformly: BPB = log2(V) * tokens / bytes."""
    cfg = GPTConfig(vocab_size=16, n_layer=1, d_model=16, n_head=2, max_ctx=8)
    m = GPT(cfg)
    for p in m.parameters():
        torch.nn.init.zeros_(p)
    stream = np.arange(65, dtype=np.uint16) % 16
    bpb = eval_bpb(m, stream, n_bytes=128, ctx=8, device="cpu")
    assert abs(bpb - 4 * 64 / 128) < 1e-2


def test_minimal_pairs_well_formed():
    from shattered.pretrain.evals import minimal_pairs
    pairs = minimal_pairs()
    assert {p["phenomenon"] for p in pairs} == {"subject_verb_agreement_singular", "subject_verb_agreement_plural",
                                                "determiner_noun_agreement", "irregular_past"}
    for p in pairs:
        g, b = p["good"].split(), p["bad"].split()
        assert len(g) == len(b) and sum(x != y for x, y in zip(g, b)) == 1
