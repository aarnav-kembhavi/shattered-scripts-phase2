"""X4 R3 (registered, Phase 2 pre-registration, X4): unmapped retrieval natural > ITRANS on the M4c rows (the Kannada M4c sample, 496 retained ids; test half n = 248, the M4c analog), counted retrieval models,
the enlarged-set effect rule (paired difference with a 95% bootstrap CI above 0 in at least n - 1 of the n counted models; uninformative with fewer than three). Counted retrieval models for the language are
read from results/phase2/x4/<lang>/r2.json (native unmapped retrieval at least 0.50). Uses the stored 500-row sentence vectors (cache/activations/x4_<lang>) and the stored English vectors (Phase 1 caches), the
split and layer choice of the Phase 1 M4c code path (scripts/x4_lang.py: retrieval_split, retrieval_hits). Native, lossy and ITRANS on the same ids are reported next to it (the natural-minus-lossy and
native-minus-natural ladder pieces need the lowercase form and are not part of R3).
Usage: X4_LANG=bn python scripts/x4_r3.py        Output: results/phase2/x4/<lang>/r3.json"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import x4_lang as X  # noqa: E402

from shattered.runlog import REPO, write_json  # noqa: E402

N_BOOT = 10_000


def boot(d: np.ndarray) -> dict:
    idx = np.random.default_rng(0).integers(0, len(d), (N_BOOT, len(d)))
    b = d[idx].mean(1)
    return {"diff": float(d.mean()), "ci95": [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))], "n": int(len(d))}


def main() -> None:
    lang = X.XL
    r2 = json.load(open(REPO / "results" / "phase2" / "x4" / lang / "r2.json", encoding="utf-8"))
    counted = r2["counted_models"]
    ids, keep = X.m4c_rows()
    nat = X.clean_natural()
    ids_d = [i for i, k in zip(ids, keep) if k and f"flores-{i}" in nat]
    out = {"language": lang, "n_ids_with_natural": len(ids_d), "models": {}}
    for m in counted:
        hits = {f: np.asarray(X.retrieval_hits(m, lang, f, ids_d), float) for f in ("native", "natural", "itrans", "lossy", "lower")}
        out["models"][m] = {"acc_test_half": {f: float(h.mean()) for f, h in hits.items()}, "natural_minus_itrans": boot(hits["natural"] - hits["itrans"]),
                            "native_minus_natural": boot(hits["native"] - hits["natural"]), "natural_minus_lossy": boot(hits["natural"] - hits["lossy"]),
                            "L1_lower_minus_itrans": boot(hits["lower"] - hits["itrans"]), "L2_lossy_minus_lower": boot(hits["lossy"] - hits["lower"])}
    n = len(counted)
    pos = sum(1 for v in out["models"].values() if v["natural_minus_itrans"]["ci95"][0] > 0)
    neg = sum(1 for v in out["models"].values() if v["natural_minus_itrans"]["ci95"][1] < 0)
    out["R3"] = {"n_counted": n, "natural_minus_itrans_ci_above_0": pos, "ci_below_0": neg,
                 "verdict": "uninformative (fewer than three counted models)" if n < 3 else "supported" if pos >= n - 1 and neg == 0 else "refuted" if neg > 0 or pos == 0 else "partly supported"}
    ladder = {}
    for name, key in (("L1", "L1_lower_minus_itrans"), ("L2", "L2_lossy_minus_lower"), ("L3", "natural_minus_lossy")):
        p_ = sum(1 for v in out["models"].values() if v[key]["ci95"][0] > 0)
        n_ = sum(1 for v in out["models"].values() if v[key]["ci95"][1] < 0)
        ladder[name] = {"ci_above_0": p_, "ci_below_0": n_, "verdict": "effect, positive" if p_ >= len(counted) - 1 else "effect, negative" if n_ >= len(counted) - 1 else "no effect detected"}
    out["retrieval_ladder_M4c"] = ladder
    write_json(REPO / "results" / "phase2" / "x4" / lang / "r3.json", out, {"registration": "RESULTS.md X4 (R3)"})
    print(lang, out["R3"], {m: ({f: round(a, 3) for f, a in v["acc_test_half"].items()}, [round(x, 3) for x in v["natural_minus_itrans"]["ci95"]]) for m, v in out["models"].items()})


if __name__ == "__main__":
    main()
