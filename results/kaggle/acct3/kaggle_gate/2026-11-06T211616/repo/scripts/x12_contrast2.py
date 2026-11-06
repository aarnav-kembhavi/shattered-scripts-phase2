"""X12 contrast 2 (secondary; instruction-pair exposure contrast): MDL assembly layer for native Kannada words, Ambari-Instruct-v0.1 (Ambari-7B-base tokenizer, native 2.74 tokens per word) versus v0.2 (the original
Llama-2 tokenizer, native 20.83 tokens per word), the 300 Phase 1 probe words, Phase 1 protocol, fp16, both passed A1-P. Registered rule (as H3, descriptive): the sign of the layer difference (v0.2 minus v0.1)
matches the sign of the tokens-per-word difference, with the CI excluding 0; the more fragmented input is predicted to be assembled later. Word-clustered paired bootstrap (10,000, seed 0) as Phase 1 (`paired_mdl`
logic: the two models see the same words and occurrences). Accuracy differences between the models are exploratory. Caveat registered with the contrast: v0.1 is built on Ambari-7B-base-v0.1 and v0.2 on Llama-2,
so the pair is not a clean 'fragmentation with data fixed' test unless the base models are shown to match; reported as the comparison of the two released instruction models.
Output: results/phase2/x12/contrast2_mdl.json. Usage: python scripts/x12_contrast2.py"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shattered.interp.clustered import ci, first_reach, mdl_curves, weights  # noqa: E402
from shattered.runlog import REPO, results_dir, write_json  # noqa: E402

A, B = "ambari-7b-instruct-v0.1", "ambari-7b-instruct-v0.2"


def load(base: Path, form: str) -> tuple[dict, dict]:
    return json.load(open(base / f"{form}.json")), dict(np.load(base / f"items_{form}.npz"))


def main() -> None:
    st = json.load(open(REPO / "results" / "kaggle" / "acct2" / "queue_state.json"))
    out = {"models": {}}
    data = {}
    for m in (A, B):
        base = REPO / st["mdl"][m]["dir"]
        data[m] = {f: load(base, f) for f in ("native", "itrans")}
    # the two models keep slightly different numbers of occurrences (a few contexts are dropped for the more fragmented tokenizer), so the pairing is by WORD: both models see the same resampled words
    for f in ("native", "itrans"):
        la, lb = data[A][f][1]["labels"][data[A][f][1]["mdl_order"]], data[B][f][1]["labels"][data[B][f][1]["mdl_order"]]
        out.setdefault("occurrences", {})[f] = {A: int(len(la)), B: int(len(lb)), "words_in_both": int(len(np.intersect1d(la, lb)))}
    for m in (A, B):
        r = {}
        for f in ("native", "itrans"):
            j, it = data[m][f]
            c = it["mdl_costs"]
            r[f] = {"detok_layer": int(first_reach(1 / c.sum(1))), "tokens_per_word": j["tokens_per_word_mean"], "n_layers": j["n_layers"]}
        out["models"][m] = r
    res = {}
    for f in ("native", "itrans"):
        ca, cb = data[A][f][1]["mdl_costs"], data[B][f][1]["mdl_costs"]
        la, lb = data[A][f][1]["labels"][data[A][f][1]["mdl_order"]], data[B][f][1]["labels"][data[B][f][1]["mdl_order"]]
        uniq = np.union1d(la, lb)
        ia, ib = np.searchsorted(uniq, la), np.searchsorted(uniq, lb)
        rng = np.random.default_rng(0)
        parts = []
        for _ in range(10_000 // 500):
            cnt = rng.multinomial(len(uniq), np.full(len(uniq), 1 / len(uniq)), size=500).astype(np.float32)
            parts.append(first_reach(mdl_curves(cb, cnt[:, ib])) - first_reach(mdl_curves(ca, cnt[:, ia])))
        diffs = np.concatenate(parts)
        lo, hi = ci(diffs)
        d_layer = out["models"][B][f]["detok_layer"] - out["models"][A][f]["detok_layer"]
        d_tpw = out["models"][B][f]["tokens_per_word"] - out["models"][A][f]["tokens_per_word"]
        sign_ci = 1 if lo > 0 else -1 if hi < 0 else 0
        res[f] = {"v02_minus_v01_layer": d_layer, "ci95": [float(lo), float(hi)], "tokens_per_word_difference_v02_minus_v01": d_tpw, "sign_ci": sign_ci,
                  "sign_expected_from_tpw": int(np.sign(d_tpw)), "H3_pattern_met": bool(sign_ci == int(np.sign(d_tpw)) and sign_ci != 0)}
    out["contrast"] = res
    out["registered_form"] = "native"
    out["verdict_native"] = "pattern met (more fragmented input assembled later)" if res["native"]["H3_pattern_met"] else "pattern not met"
    write_json(results_dir("phase2/x12") / "contrast2_mdl.json", out, {"registration": "RESULTS.md Amendment 2, X12 contrast 2 (descriptive)"})
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
