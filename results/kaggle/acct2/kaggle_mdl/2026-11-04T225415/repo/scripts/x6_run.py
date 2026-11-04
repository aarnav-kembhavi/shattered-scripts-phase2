"""X6 run part 1 (registered: rule (3), counting): SIB-200 accuracy for the X6 shortlist models (Llama 3.2 1B base from the NousResearch mirror, deviation X6-D1; oroZ-1.7B-Indic-v1) in the forms
english, native, ITRANS, lowercase (E9 universal|lower), lossy, T1 template, calibrated as Phase 1, exactly the Phase 1 scoring code path (e0b.score_model). The model is counted if its native SIB-200
CI lower bound exceeds 0.40. Retrieval, the T2 template and the ladder follow only for counted models. Usage: python scripts/x6_run.py score | analyse   Output: results/phase2/x6/scores/, counting.json"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e0b_familiarity as e0b  # noqa: E402
import l_ladder as lad  # noqa: E402

from shattered.runlog import REPO, results_dir, write_json  # noqa: E402

MODELS = ["llama-3.2-1b", "oro-1.7b"]
FORMS = ["english", "native", "itrans", "lower", "lossy"]
OUT = results_dir("phase2/x6")
SC = OUT / "scores"


def score() -> None:
    SC.mkdir(parents=True, exist_ok=True)
    items = lad.e0c_items()
    for m in MODELS:
        e0b.score_model(m, {"sib": items["sib"]}, FORMS, SC)


def analyse() -> None:
    e0b.CHANCE.setdefault("sib", 1 / 7)
    out = {}
    for m in MODELS:
        df = pd.concat([pd.read_parquet(SC / f"{m}__{f}.parquet") for f in FORMS], ignore_index=True)
        df, fb = e0b.apply_calibration(df, {m: json.load(open(SC / f"cf_{m}.json"))})
        acc = e0b.accuracy_table(df)
        a = {r.form: {"n": int(r.n), "acc_cal": float(r.acc_cal), "ci95": [float(r.acc_cal_ci_low), float(r.acc_cal_ci_high)]} for r in acc.itertuples()}
        out[m] = {"accuracy": a, "raw_fallback_used": bool(fb.use_raw.any()), "native_ci_lower": a["native"]["ci95"][0], "counted": bool(a["native"]["ci95"][0] > 0.40),
                  "english_above_chance_plus_5": bool(a["english"]["acc_cal"] >= 1 / 7 + 0.05)}
    write_json(OUT / "counting.json", out, {"registration": "RESULTS.md X6, rule (3)"})
    print(json.dumps({m: {"counted": v["counted"], "native_ci_lower": round(v["native_ci_lower"], 3), **{f: round(x["acc_cal"], 3) for f, x in v["accuracy"].items()}} for m, v in out.items()}, indent=1))


if __name__ == "__main__":
    {"score": score, "analyse": analyse}[sys.argv[1]]()
