"""Linear word-identity probes per layer (M1b), with a random-label control and bootstrap CIs on the detok layer.

Probe: multinomial logistic regression on standardized features (train-split statistics), full-batch Adam on GPU,
fixed hyperparameters for every model/layer (no tuning on test data). Split: held-out occurrences, stratified by word.
Control: the same probe trained on labels permuted across training occurrences (tests memorization capacity; expected
near chance on the held-out set).
Detokenization layer: first layer whose held-out accuracy reaches `frac` (0.9) of the model's maximum over layers.
"""
from __future__ import annotations

import numpy as np
import torch
import torch.nn.functional as F

PROBE = {"steps": 300, "lr": 1e-2, "weight_decay": 1e-3}


def split_by_word(labels: np.ndarray, test_frac: float = 0.3, seed: int = 0) -> np.ndarray:
    """Boolean train mask: per word, round(test_frac * n) occurrences held out (at least one if n >= 2)."""
    rng = np.random.default_rng(seed)
    train = np.ones(len(labels), bool)
    for w in np.unique(labels):
        idx = np.flatnonzero(labels == w)
        if len(idx) < 2:
            continue
        k = max(1, int(round(test_frac * len(idx))))
        train[rng.choice(idx, k, replace=False)] = False
    return train


def fit_predict(Xtr: torch.Tensor, ytr: torch.Tensor, Xte: torch.Tensor, n_classes: int, seed: int = 0,
                steps: int = PROBE["steps"], lr: float = PROBE["lr"], wd: float = PROBE["weight_decay"]) -> torch.Tensor:
    """Returns predicted labels for Xte."""
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-6
    Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
    g = torch.Generator(device="cpu").manual_seed(seed)
    W = (torch.randn(Xtr.shape[1], n_classes, generator=g) * 0.01).to(Xtr.device).requires_grad_()
    b = torch.zeros(n_classes, device=Xtr.device, requires_grad=True)
    opt = torch.optim.Adam([W, b], lr=lr)
    for _ in range(steps):
        opt.zero_grad(set_to_none=True)
        loss = F.cross_entropy(Xtr @ W + b, ytr) + wd * (W ** 2).sum()
        loss.backward()
        opt.step()
    with torch.no_grad():
        return (Xte @ W + b).argmax(1)


def layer_curve(states: np.ndarray, labels: np.ndarray, train_mask: np.ndarray, seed: int = 0,
                device: str = "cuda") -> dict:
    """states [n, L+1, d]; labels int [n]. Returns per-layer held-out accuracy (probe and control) and the held-out
    correctness matrix [L+1, n_test] for bootstrapping."""
    y = torch.as_tensor(labels, device=device)
    tr, te = torch.as_tensor(train_mask, device=device), torch.as_tensor(~train_mask, device=device)
    n_classes = int(labels.max()) + 1
    y_ctrl = y.clone()
    perm = torch.as_tensor(np.random.default_rng(seed + 1).permutation(int(train_mask.sum())), device=device)
    y_ctrl[tr] = y[tr][perm]
    acc, acc_ctrl, correct = [], [], []
    for layer in range(states.shape[1]):
        X = torch.as_tensor(states[:, layer], device=device, dtype=torch.float32)
        pred = fit_predict(X[tr], y[tr], X[te], n_classes, seed)
        c = (pred == y[te])
        correct.append(c.cpu().numpy())
        acc.append(float(c.float().mean()))
        pc = fit_predict(X[tr], y_ctrl[tr], X[te], n_classes, seed)
        acc_ctrl.append(float((pc == y[te]).float().mean()))
    return {"acc": np.asarray(acc), "acc_control": np.asarray(acc_ctrl), "correct": np.stack(correct)}


def detok_layer(acc: np.ndarray, frac: float = 0.9) -> int:
    return int(np.flatnonzero(acc >= frac * acc.max())[0])


def bootstrap_detok(correct: np.ndarray, frac: float = 0.9, n_boot: int = 2000, seed: int = 0,
                    subset: np.ndarray | None = None) -> dict:
    """correct [L+1, n_test] booleans. Resamples test occurrences; returns point estimate, 95% CI and the bootstrap
    distribution's mean. `subset` restricts to some test occurrences (e.g. multi-token words)."""
    c = correct if subset is None else correct[:, subset]
    point = detok_layer(c.mean(1), frac)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, c.shape[1], size=(n_boot, c.shape[1]))
    boots = np.array([detok_layer(c[:, i].mean(1), frac) for i in idx])
    return {"detok_layer": point, "ci_low": float(np.percentile(boots, 2.5)),
            "ci_high": float(np.percentile(boots, 97.5)), "boot_mean": float(boots.mean()), "n_test": int(c.shape[1]),
            "acc": c.mean(1).tolist()}
