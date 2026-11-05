"""X14 (exploratory, no verdict): per hosted model, SIB-200 accuracy by form with 95% bootstrap intervals (items, 10,000, seed 0) and native minus form gaps (paired over item ids; natural on its 257-item subset).
Usage: python scripts/x14_analyse.py        Output: results/phase2/x14/analysis.json"""
import json
from pathlib import Path

import numpy as np

from shattered.runlog import REPO, write_json

OUT = REPO / "results" / "phase2" / "x14"
FORMS = ["native", "itrans", "lossy", "natural"]


def main() -> None:
    rng = np.random.default_rng(0)
    res = {}
    for p in sorted((OUT / "raw").glob("*.jsonl")):
        R = [json.loads(l) for l in p.open(encoding="utf-8")]
        c = {f: {r["id"]: float(r["pred"] == r["label"]) for r in R if r["form"] == f} for f in FORMS}
        row = {"acc": {}, "gap_native_minus": {}, "unparsed_share": {f: float(np.mean([r["pred"] is None for r in R if r["form"] == f])) for f in FORMS}}
        for f in FORMS:
            v = np.array(list(c[f].values()))
            b = v[rng.integers(0, len(v), (10_000, len(v)))].mean(1)
            row["acc"][f] = {"n": len(v), "acc": float(v.mean()), "ci95": [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))]}
        for f in FORMS[1:]:
            ids = sorted(set(c["native"]) & set(c[f]))
            d = np.array([c["native"][i] - c[f][i] for i in ids])
            b = d[rng.integers(0, len(d), (10_000, len(d)))].mean(1)
            row["gap_native_minus"][f] = {"n": len(ids), "gap": float(d.mean()), "ci95": [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))]}
        res[p.stem] = row
    write_json(OUT / "analysis.json", res, {"status": "exploratory, no verdict", "registered": "Amendment 2 X14"})
    for m, r in res.items():
        print(m, {f: (round(v["acc"], 3), [round(x, 3) for x in v["ci95"]]) for f, v in r["acc"].items()})
        print("  gap", {f: (round(v["gap"], 3), [round(x, 3) for x in v["ci95"]], v["n"]) for f, v in r["gap_native_minus"].items()}, "unparsed", {f: round(x, 3) for f, x in r["unparsed_share"].items()})


if __name__ == "__main__":
    main()
