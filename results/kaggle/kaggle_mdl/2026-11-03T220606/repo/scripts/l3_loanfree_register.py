"""Register check for the A4 loan-free L3 subset (post hoc descriptive, 2026-10-23, no verdict). CPU only, text only.

The loan-free subset (natural text with no English word of 4+ characters, wordfreq Zipf >= 3; as
scripts/l_ladder_posthoc.py) may differ in register from the other items. For loan-free vs other items, per L3 sample
(retrieval: M4c test half 248; sentiment: 198 clean natural items; SIB-257), reported: mean sentence length in native
words and in natural-romanization words, and a named-entity proxy: capitalized words that are not sentence-initial,
counted in the English source and in the natural romanization.

Usage: python scripts/l3_loanfree_register.py     Output: results/l_ladder_posthoc/l3_loanfree_register.csv
"""
import re
import sys

import numpy as np
import pandas as pd

from shattered.runlog import REPO, results_dir, write_json

sys.path.insert(0, str(REPO / "scripts"))
import english_share as es  # noqa: E402
import l_ladder as lad  # noqa: E402
from l_ladder_posthoc import has_english  # noqa: E402
from m4c_natural_flores import SEED  # noqa: E402

SENT_START = re.compile(r"(^|[.!?]\s+)$")


def caps(text: str) -> int:
    """Capitalized words not at the start of a sentence (named-entity proxy)."""
    n = 0
    for m in re.finditer(r"\S+", text):
        w = m.group().strip("\"'([“‘")
        if w[:1].isupper() and not SENT_START.search(text[: m.start()]):
            n += 1
    return n


def samples() -> dict:
    from m14_full import flores_forms
    F = flores_forms()
    R, keep, native = lad.m4c_sample()
    kept = [(r, t) for r, t, k in zip(R, native, keep) if k]
    n = len(kept)
    te = np.sort(np.random.default_rng(SEED).permutation(n)[n // 2:])
    out = {"retrieval (M4c test half)": [(kept[i][1], kept[i][0]["natural"], F["english"][kept[i][0]["index"]])
                                         for i in te]}
    out["sentiment"] = [(it["forms"]["native"]["text"], it["forms"]["natural"]["text"], it["forms"]["english"]["text"])
                        for it in lad.e0b_items()["sentiment"] if not it.get("natural_defective")]
    out["SIB-257"] = [(F["native"][it["id"]], it["forms"]["natural257"]["text"], F["english"][it["id"]])
                      for it in lad.sib257_items()["sib"]]
    return out


def main() -> None:
    wl = es.wordlists()["zipf>=3"]
    rows = []
    for d, items in samples().items():
        X = pd.DataFrame([{"loan_free": not has_english(nat, wl), "native_words": len(nv.split()),
                           "natural_words": len(nat.split()), "caps_english": caps(en), "caps_natural": caps(nat)}
                          for nv, nat, en in items])
        for lf, g in X.groupby("loan_free"):
            rows.append({"dataset": d, "group": "loan-free" if lf else "other", "n": len(g),
                         **{f"mean_{c}": g[c].mean() for c in ("native_words", "natural_words", "caps_english",
                                                                 "caps_natural")},
                         "share_with_caps_english": (g.caps_english > 0).mean()})
    out = results_dir("l_ladder_posthoc")
    pd.DataFrame(rows).to_csv(out / "l3_loanfree_register.csv", index=False)
    write_json(out / "l3_loanfree_register_provenance.json", {"rows": len(rows)},
               {"status": "post hoc descriptive, 2026-10-23, no verdict",
                "caps": "capitalized words not sentence-initial"})
    pd.set_option("display.width", 200)
    print(pd.DataFrame(rows).round(2).to_string())


if __name__ == "__main__":
    main()
