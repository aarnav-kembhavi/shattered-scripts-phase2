"""Sarvam-m X10, native minus ITRANS (post hoc extension; the registered X10-P verdict concerns the four counted accuracy models and is not changed). Reads the two Kaggle outputs
(account 3, sarvam-m, batch 16, 4-bit), uses the registered first-line outputs (output cut at the first newline; empty outputs scored as empty), sentence-level chrF2 (sacreBLEU, char 6, word 0, beta 2),
paired bootstrap (10,000, seed 0, two-sided p as in scripts/x10.py boot_p). Holm is reported over the registered family of 16 plus this one contrast (17), and the registered 16 p-values are read unchanged from analysis.json.
Writes results/phase2/x10/sarvam-m_analysis.json (a new file; nothing existing is changed)."""
import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "src"))
import x10  # noqa: E402

K = REPO / "results" / "kaggle" / "acct3" / "kaggle_x10"
files = {"native": K / "2026-11-08T105332" / "out" / "sarvam-m" / "native.json", "itrans": K / "2026-11-08T160147" / "out" / "sarvam-m" / "itrans.json"}
refs = x10.inputs()["reference"]
from sacrebleu.metrics import CHRF  # noqa: E402

S, corpus = {}, {}
for f, p in files.items():
    d = json.loads(p.read_text(encoding="utf-8"))
    hyp = d["registered_first_line"]
    r = [refs[i] for i in d["ids"]]
    S[f] = dict(zip(d["ids"], x10.chrf_scores(hyp, r)))
    corpus[f] = {"corpus_chrf": CHRF(char_order=6, word_order=0, beta=2).corpus_score(hyp, [r]).score, "n": d["summary"]["n"], "empty_share": d["summary"]["empty_share"],
                 "starts_with_think_share": d["summary"]["starts_with_think_share"], "seconds_per_sentence": d["summary"]["seconds_per_sentence"], "source": str(p.relative_to(REPO)).replace(chr(92), "/")}
ids = sorted(set(S["native"]) & set(S["itrans"]))
dd = np.array([S["native"][i] - S["itrans"][i] for i in ids])
row = {"model": "sarvam-m", "contrast": "native - itrans", "n": len(ids), **x10.boot_p(dd)}
reg = json.loads((REPO / "results/phase2/x10/analysis.json").read_text(encoding="utf-8"))
ps = [c["p"] for c in reg["contrasts"]] + [row["p"]]
from statsmodels.stats.multitest import multipletests  # noqa: E402
row["p_holm_family_17"] = float(multipletests(ps, method="holm")[1][-1])
row["significant_positive_family_17"] = bool(row["p_holm_family_17"] < 0.05 and row["diff"] > 0)
out = {"provenance": {"status": "post hoc extension (Sarvam-m is not one of the four counted models of X10-P); registered X10-P verdict unchanged", "registration": "RESULTS.md X10 and the 2026-11-08 16:23 IST entry (native and ITRANS only)",
                      "metric": "sentence chrF2 on the registered first-line outputs", "bootstrap": "10,000 resamples, seed 0, two-sided", "family": "Holm over the 16 registered contrasts plus this one (17)"},
       "contrast": row, "corpus": corpus, "registered_X10_P_unchanged": reg["X10_P"]}
(REPO / "results/phase2/x10/sarvam-m_analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps({"contrast": row, "corpus": corpus}, indent=1))
