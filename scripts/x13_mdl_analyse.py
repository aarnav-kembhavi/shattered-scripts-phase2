"""X13 MDL assembly-layer analysis for a Kaggle-run 7-9B model (default Qwen3-8B): native vs ITRANS on the 300 Phase 1 probe words, Phase 1 functions (scripts/m14_gate2.py: paired_mdl, word-clustered
bootstrap 10,000, seed 0; detok layer = first layer reaching 90% of the curve maximum).

Registration status (RESULTS.md Amendment 2, X13): the MDL run is registered ("Runs: ... MDL assembly") without a separate verdict word. The reading applied here is the Phase 1 H3 text as used in
the X4 rule R4: "the sign of (ITRANS - native MDL detok layer) matches the sign of (ITRANS - native tokens per word), with the CI excluding 0", applied only where native and ITRANS tokens per word
differ by at least 1. Reported next to the four Phase 1 models (stored results/m14_full/gate2/paired.csv values are recomputed here from their per-item files by the same function).
Output: results/phase2/x13/<model>/mdl_analysis.json. Usage: python scripts/x13_mdl_analyse.py [--model qwen3-8b]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import m14_gate2 as G  # noqa: E402

from shattered.runlog import REPO, results_dir, write_json  # noqa: E402


def load_forms(base: Path) -> dict:
    d = {"res": {f: json.load(open(base / f"{f}.json")) for f in ("native", "itrans")},
         "items": {f: dict(np.load(base / f"items_{f}.npz")) for f in ("native", "itrans")}}
    n, it = d["items"]["native"], d["items"]["itrans"]
    for k in ("mdl_order", "labels", "probe_train_mask", "in_e0"):
        assert np.array_equal(n[k], it[k]), f"native/ITRANS not paired on {k}"
    d["L"] = d["res"]["native"]["n_layers"]
    return d


def summarize(d: dict) -> dict:
    p = G.paired_mdl(d)
    tn, ti = d["res"]["native"]["tokens_per_word_mean"], d["res"]["itrans"]["tokens_per_word_mean"]
    lo, hi = p["diff_ci"]
    sign_ci = 1 if lo > 0 else -1 if hi < 0 else 0
    want = int(np.sign(ti - tn))
    return {"n_layers": d["L"], "mdl_detok_native": p["native"], "mdl_detok_itrans": p["itrans"], "itrans_minus_native": p["diff"], "ci95": [float(lo), float(hi)], "frac_depth_diff": p["diff_frac_depth"],
            "tokens_per_word_native": tn, "tokens_per_word_itrans": ti, "tpw_difference_at_least_1": bool(abs(ti - tn) >= 1), "expected_sign_from_tpw": want, "ci_sign": sign_ci,
            "H3_pattern_met": bool(abs(ti - tn) >= 1 and sign_ci == want), "n_words_occurrences": p["n"]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen3-8b")
    a = ap.parse_args()
    st = json.load(open(REPO / "results" / "kaggle" / "queue_state.json"))
    a2 = REPO / "results" / "kaggle" / "acct2" / "queue_state.json"  # models run on the second Kaggle account
    if a2.exists():
        st["mdl"] = {**json.load(open(a2)).get("mdl", {}), **st.get("mdl", {})}
    base = REPO / st["mdl"][a.model]["dir"]
    out = {"model": a.model, "this_model": summarize(load_forms(base)), "phase1_models": {}}
    for m in G.MODELS:
        out["phase1_models"][m] = summarize(load_forms(REPO / "results" / "m14_full" / m))
    write_json(results_dir(f"phase2/x13/{a.model}") / "mdl_analysis.json", out, {"registration": "RESULTS.md Amendment 2, X13 (MDL run; reading = Phase 1 H3 text as in R4)"})
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
