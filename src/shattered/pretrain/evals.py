"""E5 evaluations beyond BPB: templated grammatical minimal pairs restricted to TinyStories vocabulary.

Each pair (good, bad) differs in one word. A model is correct when log P(good) > log P(bad), using the total log
probability of the whole sentence given a leading EOS (the story separator). Per-byte normalized accuracy is also
reported because some bad forms are longer ("runned").
"""
from __future__ import annotations

import itertools
import random

import numpy as np
import torch

SING_PLUR = [("dog", "dogs"), ("cat", "cats"), ("girl", "girls"), ("boy", "boys"), ("bird", "birds"),
             ("friend", "friends"), ("bunny", "bunnies"), ("frog", "frogs"), ("duck", "ducks"), ("bear", "bears")]
VERBS = [("runs", "run"), ("jumps", "jump"), ("plays", "play"), ("walks", "walk"), ("sings", "sing"),
         ("laughs", "laugh"), ("smiles", "smile"), ("sleeps", "sleep")]
SVA_FRAMES = ["The {s} {v} in the park.", "The little {s} {v} every day.", "Every morning, the {s} {v} with joy."]
DET_FRAMES = ["Tom saw {d} {n} near the tree.", "Lily liked {d} {n} very much.", "Mom gave {d} {n} some food."]
IRREGULAR = [("went", "goed"), ("ate", "eated"), ("ran", "runned"), ("saw", "seed"), ("took", "taked"),
             ("gave", "gived"), ("found", "finded"), ("came", "comed"), ("made", "maked"), ("sat", "sitted"),
             ("felt", "feeled"), ("knew", "knowed")]
PAST_FRAMES = {
    "went": "Yesterday, Lily {v} to the park.", "ate": "Yesterday, Tom {v} a big cake.",
    "ran": "Yesterday, the dog {v} very fast.", "saw": "Yesterday, Sue {v} a pretty bird.",
    "took": "Yesterday, Ben {v} the red ball.", "gave": "Yesterday, Mom {v} Tim a hug.",
    "found": "Yesterday, Max {v} a shiny stone.", "came": "Yesterday, Grandma {v} to visit.",
    "made": "Yesterday, Amy {v} a sand castle.", "sat": "Yesterday, the cat {v} on the mat.",
    "felt": "Yesterday, Sam {v} very happy.", "knew": "Yesterday, Anna {v} the answer.",
}


def minimal_pairs(seed: int = 0, max_per_phenomenon: int = 200) -> list[dict]:
    pairs = []
    for (s, p), (v3, v), f in itertools.product(SING_PLUR, VERBS, SVA_FRAMES):
        pairs.append({"phenomenon": "subject_verb_agreement_singular", "good": f.format(s=s, v=v3),
                      "bad": f.format(s=s, v=v)})
        pairs.append({"phenomenon": "subject_verb_agreement_plural", "good": f.format(s=p, v=v),
                      "bad": f.format(s=p, v=v3)})
    for (s, p), f in itertools.product(SING_PLUR, DET_FRAMES):
        pairs.append({"phenomenon": "determiner_noun_agreement", "good": f.format(d="this", n=s),
                      "bad": f.format(d="these", n=s)})
        pairs.append({"phenomenon": "determiner_noun_agreement", "good": f.format(d="these", n=p),
                      "bad": f.format(d="this", n=p)})
    for good, bad in IRREGULAR:
        f = PAST_FRAMES[good]
        pairs.append({"phenomenon": "irregular_past", "good": f.format(v=good), "bad": f.format(v=bad)})
    rng = random.Random(seed)
    out = []
    for ph in sorted({p["phenomenon"] for p in pairs}):
        group = [p for p in pairs if p["phenomenon"] == ph]
        rng.shuffle(group)
        out += group[:max_per_phenomenon]
    return out


def vocabulary_check(pairs: list[dict], word_counts: dict) -> dict:
    """Training-corpus counts of every word used in good sentences (bad forms are expected to be rare)."""
    words = {w.strip(".,").lower() for p in pairs for w in p["good"].split()}
    return {w: word_counts.get(w, 0) for w in sorted(words)}


@torch.no_grad()
def sentence_logprobs(model, tok, sentences: list[str], device: str) -> list[float]:
    eos = tok.token_to_id("<|endoftext|>")
    model.eval()
    out = []
    for s in sentences:
        ids = [eos] + tok.encode(s).ids
        x = torch.tensor(ids, device=device)[None]
        logits, _, _ = model(x[:, :-1])
        lp = torch.log_softmax(logits.float(), -1)[0].gather(-1, x[0, 1:, None]).sum()
        out.append(float(lp))
    return out


def score_minimal_pairs(model, tok, pairs: list[dict], device: str) -> dict:
    good = sentence_logprobs(model, tok, [p["good"] for p in pairs], device)
    bad = sentence_logprobs(model, tok, [p["bad"] for p in pairs], device)
    res = {}
    for ph in sorted({p["phenomenon"] for p in pairs}) + ["all"]:
        idx = [i for i, p in enumerate(pairs) if ph == "all" or p["phenomenon"] == ph]
        acc = np.mean([good[i] > bad[i] for i in idx])
        accb = np.mean([good[i] / len(pairs[i]["good"].encode()) > bad[i] / len(pairs[i]["bad"].encode())
                        for i in idx])
        res[ph] = {"n": len(idx), "acc_total_logprob": float(acc), "acc_per_byte": float(accb)}
    return res
