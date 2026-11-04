"""Matched-sample accuracy and tokens per word for the paper's main tables (descriptive, 2026-10-22, no verdict).

Every form on the same items, so the forms can be read side by side:
- sentiment: the 200 E0b items (natural: the 198 with a clean natural romanization; the paired contrasts in Gate 1
  and the ladder use those 198);
- SIB-200: the 257 SIB items in the retained M4c sample, the only SIB items with a natural romanization;
- M4c sample: the 496 retained FLORES+ sentences (tokens per word only; retrieval is in results/m4c_natural and
  results/l_ladder on the 248 test-half sentences).
Accuracy uses the stored item scores (results/e0b_familiarity/scores, results/e0c_sib/scores; natural on SIB =
the ladder's `natural257` scores) and the primary calibration with its raw-fallback rule, decided on the full English
rows exactly as in Gate 1 and E0c; the 257-item subset is taken after calibration. Missing score files are skipped and
reported. CPU only; no model is run.

Usage: python scripts/matched_samples.py     Outputs: results/matched/{accuracy.csv, tokens_per_word.csv}
"""
import json
import sys

import numpy as np
import pandas as pd

from shattered.runlog import REPO, results_dir, write_json

sys.path.insert(0, str(REPO / "scripts"))
import e0b_familiarity as e0b  # noqa: E402
import l_ladder as lad  # noqa: E402

MODELS = lad.ACC_MODELS
FORMS = ["english", "native", "itrans", "lower", "lossy", "natural"]


def sib257_ids() -> set:
    return {it["id"] for it in lad.sib257_items()["sib"]}


def tokens() -> pd.DataFrame:
    from transformers import AutoTokenizer
    from m14_full import flores_forms
    from shattered.interp.load import MODELS as REPOS
    a = lad.e0b_items()
    c, s = lad.e0c_items(), lad.sib257_items()
    ids = {it["id"] for it in s["sib"]}
    nat257 = {it["id"]: it["forms"]["natural257"]["text"] for it in s["sib"]}
    sib = [it for it in c["sib"] if it["id"] in ids]
    F = flores_forms()
    R, keep, native = lad.m4c_sample()
    sets = {"sentiment": {f: [v for it in a["sentiment"] if not (f == "natural" and it.get("natural_defective"))
                              for v in it["forms"][f].values()] for f in FORMS},
            "sib257": {**{f: [it["forms"][f]["text"] for it in sib] for f in FORMS if f != "natural"},
                       "natural": [nat257[it["id"]] for it in sib]},
            "m4c496": {"english": [F["english"][r["index"]] for r, k in zip(R, keep) if k],
                       "native": [t for t, k in zip(native, keep) if k],
                       "itrans": [F["itrans"][r["index"]] for r, k in zip(R, keep) if k],
                       "lower": [lad.to_lower(t) for t, k in zip(native, keep) if k],
                       "lossy": [lad.to_lossy(t) for t, k in zip(native, keep) if k],
                       "natural": [r["natural"] for r, k in zip(R, keep) if k]}}
    out = []
    for m in MODELS:
        tok = AutoTokenizer.from_pretrained(REPOS[m])
        for d, forms in sets.items():
            for f, T in forms.items():
                n = sum(len(x) for x in tok(T, add_special_tokens=False)["input_ids"])
                out.append({"model": m, "dataset": d, "form": f, "n_texts": len(T),
                            "tokens_per_word": n / sum(len(x.split()) for x in T)})
    return pd.DataFrame(out)


def load_scores(score_dir, forms) -> tuple[pd.DataFrame, list]:
    parts, missing = [], []
    for m in MODELS:
        for f in forms:
            p = score_dir / f"{m}__{f}.parquet"
            if p.exists():
                parts.append(pd.read_parquet(p))
            else:
                missing.append(str(p.relative_to(REPO)))
    return pd.concat(parts, ignore_index=True), missing


def accuracy() -> tuple[pd.DataFrame, list]:
    rows, missing = [], []
    B, mb = load_scores(lad.E0B_DIR, ["english", "native", "itrans", "lower", "lossy", "natural"])
    B, _ = e0b.apply_calibration(B, {m: json.load(open(lad.E0B_DIR / f"cf_{m}.json")) for m in MODELS})
    C, mc = load_scores(lad.E0C_DIR, ["english", "native", "itrans", "lower", "lossy", "natural257"])
    C, _ = e0b.apply_calibration(C, {m: json.load(open(lad.E0C_DIR / f"cf_{m}.json")) for m in MODELS})
    missing += mb + mc
    C = C.assign(form=C.form.replace({"natural257": "natural"}))
    ids = sib257_ids()
    for df, task, sample in ((B[B.task == "sentiment"], "sentiment", "all 200 (natural: 198 clean)"),
                             (C[C.id.isin(ids)], "sib", "257 SIB items with natural")):
        for (m, f), g in df.groupby(["model", "form"]):
            c = (g.pred_cal == g.label).to_numpy().astype(float)
            lo, hi = e0b.bootstrap_ci(c)
            rows.append({"model": m, "task": task, "sample": sample, "form": f, "n": len(g), "acc_cal": c.mean(),
                         "acc_cal_ci_low": lo, "acc_cal_ci_high": hi})
    return pd.DataFrame(rows), missing


def main() -> None:
    out = results_dir("matched")
    T = tokens()
    T.to_csv(out / "tokens_per_word.csv", index=False)
    A, missing = accuracy()
    A.to_csv(out / "accuracy.csv", index=False)
    # sanity: sentiment accuracy for the Gate 1 forms equals results/e0b_familiarity/gate1/accuracy.csv
    g1 = pd.read_csv(REPO / "results/e0b_familiarity/gate1/accuracy.csv")
    g1 = g1[g1.task == "sentiment"].set_index(["model", "form"]).acc_cal
    s = A[A.task == "sentiment"].set_index(["model", "form"]).acc_cal
    common = g1.index.intersection(s.index)
    assert np.allclose(g1.loc[common], s.loc[common]), "matched sentiment accuracy differs from Gate 1"
    write_json(out / "provenance.json", {"missing_score_files": missing, "n_sib257": len(sib257_ids()),
                                         "gate1_sentiment_check_cells": len(common)},
               {"status": "descriptive, 2026-10-22, no verdict"})
    print(f"accuracy rows {len(A)}, tokens rows {len(T)}, missing score files {missing}")


if __name__ == "__main__":
    main()
