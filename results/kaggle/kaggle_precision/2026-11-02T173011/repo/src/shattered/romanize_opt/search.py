"""Greedy coordinate-descent search for a tokenizer-optimal reversible romanization (E9).

Objective: total tokens over a weighted Kannada word list, sum_w count(w) * ntok(" " + encode(w)), under one or more
local tokenizers (never API counters). For a multi-tokenizer ("universal") objective, each tokenizer's total is
normalized by its ITRANS total and the normalized totals are averaged.

Changing one unit's spelling only affects words containing that unit, so evaluations re-encode and re-count just
those words.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

import numpy as np

from ..translit.scheme import Scheme
from .candidates import all_candidates, itrans_assignment, tables


@dataclass
class SearchResult:
    assignment: dict
    objective: float
    per_tokenizer: dict
    history: list
    evaluations: int


class WordObjective:
    def __init__(self, words: list[str], weights: np.ndarray, counters: dict, base_scheme: Scheme) -> None:
        self.words = words
        self.w = np.asarray(weights, dtype=np.float64)
        self.counters = counters  # name -> f(list[str]) -> list[int]
        self.units = [base_scheme.units(w) for w in words]
        self.by_key: dict[str, np.ndarray] = {}
        tmp: dict[str, list[int]] = {}
        for i, us in enumerate(self.units):
            for k in {u.native for u in us if u.kind in ("C", "V", "IV", "S")}:
                tmp.setdefault(k, []).append(i)
        self.by_key = {k: np.asarray(v) for k, v in tmp.items()}
        self.norm = None
        self.evaluations = 0

    def scheme(self, assign: dict) -> Scheme:
        c, v, g = tables(assign)
        return Scheme("search", c, v, g)

    def counts(self, scheme: Scheme, idx: np.ndarray | None = None) -> dict[str, np.ndarray]:
        idx = np.arange(len(self.words)) if idx is None else idx
        texts = [" " + scheme.encode_units(self.units[i]) for i in idx]
        self.evaluations += 1
        return {n: np.asarray(f(texts), dtype=np.float64) for n, f in self.counters.items()}

    def total(self, per_word: dict[str, np.ndarray]) -> tuple[float, dict]:
        per_tok = {n: float((c * self.w).sum()) for n, c in per_word.items()}
        if self.norm is None:
            return per_tok[next(iter(per_tok))], per_tok
        return float(np.mean([per_tok[n] / self.norm[n] for n in per_tok])), per_tok


def coordinate_descent(obj: WordObjective, init: dict, cands: dict, seed: int, max_sweeps: int = 6,
                       log=print) -> SearchResult:
    rng = random.Random(seed)
    assign = dict(init)
    scheme = obj.scheme(assign)
    cur = obj.counts(scheme)
    best, per_tok = obj.total(cur)
    history = [{"sweep": 0, "objective": best}]
    keys = list(cands)
    for sweep in range(1, max_sweeps + 1):
        improved = False
        rng.shuffle(keys)
        for key in keys:
            idx = obj.by_key.get(key[1])
            if idx is None:  # unit never occurs in the word list: keep it
                continue
            for sp in cands[key]:
                if sp == assign[key] or sp in {s for k, s in assign.items() if k != key}:
                    continue
                trial = {**assign, key: sp}
                try:
                    sch = obj.scheme(trial)
                    part = obj.counts(sch, idx)
                except ValueError:
                    continue  # invalid or non-separable scheme
                new = {n: c.copy() for n, c in cur.items()}
                for n in new:
                    new[n][idx] = part[n]
                val, pt = obj.total(new)
                if val < best - 1e-9:
                    best, per_tok, assign, cur = val, pt, trial, new
                    improved = True
        history.append({"sweep": sweep, "objective": best})
        log(f"  sweep {sweep}: objective {best:.6g}")
        if not improved:
            break
    return SearchResult(assign, best, per_tok, history, obj.evaluations)


def random_valid_init(cands: dict, seed: int, base: dict | None = None) -> dict:
    """Random assignment with unique spellings (falls back to base where needed)."""
    rng = random.Random(seed)
    assign, used = {}, set()
    for key in sorted(cands, key=lambda k: len(cands[k])):
        opts = [s for s in cands[key] if s not in used]
        rng.shuffle(opts)
        sp = opts[0] if opts else (base or {}).get(key)
        assign[key] = sp
        used.add(sp)
    return assign


def lowercase_init(cands_lower: dict) -> dict:
    """First lowercase candidate per unit, made unique."""
    assign, used = {}, set()
    for key, opts in cands_lower.items():
        sp = next(s for s in opts if s not in used)
        assign[key] = sp
        used.add(sp)
    return assign


__all__ = ["WordObjective", "coordinate_descent", "random_valid_init", "lowercase_init", "all_candidates",
           "itrans_assignment"]
