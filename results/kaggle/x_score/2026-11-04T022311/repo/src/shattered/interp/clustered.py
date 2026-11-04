"""Bootstrap resampling by multinomial reweighting, either over items (occurrences, sentences) or clustered over
groups (words: a resampled word brings all its occurrences). Used for detok-layer and alignment-layer CIs.

Detok / alignment layer = first layer whose curve reaches `frac` of the curve's maximum.
"""
from __future__ import annotations

import numpy as np

B, CHUNK, FRAC = 10_000, 500, 0.9


def first_reach(curves: np.ndarray, frac: float = FRAC) -> np.ndarray:
    """curves [..., L+1] -> first layer index reaching frac * max along the last axis."""
    return np.argmax(curves >= frac * curves.max(-1, keepdims=True), axis=-1)


def weights(n: int, seed: int, groups: np.ndarray | None = None, n_boot: int = B):
    """Yields resample-count matrices [chunk, n] over n items. With `groups` (int label per item), groups are
    resampled with replacement and each item gets its group's count (cluster bootstrap)."""
    rng = np.random.default_rng(seed)
    if groups is not None:
        uniq, inv = np.unique(groups, return_inverse=True)
    for s in range(0, n_boot, CHUNK):
        k = min(CHUNK, n_boot - s)
        if groups is None:
            yield rng.multinomial(n, np.full(n, 1 / n), size=k).astype(np.float32)
        else:
            g = len(uniq)
            yield rng.multinomial(g, np.full(g, 1 / g), size=k).astype(np.float32)[:, inv]


def mdl_curves(costs: np.ndarray, w: np.ndarray) -> np.ndarray:
    """costs [L+1, n] bits; w [k, n] counts -> curves proportional to compression [k, L+1] (1 / total cost)."""
    return 1.0 / (w @ costs.T)


def acc_curves(correct: np.ndarray, w: np.ndarray) -> np.ndarray:
    """correct [L+1, n] booleans -> weighted accuracy curves [k, L+1]."""
    return (w @ correct.T.astype(np.float32)) / w.sum(1, keepdims=True)


def ci(x) -> list:
    return [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))]


def detok_ci(costs: np.ndarray, groups: np.ndarray | None, seed: int = 0) -> list:
    """95% CI of the MDL detok layer; groups aligned with the columns of costs (None = item level)."""
    return ci(np.concatenate([first_reach(mdl_curves(costs, w)) for w in weights(costs.shape[1], seed, groups)]))
