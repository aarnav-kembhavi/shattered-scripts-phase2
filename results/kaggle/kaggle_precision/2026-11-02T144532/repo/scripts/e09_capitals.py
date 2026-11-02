"""E9 diagnostic: do mid-word capitals explain ITRANS's extra tokens on modern tokenizers?

Compares, on FLORES Kannada: native, ITRANS, and ITRANS lowercased (lossy; a diagnostic only). Reports the share of
ITRANS's excess over native that disappears when capitals are removed, and per-word token deltas for words that
contain a capital after the first letter.

Usage: python scripts/e09_capitals.py [--corpus flores_plus]
Output: results/e09_romanize/capitals.json
"""
import argparse

import numpy as np

from shattered.data import corpora
from shattered.runlog import results_dir, write_json
from shattered.tok.registry import load_counter
from shattered.translit import to_itrans

TOKENIZERS = [
    {"id": "o200k_base", "kind": "tiktoken", "label": "o200k"},
    {"id": "google/gemma-4-E2B-it", "kind": "hf", "label": "Gemma 4"},
    {"id": "Qwen/Qwen3.5-9B", "kind": "hf", "label": "Qwen3.5"},
    {"id": "Qwen/Qwen3-8B", "kind": "hf", "label": "Qwen2.5/3"},
    {"id": "sarvamai/sarvam-1", "kind": "hf", "label": "Sarvam-1"},
]


def has_midword_capital(w: str) -> bool:
    return any(c.isupper() for c in w[1:])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="flores_plus")
    args = ap.parse_args()
    native = [t for s in ("dev", "devtest") for t in corpora.flores_any("kan_Knda", s, args.corpus, nfc=True)]
    itrans = [to_itrans(t) for t in native]
    lower = [t.lower() for t in itrans]
    words = sorted({w for t in itrans for w in t.split()})
    cap_words = [w for w in words if has_midword_capital(w)]
    word_freq = {}
    for t in itrans:
        for w in t.split():
            word_freq[w] = word_freq.get(w, 0) + 1
    out = {"n_sentences": len(native),
           "share_word_tokens_with_midword_capital": sum(word_freq[w] for w in cap_words) / sum(word_freq.values()),
           "tokenizers": {}}
    for spec in TOKENIZERS:
        count = load_counter(spec)
        tn, ti, tl = (sum(count(x)) for x in (native, itrans, lower))
        cw = np.asarray(count([" " + w for w in cap_words]))
        cl = np.asarray(count([" " + w.lower() for w in cap_words]))
        f = np.asarray([word_freq[w] for w in cap_words])
        res = {"tokens_native": tn, "tokens_itrans": ti, "tokens_itrans_lowercased": tl,
               "itrans_vs_native": ti / tn, "lowercased_vs_native": tl / tn,
               "capital_cost_share_of_itrans_tokens": (ti - tl) / ti,
               "share_of_excess_over_native_explained_by_capitals": ((ti - tl) / (ti - tn)) if ti > tn else None,
               "midcap_words_mean_tokens": float((cw * f).sum() / f.sum()),
               "midcap_words_mean_tokens_lowercased": float((cl * f).sum() / f.sum())}
        out["tokenizers"][spec["label"]] = res
        print(spec["label"], {k: round(v, 3) if isinstance(v, float) else v for k, v in res.items()})
    write_json(results_dir("e09_romanize") / "capitals.json", out, {"corpus": args.corpus, "lang": "kan_Knda"})
    print("share of word tokens with a mid-word capital:", round(out["share_word_tokens_with_midword_capital"], 3))


if __name__ == "__main__":
    main()
