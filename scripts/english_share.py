"""Share of words that are English words in natural, lossy and ITRANS romanization (post hoc descriptive, 2026-10-22,
no verdict). CPU only; no model is run.

Samples (matched: every form on the same items):
- m4c496: the 496 retained M4c FLORES+ sentences;
- sentiment: the 198 IndicSentiment items with a clean natural romanization (2 of the 200 are natural_defective).

Word = whitespace token with leading/trailing non-letters stripped; tokens with no ASCII letter left are dropped
(numbers, punctuation). A word is English if its lowercased form is in the English wordlist. Wordlist: wordfreq
(Speer et al., https://github.com/rspeer/wordfreq), language "en", "best" list; primary = words with Zipf frequency
>= 3.0 (at least about once per million words), sensitivity = Zipf >= 4.0. ITRANS is also reported "as written"
(a word with any uppercase letter is not English: in ITRANS uppercase marks Kannada long vowels/retroflexes).

No named-entity list exists in this repo, so proper nouns are approximated by capitalization in natural: a natural
word that starts with an uppercase letter and is not sentence-initial (not the first word of the text and not after a
word ending in . ! ?). "no proper nouns" removes those words from natural and, best effort, removes from lossy and
ITRANS of the same item any word whose lowercased form equals one of them.

Share = English words / words, pooled over items. CI: paired bootstrap over items, 10,000 resamples, seed 0,
percentile 95%.

Usage: python scripts/english_share.py     Outputs: results/english_share/{shares.csv, wordlist.json}
"""
import re
import sys
from collections import Counter

import numpy as np
import pandas as pd
from wordfreq import iter_wordlist, zipf_frequency
import importlib.metadata as md

from shattered.runlog import REPO, results_dir, write_json

sys.path.insert(0, str(REPO / "scripts"))
import l_ladder as lad  # noqa: E402

FORMS = ["natural", "lossy", "itrans"]
THRESHOLDS = {"zipf>=3": 3.0, "zipf>=4": 4.0}
B, SEED = 10_000, 0
EDGE = re.compile(r"^[^A-Za-z]+|[^A-Za-z]+$")


def wordlists() -> dict:
    out = {k: set() for k in THRESHOLDS}
    for w in iter_wordlist("en", "best"):
        z = zipf_frequency(w, "en", "best")
        if z < min(THRESHOLDS.values()):
            break
        for k, t in THRESHOLDS.items():
            if z >= t:
                out[k].add(w)
    return out


def words(text: str) -> list[str]:
    return [w for w in (EDGE.sub("", t) for t in text.split()) if re.search("[A-Za-z]", w)]


def proper(text: str) -> set[str]:
    toks, out = text.split(), set()
    for i, t in enumerate(toks):
        w = EDGE.sub("", t)
        if i > 0 and w[:1].isupper() and not re.search(r"[.!?][\"')\]]*$", toks[i - 1]):
            out.add(w.lower())
    return out


def samples() -> dict:
    from m14_full import flores_forms
    a = lad.e0b_items()
    sent = [{f: it["forms"][f]["text"] for f in FORMS} for it in a["sentiment"] if not it.get("natural_defective")]
    F = flores_forms()
    R, keep, native = lad.m4c_sample()
    m4c = [{"natural": r["natural"], "lossy": lad.to_lossy(t), "itrans": F["itrans"][r["index"]]}
           for r, k, t in zip(R, keep, native) if k]
    return {"m4c496": m4c, "sentiment198": sent}


def counts(items, wl, drop_proper, as_written=False):
    """(n_items, n_forms, 2) array: English words and words per item and form."""
    out = np.zeros((len(items), len(FORMS), 2))
    for i, it in enumerate(items):
        P = proper(it["natural"]) if drop_proper else set()
        for j, f in enumerate(FORMS):
            W = [w for w in words(it[f]) if w.lower() not in P]
            eng = [w for w in W if w.lower() in wl and not (as_written and f == "itrans" and w != w.lower())]
            out[i, j] = len(eng), len(W)
    return out


def main() -> None:
    out = results_dir("english_share")
    WL = wordlists()
    S = samples()
    rng = np.random.default_rng(SEED)
    rows = []
    for d, items in S.items():
        idx = rng.integers(0, len(items), size=(B, len(items)))
        for wk, wl in WL.items():
            for variant, dp, aw in (("all words", False, False), ("no proper nouns", True, False),
                                    ("all words, ITRANS as written", False, True)):
                C = counts(items, wl, dp, aw)
                share = C[:, :, 0].sum(0) / C[:, :, 1].sum(0)
                bs = C[idx].sum(1)                      # (B, forms, 2)
                bshare = bs[:, :, 0] / bs[:, :, 1]
                for j, f in enumerate(FORMS):
                    lo, hi = np.percentile(bshare[:, j], [2.5, 97.5])
                    rows.append({"sample": d, "n_items": len(items), "wordlist": wk, "variant": variant,
                                 "quantity": f, "n_words": int(C[:, j, 1].sum()), "n_english": int(C[:, j, 0].sum()),
                                 "value": share[j], "ci_low": lo, "ci_high": hi})
                for a_, b_ in (("natural", "lossy"), ("natural", "itrans")):
                    ja, jb = FORMS.index(a_), FORMS.index(b_)
                    diff = bshare[:, ja] - bshare[:, jb]
                    lo, hi = np.percentile(diff, [2.5, 97.5])
                    rows.append({"sample": d, "n_items": len(items), "wordlist": wk, "variant": variant,
                                 "quantity": f"{a_} - {b_}", "value": share[ja] - share[jb], "ci_low": lo,
                                 "ci_high": hi})
    pd.DataFrame(rows).to_csv(out / "shares.csv", index=False)
    top = {d: {f: Counter(w.lower() for it in items for w in words(it[f]) if w.lower() in WL["zipf>=3"])
               .most_common(25) for f in FORMS} for d, items in S.items()}
    write_json(out / "wordlist.json", {"source": "wordfreq " + md.version("wordfreq") + ", language en, list 'best'",
                                       "url": "https://github.com/rspeer/wordfreq",
                                       "sizes": {k: len(v) for k, v in WL.items()},
                                       "top_matched_words_zipf3_all_words": top,
                                       "proper_noun_rule": "capitalized, not sentence-initial, in natural"},
               {"status": "post hoc descriptive, 2026-10-22, no verdict", "bootstrap": B, "seed": SEED})
    print(pd.DataFrame(rows).to_string())


if __name__ == "__main__":
    main()
