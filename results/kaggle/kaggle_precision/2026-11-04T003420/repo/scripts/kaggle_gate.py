"""Kaggle reproducibility gate (registered in RESULTS.md, 2026-11-02, before it is run): rescore 100 SIB-200 items x 3 forms
(native, ITRANS, lossy) with two Phase 1 models on the Kaggle T4 and compare with the laptop scores in results/e0c_sib/scores.

The forms are built from the public SIB-200 Kannada text (Davlan/sib200, the Phase 1 revision) with the project's own ITRANS and lossy
code, so no FLORES+ text leaves the laptop. The same 100 ids as `e0c_sib.load_items(limit=100)` (default_rng(0)) are used.
T4 has no bf16: each model is run in float16 first and, if the gate fails or a value is non-finite, in float32. Reported per model,
dtype and form: max and mean |d logprob| against the laptop (bf16), raw-prediction agreement, accuracy on both, the number of
non-finite log-probs, the prompt-token agreement with the laptop run, the largest absolute hidden state (fp16 overflow check, limit
65504), and wall time. Usage: python scripts/kaggle_gate.py --out DIR [--models sarvam-1 gemma4-e2b]
"""
import argparse
import json
import sys
import time
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
import torch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from shattered.eval.loglik import VERBALIZERS, build_prompt, choice_logprobs  # noqa: E402
from shattered.interp.load import load  # noqa: E402
from shattered.translit import to_itrans, to_lossy  # noqa: E402

SIB_REPO, SIB_REV = "Davlan/sib200", "38977a667f6fc264d5c26ec57a01e16db040b358"
CATS = ["science/technology", "travel", "politics", "sports", "health", "entertainment", "geography"]
FORMS = ["native", "itrans", "lossy"]
# registered pass rule, per model and form: raw-prediction agreement >= 95/100, |accuracy difference| <= 0.03, no non-finite value,
# prompt tokens identical to the laptop run on every item, and no hidden state above 65504 (fp16 limit) in the check forward.
PASS = {"agree_min": 0.95, "acc_diff_max": 0.03, "hidden_max": 65504.0}


def items(laptop: Path, model: str) -> list[dict]:
    import os
    from huggingface_hub import hf_hub_download
    parts = [pd.read_csv(hf_hub_download(SIB_REPO, f"data/kan_Knda/{s}.tsv", repo_type="dataset", revision=SIB_REV,
                                         token=os.environ.get("HF_TOKEN")), sep="\t") for s in ("train", "dev", "test")]
    S = pd.concat(parts, ignore_index=True).sort_values("index_id", ignore_index=True)
    rows = []
    for i, t, c in zip(S.index_id, S.text, S.category):
        nat = unicodedata.normalize("NFC", t).strip()
        rows.append({"id": int(i), "label": CATS.index(c), "native": nat, "itrans": " ".join(to_itrans(w) for w in nat.split()),
                     "lossy": to_lossy(nat)})
    pick = np.random.default_rng(0).choice(len(rows), 100, replace=False)  # as e0c_sib.load_items(limit=100)
    return [rows[j] for j in pick]


def run(model_name: str, dtype_name: str, its: list[dict], laptop: Path) -> dict:
    dtype = {"float16": torch.float16, "float32": torch.float32, "bfloat16": torch.bfloat16}[dtype_name]
    t0 = time.time()
    model, tok = load(model_name, "cuda", dtype=dtype)
    res = {"model": model_name, "dtype": dtype_name, "load_s": time.time() - t0, "forms": {}}
    # fp16 overflow check: largest absolute hidden state over every layer for 5 native prompts
    hmax = 0.0
    with torch.no_grad():
        for it in its[:5]:
            ids = tok(build_prompt("sib", {"text": it["native"]}), return_tensors="pt").to(model.device)
            hs = model(**ids, output_hidden_states=True).hidden_states
            hmax = max(hmax, max(float(h.float().abs().max()) for h in hs))
    res["hidden_abs_max"] = hmax
    for f in FORMS:
        L = pd.read_parquet(laptop / f"{model_name}__{f}.parquet").set_index("id")
        t1, lp_new, lp_old, nonfinite, tok_equal = time.time(), [], [], 0, 0
        for it in its:
            lp, n_tok = choice_logprobs(model, tok, build_prompt("sib", {"text": it[f]}), VERBALIZERS["sib"])
            lp = np.asarray(lp, dtype=float)
            nonfinite += int((~np.isfinite(lp)).sum())
            old = np.asarray(L.loc[it["id"], "logprobs"], dtype=float)
            tok_equal += int(n_tok == int(L.loc[it["id"], "prompt_tokens"]))
            lp_new.append(lp)
            lp_old.append(old)
        a, b = np.stack(lp_new), np.stack(lp_old)
        lab = np.array([it["label"] for it in its])
        d = np.abs(a - b)
        ok_d = np.isfinite(d)
        res["forms"][f] = {"max_abs_dlogprob": float(d[ok_d].max()) if ok_d.any() else None,
                           "mean_abs_dlogprob": float(d[ok_d].mean()) if ok_d.any() else None,
                           "raw_pred_agreement": float((a.argmax(1) == b.argmax(1)).mean()),
                           "acc_kaggle_raw": float((a.argmax(1) == lab).mean()), "acc_laptop_raw": float((b.argmax(1) == lab).mean()),
                           "non_finite_values": nonfinite, "prompt_tokens_equal": f"{tok_equal}/{len(its)}", "seconds": time.time() - t1}
        g = res["forms"][f]
        g["acc_diff"] = g["acc_kaggle_raw"] - g["acc_laptop_raw"]
        g["pass"] = bool(g["raw_pred_agreement"] >= PASS["agree_min"] and abs(g["acc_diff"]) <= PASS["acc_diff_max"]
                         and nonfinite == 0 and tok_equal == len(its))
    res["pass"] = bool(all(g["pass"] for g in res["forms"].values()) and hmax < PASS["hidden_max"])
    del model
    torch.cuda.empty_cache()
    return res


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--models", nargs="+", default=["sarvam-1", "gemma4-e2b"])
    ap.add_argument("--laptop", default=str(REPO / "results" / "e0c_sib" / "scores"))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    laptop = Path(a.laptop)
    its = items(laptop, "")
    results = []
    for m in a.models:
        for dt in ("float16", "float32"):
            try:
                r = run(m, dt, its, laptop)
            except Exception as e:  # noqa: BLE001 - reported, not hidden
                r = {"model": m, "dtype": dt, "error": repr(e)[:500], "pass": False}
            results.append(r)
            print(json.dumps(r, default=str), flush=True)
            (out / "gate.json").write_text(json.dumps({"rule": PASS, "results": results}, indent=1, default=str))
            if r.get("pass"):
                break  # the first dtype that passes is the dtype used for that model on Kaggle
    final = {m: next((r["dtype"] for r in results if r["model"] == m and r.get("pass")), None) for m in a.models}
    (out / "gate.json").write_text(json.dumps({"rule": PASS, "results": results, "dtype_used": final,
                                               "gate_passed": all(v is not None for v in final.values())}, indent=1, default=str))
    print("dtype_used", final)


if __name__ == "__main__":
    main()
