"""X11, Arm A (registered, Amendment 2): quantization control on Qwen3.5-2B (laptop).

Qwen3.5-2B in 4-bit NF4 (bitsandbytes, double quantisation, bf16 compute) rerun on SIB-200 (1,004 items; forms native, ITRANS, lowercase, lossy, plus English for the calibration fallback rule), T1
template, calibrated as Phase 1 (mean of the three content-free inputs, raw fallback rule), against its stored full-precision (bf16) Phase 1 results on the same items (`results/e0c_sib/scores`).
Reported: accuracy per form and the change (4-bit minus bf16) with exact McNemar and a paired bootstrap CI (10,000, seed 0), and the change in the native-minus-ITRANS gap with its CI. No retrieval.
Prediction: quantization does not change the picture. SUPPORTED: every form's accuracy change is within 3 points (point estimate) and the 95% CI of the gap change lies within +-5 points.
REFUTED: any form changes by more than 5 points with the CI excluding 0. PARTLY SUPPORTED: otherwise. (Arm B is optional and descriptive and is not built.)
Usage: python scripts/x11.py score | analyse        Output: results/phase2/x11/
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from statsmodels.stats.contingency_tables import mcnemar

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e0b_familiarity as e0b  # noqa: E402
import l_ladder as lad  # noqa: E402

from shattered.eval.loglik import VERBALIZERS, build_prompt, choice_logprobs  # noqa: E402
from shattered.interp.load import load  # noqa: E402
from shattered.runlog import REPO, results_dir, write_json  # noqa: E402

MODEL, TAG = "qwen3.5-2b", "qwen3.5-2b-4bit"
FORMS = ["english", "native", "itrans", "lower", "lossy"]
OUT = results_dir("phase2/x11")
BF16 = REPO / "results" / "e0c_sib" / "scores"
N_BOOT = 10_000


def score() -> None:
    items = lad.e0c_items()
    its = items["sib"]
    t0 = time.time()
    model, tok = load(MODEL, "cuda", dtype=torch.bfloat16, quant="4bit")
    (OUT / "load.json").write_text(json.dumps({"quantization": "bitsandbytes NF4, double quantisation, bf16 compute", "load_seconds": time.time() - t0,
                                               "cuda_memory_gib": torch.cuda.memory_allocated() / 2**30}, indent=1))
    cf = {x: {"sib": choice_logprobs(model, tok, build_prompt("sib", {"text": x}), VERBALIZERS["sib"])[0]} for x in ["N/A", "", "[MASK]"]}
    (OUT / f"cf_{TAG}.json").write_text(json.dumps(cf, indent=1))
    for f in FORMS:
        path = OUT / f"{TAG}__{f}.parquet"
        if path.exists():
            continue
        t1, rows = time.time(), []
        for it in its:
            lp, n_tok = choice_logprobs(model, tok, build_prompt("sib", it["forms"][f]), VERBALIZERS["sib"])
            rows.append({"model": TAG, "task": "sib", "form": f, "id": it["id"], "label": it["label"], "logprobs": lp, "prompt_tokens": n_tok})
        pd.DataFrame(rows).to_parquet(path)
        print(f, len(rows), f"{time.time() - t1:.0f}s", flush=True)


def paired(a: np.ndarray, b: np.ndarray) -> dict:
    d = a.astype(float) - b.astype(float)
    idx = np.random.default_rng(0).integers(0, len(d), (N_BOOT, len(d)))
    m = d[idx].mean(1)
    return {"diff": float(d.mean()), "ci95": [float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))]}


def analyse() -> None:
    e0b.CHANCE.setdefault("sib", 1 / 7)
    q = pd.concat([pd.read_parquet(OUT / f"{TAG}__{f}.parquet") for f in FORMS], ignore_index=True)
    q, fq = e0b.apply_calibration(q, {TAG: json.load(open(OUT / f"cf_{TAG}.json"))})
    b = pd.concat([pd.read_parquet(BF16 / f"{MODEL}__{f}.parquet") for f in FORMS], ignore_index=True)
    b, fb = e0b.apply_calibration(b, {MODEL: json.load(open(BF16 / f"cf_{MODEL}.json"))})
    corr = {}
    for nm, df in (("q4", q), ("bf16", b)):
        piv = df.pivot_table(index="id", columns="form", values="pred_cal")
        lab = df.drop_duplicates("id").set_index("id").label.loc[piv.index]
        corr[nm] = piv.eq(lab, axis=0)
    ids = corr["q4"].index.intersection(corr["bf16"].index)
    res = {"n_items": int(len(ids)), "raw_fallback_4bit": bool(fq.use_raw.any()), "raw_fallback_bf16": bool(fb.use_raw.any()), "forms": {}}
    for f in FORMS:
        a, c = corr["q4"].loc[ids, f].to_numpy(), corr["bf16"].loc[ids, f].to_numpy()
        tb = [[int((a & c).sum()), int((a & ~c).sum())], [int((~a & c).sum()), int((~a & ~c).sum())]]
        res["forms"][f] = {"acc_4bit": float(a.mean()), "acc_bf16": float(c.mean()), "change": paired(a, c), "mcnemar_p": float(mcnemar(tb, exact=True).pvalue),
                           "only_4bit_correct": tb[0][1], "only_bf16_correct": tb[1][0]}
    gq = corr["q4"].loc[ids, "native"].to_numpy().astype(float) - corr["q4"].loc[ids, "itrans"].to_numpy().astype(float)
    gb = corr["bf16"].loc[ids, "native"].to_numpy().astype(float) - corr["bf16"].loc[ids, "itrans"].to_numpy().astype(float)
    res["gap_native_minus_itrans"] = {"gap_4bit": float(gq.mean()), "gap_bf16": float(gb.mean()), "change": paired(gq, gb)}
    tested = [f for f in FORMS if f != "english"]  # the four registered forms
    within3 = all(abs(res["forms"][f]["change"]["diff"]) <= 0.03 for f in tested)
    gap_ok = all(abs(x) <= 0.05 for x in res["gap_native_minus_itrans"]["change"]["ci95"])
    big = [f for f in tested if abs(res["forms"][f]["change"]["diff"]) > 0.05 and not (res["forms"][f]["change"]["ci95"][0] <= 0 <= res["forms"][f]["change"]["ci95"][1])]
    res["verdict"] = "supported" if within3 and gap_ok else "refuted" if big else "partly supported"
    res["rule_check"] = {"every_form_within_3_points": within3, "gap_change_ci_within_5_points": gap_ok, "forms_changed_by_more_than_5_points_with_ci_excluding_0": big}
    write_json(OUT / "analysis.json", res, {"registration": "RESULTS.md X11 Arm A", "label": "label: exploratory control, 4-bit NF4 with double quantisation, bf16 compute"})
    print(json.dumps({"verdict": res["verdict"], "forms": {f: (round(v["acc_4bit"], 3), round(v["acc_bf16"], 3), round(v["change"]["diff"], 3)) for f, v in res["forms"].items()},
                      "gap": res["gap_native_minus_itrans"], "rule": res["rule_check"]}, indent=1))


if __name__ == "__main__":
    {"score": score, "analyse": analyse}[sys.argv[1]]()
