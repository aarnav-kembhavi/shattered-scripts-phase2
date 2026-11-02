"""A1-P per-model precision check (Amendment 2): for each model without a laptop baseline, score the gate's 100 SIB-200 items x 3 forms
(native, ITRANS, lossy) in float16 and in a reference precision: float32 if it fits 2 x T4 (weights x 4 bytes <= 24 GiB), else 8-bit
(bitsandbytes LLM.int8, stated in the output). The model counts only if, per form, raw-label agreement float16 vs reference >= 0.98 and
|accuracy difference| <= 0.01, no non-finite value, and reported: max |hidden state| in float16 (limit 65504), mean/max |d logprob| fp16 vs
reference. Models are sharded over both GPUs (device_map auto). One result file per model (resumable).
Usage: python scripts/kaggle_precision.py --out DIR --models qwen3-8b ambari-7b-base
"""
import argparse
import gc
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from kaggle_gate import FORMS, items  # noqa: E402
from shattered.eval.loglik import VERBALIZERS, build_prompt, choice_logprobs  # noqa: E402
from shattered.interp.load import MODELS, load  # noqa: E402

RULE = {"agree_min": 0.98, "acc_diff_max": 0.01, "hidden_max": 65504.0}


def score(model, tok, its, hidden=False) -> dict:
    out = {"lp": {}, "nonfinite": 0, "hidden_abs_max": None}
    if hidden:
        hmax = 0.0
        with torch.no_grad():
            for it in its[:5]:
                ids = tok(build_prompt("sib", {"text": it["native"]}), return_tensors="pt").to(model.device)
                hmax = max(hmax, max(float(h.float().abs().max()) for h in model(**ids, output_hidden_states=True).hidden_states))
        out["hidden_abs_max"] = hmax
    for f in FORMS:
        a = np.stack([np.asarray(choice_logprobs(model, tok, build_prompt("sib", {"text": it[f]}), VERBALIZERS["sib"])[0], float) for it in its])
        out["nonfinite"] += int((~np.isfinite(a)).sum())
        out["lp"][f] = a
    return out


def free(model) -> None:
    del model
    gc.collect()
    torch.cuda.empty_cache()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--models", nargs="+", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    its = items(None, "")
    lab = np.array([it["label"] for it in its])
    from huggingface_hub import HfApi
    for m in a.models:
        f_out = out / f"precision_{m}.json"
        if f_out.exists():
            continue
        t0 = time.time()
        r = {"model": m, "repo": MODELS[m], "rule": RULE}
        try:
            info = HfApi().model_info(MODELS[m])
            n_par = (info.safetensors.total if info.safetensors else None)
            r["parameters"] = n_par
            ref_kind = "float32" if (n_par and n_par * 4 / 2**30 <= 24) else "8bit"
            r["reference"] = ref_kind
            model, tok = load(m, "auto", dtype=torch.float16)
            h = score(model, tok, its, hidden=True)
            free(model)
            model, tok = load(m, "auto", dtype=torch.float32) if ref_kind == "float32" else load(m, "auto", dtype=torch.float16, quant="8bit")
            ref = score(model, tok, its)
            free(model)
            r.update({"hidden_abs_max_fp16": h["hidden_abs_max"], "nonfinite_fp16": h["nonfinite"], "nonfinite_ref": ref["nonfinite"], "forms": {}})
            for f in FORMS:
                x, y = h["lp"][f], ref["lp"][f]
                d = np.abs(x - y)
                ok = np.isfinite(d)
                g = {"raw_agreement": float((x.argmax(1) == y.argmax(1)).mean()), "acc_fp16": float((x.argmax(1) == lab).mean()),
                     "acc_ref": float((y.argmax(1) == lab).mean()), "mean_abs_dlogprob": float(d[ok].mean()), "max_abs_dlogprob": float(d[ok].max())}
                g["acc_diff"] = g["acc_fp16"] - g["acc_ref"]
                g["pass"] = bool(g["raw_agreement"] >= RULE["agree_min"] and abs(g["acc_diff"]) <= RULE["acc_diff_max"] + 1e-9)
                r["forms"][f] = g
            r["pass"] = bool(all(g["pass"] for g in r["forms"].values()) and r["nonfinite_fp16"] == 0 and r["nonfinite_ref"] == 0
                             and h["hidden_abs_max"] < RULE["hidden_max"])
        except Exception as e:  # noqa: BLE001 - reported
            r.update({"error": repr(e)[:600], "pass": False})
        r["seconds"] = time.time() - t0
        f_out.write_text(json.dumps(r, indent=1))
        print(json.dumps({k: v for k, v in r.items() if k != "rule"}), flush=True)


if __name__ == "__main__":
    main()
