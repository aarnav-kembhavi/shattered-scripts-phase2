"""Validity check of the English-word tagger on Kannada Kanglish (Aarnav, 2026-10-26; before any K2 result exists).

A sample of kanglish_verified texts (data/annotation/verified_A_v1.jsonl, default_rng(seed)); every alphabetic token
is tagged by the tagger version given; precision and recall of the "en" tag against Claude Code's hand marking
(results/codemix_check/gold_sample<seed>.json). Gold N (names) and H (English stem + Kannada suffix) count as not
English; a sensitivity line counts H as English.

Usage: python scripts/codemix_check.py <seed> <v1|v2>     -> results/codemix_check/check_sample<seed>_<v>.json
"""
import json
import sys

import numpy as np

from shattered.runlog import REPO, results_dir, write_json
from shattered.translit import codemix

OUT = results_dir("codemix_check")


def sample(seed: int) -> list:
    V = [json.loads(x) for x in open(REPO / "data/annotation/verified_A_v1.jsonl", encoding="utf-8")]
    return [V[k] for k in sorted(np.random.default_rng(seed).choice(len(V), 50, replace=False).tolist())]


def main(seed: int, version: str) -> None:
    gold_file = json.load(open(OUT / f"gold_sample{seed}.json", encoding="utf-8"))
    over = gold_file["overrides"]
    default = gold_file.get("default_from_v1_tag", {"en": "E", "kn": "K", "u": "K"})
    toks = []
    for v in sample(seed):
        t1 = codemix.tag(v["kanglish_verified"])
        tv = t1 if version == "v1" else codemix.tag_v2(v["kanglish_verified"], v["english"])
        for (tok, g1), (_, g) in zip(t1, tv):
            if tok.isalpha():
                w = tok.lower()
                toks.append({"item_id": v["item_id"], "token": tok, "tag": g, "gold": over.get(w, default[g1])})
    res = {}
    for name, eng in (("main (H not English)", {"E"}), ("sensitivity (H English)", {"E", "H"})):
        tp = sum(t["tag"] == "en" and t["gold"] in eng for t in toks)
        fp = sum(t["tag"] == "en" and t["gold"] not in eng for t in toks)
        fn = sum(t["tag"] != "en" and t["gold"] in eng for t in toks)
        res[name] = {"tp": tp, "fp": fp, "fn": fn, "precision": tp / (tp + fp), "recall": tp / (tp + fn)}
    errs = {"false_positive": sorted({(t["token"].lower(), t["gold"]) for t in toks if t["tag"] == "en" and t["gold"] != "E"}),
            "missed_english": sorted({(t["token"].lower(), t["tag"]) for t in toks if t["tag"] != "en" and t["gold"] == "E"}),
            "hybrid_H": sorted({t["token"].lower() for t in toks if t["gold"] == "H"})}
    out = {"seed": seed, "tagger": version, "texts": 50, "alphabetic_tokens": len(toks),
           "tokens_tagged_en": sum(t["tag"] == "en" for t in toks), **res, "errors": errs}
    write_json(OUT / f"check_sample{seed}_{version}.json", out, {"gold": f"gold_sample{seed}.json"})
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(int(sys.argv[1]), sys.argv[2])
