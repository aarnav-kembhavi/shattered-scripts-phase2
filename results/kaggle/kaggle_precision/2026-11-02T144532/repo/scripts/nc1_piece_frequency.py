"""NC1 piece-frequency proxy (post hoc descriptive, 2026-10-22, no verdict). CPU only; tokenizers only, no model.

Replaces the token-id rank proxy. For each tokenizer, canonical token frequencies are counted over a reference corpus:
all lossy text in the study (FLORES+ dev+devtest 2,009 sentences, the 200 sentiment and 200 XNLI items, the 1,004
SIB-200 items) plus the English FLORES+ dev+devtest (2,009). For each NC1 condition (a), (b), (c) the pieces used in
the Kannada text span are looked up; reported per model and dataset: mean and median log(count + 1) and the share of
pieces never seen in the canonical reference (count 0). The splits are regenerated with nc1's fixed seeds, so they are
the ones the NC1 run uses. Note: the reference is canonical tokenization, so (a) is in-distribution by construction.

Usage: python scripts/nc1_piece_frequency.py     Output: results/nc1/piece_frequency.csv
"""
import sys
from collections import Counter

import numpy as np
import pandas as pd

from shattered.runlog import REPO, results_dir, write_json
from shattered.translit import to_lossy

sys.path.insert(0, str(REPO / "scripts"))
import l_ladder as lad  # noqa: E402
import nc1  # noqa: E402


def reference_texts() -> list[str]:
    from m14_full import flores_forms
    F = flores_forms()
    items = nc1.score_items()
    lossy = [to_lossy(t) for t in F["native"]]
    lossy += [v for _, its in items for it in its for v in it["forms"]["lossy"].values()]
    return lossy + list(F["english"])


def main() -> None:
    from transformers import AutoTokenizer
    from shattered.interp.load import MODELS as REPOS
    ref = reference_texts()
    R, keep, native = lad.m4c_sample()
    tasks = nc1.score_items()
    rows = []
    for m in lad.ACC_MODELS:
        tok = AutoTokenizer.from_pretrained(REPOS[m])
        V = nc1.Vocab(tok)
        freq = Counter(s for x in tok(ref, add_special_tokens=False)["input_ids"] for s in tok.convert_ids_to_tokens(x))
        sets = {"m4c496": [q[3] for q, k in zip(nc1.m4c_conditions(V, m, R, native), keep) if k]}
        for t, its in tasks:
            sets[t] = [nc1.prompt_conditions(V, m, it["id"], t, it["forms"]["lossy"], it["forms"]["lower"])
                       for it in its]
        for d, items in sets.items():
            for c in nc1.CONDITIONS:
                n = np.array([freq.get(p, 0) for it in items for u in it[c][1] for p in u["pieces"]])
                lf = np.log(n + 1)
                rows.append({"model": m, "dataset": d, "condition": c, "n_items": len(items), "n_pieces": len(n),
                             "mean_log_freq": lf.mean(), "median_log_freq": float(np.median(lf)),
                             "share_unseen": float((n == 0).mean())})
            print(m, d, "done", flush=True)
    out = results_dir("nc1")
    pd.DataFrame(rows).to_csv(out / "piece_frequency.csv", index=False)
    write_json(out / "piece_frequency_provenance.json", {"reference_texts": len(ref)},
               {"status": "post hoc descriptive, 2026-10-22, no verdict", "log": "natural log of (count + 1)"})


if __name__ == "__main__":
    main()
