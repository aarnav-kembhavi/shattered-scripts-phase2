"""X4 ladder, accuracy part (registered, Phase 2 pre-registration, X4: Ladder L1-L3): L1 = lowercase minus ITRANS, L2 = lossy minus lowercase, L3 = natural minus lossy (on the natural ids), on SIB-200 accuracy
and IndicSentiment accuracy, the counted accuracy models of the language (r1.json), exact McNemar with Holm within each task over contrasts x counted models, and the enlarged-set effect rule (an effect is
"positive" or "negative" when it is significant in that direction in at least n - 1 of the n counted models, otherwise "no effect detected"; the Phase 1 rule was 3 of 4). The retrieval part of the ladder (M4c rows)
is in scripts/x4_r3.py. The lowercase form is the E9 scheme found for the language (scripts/x4_e9.py).
Usage: python scripts/x4_ladder.py       Output: results/phase2/x4/<lang>/ladder_acc.json"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e0b_familiarity as e0b  # noqa: E402

from shattered.runlog import REPO, write_json  # noqa: E402

E0B = REPO / "results" / "e0b_familiarity" / "scores"
E0C = REPO / "results" / "e0c_sib" / "scores"
CONTRASTS = [("lower", "itrans"), ("lossy", "lower"), ("natural", "lossy")]
NAMES = {("lower", "itrans"): "L1", ("lossy", "lower"): "L2", ("natural", "lossy"): "L3"}


def run(lang: str) -> dict:
    r1 = json.load(open(REPO / "results" / "phase2" / "x4" / lang / "r1.json", encoding="utf-8"))
    models = r1["counted_models"]
    n = len(models)
    out = {"language": lang, "counted_models": models, "tasks": {}}
    for task, eng_dir in (("sib", E0C), ("sentiment", E0B)):
        base = REPO / "results" / "phase2" / "x4" / lang / "scores" / task
        e0b.CHANCE.setdefault("sib", 1 / 7)
        e0b.CHANCE.setdefault("sentiment", 0.5)
        parts, cf = [], {}
        for m in models:
            for f in ("itrans", "lower", "lossy") + (("natural",) if task == "sib" else ()):  # natural drafts exist only for the SIB-200 ids
                parts.append(pd.read_parquet(base / f"{m}__{f}.parquet"))
            en = pd.read_parquet(eng_dir / f"{m}__english.parquet")
            parts.append(en[en.task == task])
            cf[m] = json.load(open(base / f"cf_{m}.json"))
        df = pd.concat(parts, ignore_index=True)[["model", "task", "form", "id", "label", "logprobs"]]
        df, fb = e0b.apply_calibration(df, cf)
        contrasts = CONTRASTS if task == "sib" else CONTRASTS[:2]  # L3 (natural minus lossy) needs natural drafts: SIB-200 only
        mc = e0b.mcnemar_table(df[df.form.isin(["itrans", "lower", "lossy", "natural"])], contrasts)
        rows = mc.to_dict("records")
        res = {}
        for a, b in contrasts:
            g = mc[(mc.a == a) & (mc.b == b)]
            pos = int(((g["diff"] > 0) & g.significant).sum())
            neg = int(((g["diff"] < 0) & g.significant).sum())
            res[NAMES[(a, b)]] = {"contrast": f"{a} minus {b}", "n_counted": n, "significant_positive": pos, "significant_negative": neg,
                                  "verdict": "effect, positive" if pos >= n - 1 else "effect, negative" if neg >= n - 1 else "no effect detected",
                                  "by_model": {r.model: {"acc_a": float(r.acc_a), "acc_b": float(r.acc_b), "diff": float(r.diff), "p_holm": float(r.p_holm), "n": int(r.n)} for r in g.itertuples()}}
        out["tasks"][task] = {"raw_fallback_rows": fb[fb.use_raw][["model", "task"]].to_dict("records"), "ladder": res, "tests": rows}
    write_json(REPO / "results" / "phase2" / "x4" / lang / "ladder_acc.json", out, {"registration": "RESULTS.md X4 (ladder, accuracy)"})
    return out


if __name__ == "__main__":
    for lang in ("bn", "te"):
        o = run(lang)
        for t, v in o["tasks"].items():
            print(lang, t, {k: (x["verdict"], x["significant_positive"], x["significant_negative"]) for k, x in v["ladder"].items()})
