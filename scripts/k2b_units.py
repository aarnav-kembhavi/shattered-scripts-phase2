"""Units for the K2b coefficients (descriptive; from the existing tagger output, no model): SD of the v2 English-word share
over the 300 items, the number of retrieval candidates, and the zero-overlap count. Output: results/k12/k2b_units.json"""
import sys

import numpy as np

from shattered.runlog import REPO, write_json
from shattered.translit.codemix import tag_v2

sys.path.insert(0, str(REPO / "scripts"))
import k2b_overlap as O  # noqa: E402
import k_k12 as K  # noqa: E402

items = K.k_items()["sib"]
txt = [it["forms"]["k_kan_ver"]["text"] for it in items]
eng = [it["english"] for it in items]
tags = [tag_v2(t, e) for t, e in zip(txt, eng)]
sh = np.array([sum(g == "en" for _, g in tg) / max(1, sum(g in ("en", "kn") for _, g in tg)) for tg in tags])
ov = np.array([O.overlap_share(t, e) for t, e in zip(txt, eng)])
te = np.load(REPO / "results/m4b_mapping/items.npz")["test_idx"]
write_json(K.OUT / "k2b_units.json",
           {"n_items": len(sh), "english_share_mean": float(sh.mean()), "english_share_sd": float(sh.std()),
            "n_candidates": int(len(te)), "n_zero_overlap": int((ov == 0).sum()),
            "outcome": "minus the natural log of the rank of the true English sentence among the candidates (higher is better)",
            "coefficient_unit": "per one standard deviation of the v2 English-word share (population SD, as the z-score)"},
           {"derived_from": "results/k12/vectors, tagger v2; descriptive"})
print(sh.mean(), sh.std(), len(te), int((ov == 0).sum()))
