"""Tiny GPT for E5: pre-LN transformer with RoPE (no learned positions, so parameter count does not depend on context
length), tied input/output embeddings, optional factorized embedding (to equalize embedding parameters across
vocabulary sizes as a sensitivity check)."""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class GPTConfig:
    vocab_size: int
    n_layer: int = 8
    d_model: int = 384
    n_head: int = 6
    mlp_mult: int = 4
    max_ctx: int = 1024
    emb_dim: int | None = None  # None = untied-dim embedding (d_model); else factorized V x emb_dim -> d_model
    rope_base: float = 10000.0

    def to_dict(self) -> dict:
        return asdict(self)


def _rope_cache(ctx: int, head_dim: int, base: float, device) -> tuple[torch.Tensor, torch.Tensor]:
    inv = 1.0 / (base ** (torch.arange(0, head_dim, 2, device=device).float() / head_dim))
    t = torch.arange(ctx, device=device).float()
    freqs = torch.outer(t, inv)
    return freqs.cos(), freqs.sin()


def _apply_rope(x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
    # x: [B, H, T, Dh]
    x1, x2 = x[..., 0::2], x[..., 1::2]
    T = x.shape[-2]
    c, s = cos[:T].to(x.dtype), sin[:T].to(x.dtype)
    out = torch.stack((x1 * c - x2 * s, x1 * s + x2 * c), dim=-1)
    return out.flatten(-2)


class Block(nn.Module):
    def __init__(self, cfg: GPTConfig) -> None:
        super().__init__()
        d = cfg.d_model
        self.n_head = cfg.n_head
        self.ln1 = nn.LayerNorm(d, bias=False)
        self.qkv = nn.Linear(d, 3 * d, bias=False)
        self.proj = nn.Linear(d, d, bias=False)
        self.ln2 = nn.LayerNorm(d, bias=False)
        self.fc = nn.Linear(d, cfg.mlp_mult * d, bias=False)
        self.fc_out = nn.Linear(cfg.mlp_mult * d, d, bias=False)

    def forward(self, x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor,
                attn_hook=None) -> torch.Tensor:
        B, T, D = x.shape
        q, k, v = self.qkv(self.ln1(x)).split(D, dim=-1)
        q, k, v = (t.view(B, T, self.n_head, D // self.n_head).transpose(1, 2) for t in (q, k, v))
        q, k = _apply_rope(q, cos, sin), _apply_rope(k, cos, sin)
        if attn_hook is None:
            y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        else:  # explicit attention (for head analysis / ablation); attn_hook(probs) may return modified probs
            att = (q @ k.transpose(-2, -1)) / math.sqrt(q.shape[-1])
            att = att.masked_fill(torch.triu(torch.ones(T, T, dtype=torch.bool, device=x.device), 1), float("-inf"))
            probs = attn_hook(att.softmax(-1))
            y = probs @ v
        x = x + self.proj(y.transpose(1, 2).reshape(B, T, D))
        return x + self.fc_out(F.gelu(self.fc(self.ln2(x))))


class GPT(nn.Module):
    def __init__(self, cfg: GPTConfig) -> None:
        super().__init__()
        self.cfg = cfg
        e = cfg.emb_dim or cfg.d_model
        self.wte = nn.Embedding(cfg.vocab_size, e)
        self.emb_proj = nn.Linear(e, cfg.d_model, bias=False) if cfg.emb_dim else None
        self.unemb_proj = nn.Linear(cfg.d_model, e, bias=False) if cfg.emb_dim else None
        self.blocks = nn.ModuleList(Block(cfg) for _ in range(cfg.n_layer))
        self.ln_f = nn.LayerNorm(cfg.d_model, bias=False)
        cos, sin = _rope_cache(cfg.max_ctx, cfg.d_model // cfg.n_head, cfg.rope_base, "cpu")
        self.register_buffer("rope_cos", cos, persistent=False)
        self.register_buffer("rope_sin", sin, persistent=False)
        self.apply(self._init)
        for name, p in self.named_parameters():
            if name.endswith("proj.weight") and "emb" not in name or name.endswith("fc_out.weight"):
                nn.init.normal_(p, std=0.02 / math.sqrt(2 * cfg.n_layer))

    @staticmethod
    def _init(m: nn.Module) -> None:
        if isinstance(m, (nn.Linear, nn.Embedding)):
            nn.init.normal_(m.weight, std=0.02)

    def param_counts(self) -> dict:
        emb = sum(p.numel() for n, p in self.named_parameters() if n.startswith(("wte", "emb_proj", "unemb_proj")))
        total = sum(p.numel() for p in self.parameters())
        return {"total": total, "embedding": emb, "non_embedding": total - emb}

    def forward(self, idx: torch.Tensor, targets: torch.Tensor | None = None, return_hidden: bool = False,
                attn_hooks: dict | None = None):
        x = self.wte(idx)
        if self.emb_proj is not None:
            x = self.emb_proj(x)
        hidden = [x] if return_hidden else None
        for i, blk in enumerate(self.blocks):
            x = blk(x, self.rope_cos, self.rope_sin, (attn_hooks or {}).get(i))
            if return_hidden:
                hidden.append(x)
        h = self.ln_f(x)
        if self.unemb_proj is not None:
            h = self.unemb_proj(h)
        logits = h @ self.wte.weight.T
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.float().view(-1, logits.size(-1)), targets.view(-1), reduction="sum")
        return logits, loss, hidden


def train_flops_per_token(cfg: GPTConfig, ctx: int, non_embedding: int) -> float:
    """Approximate training FLOPs per token: 6 * (matmul params incl. unembedding) + causal attention scores."""
    e = cfg.emb_dim or cfg.d_model
    unemb = cfg.vocab_size * e + (2 * cfg.d_model * e if cfg.emb_dim else 0)
    attn = 6 * cfg.n_layer * ctx * cfg.d_model  # QK^T and AV, fwd+bwd, causal (half of 12*L*ctx*d)
    return 6 * (non_embedding + unemb) + attn
