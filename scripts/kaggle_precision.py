"""A1-P per-model precision check (Amendment 2): for each model without a laptop baseline, score the gate's 100 SIB-200 items x 3 forms
(native, ITRANS, lossy) in float16 and in the reference precision: float32 with CPU offload (A1-P-D1, 2026-11-02; the earlier 8-bit LLM.int8
reference is withdrawn as an invalid ground truth). The model counts only if, per form, raw-label agreement float16 vs reference >= 0.98 and
|accuracy difference| <= 0.01, no non-finite value, and reported: max |hidden state| in float16 (limit 65504), mean/max |d logprob| fp16 vs
reference, and load / score / total seconds. Models are sharded over both GPUs (device_map auto; the reference keeps 12 GiB per GPU and the rest in
system RAM). **Each precision runs in its own subprocess** (worker mode), so the float16 weights are certainly gone from the GPUs when the float32
reference loads (the in-process version leaked them: A1-P-D1 note). One result file per model (resumable); an error result carries no verdict.
Usage: python scripts/kaggle_precision.py --out DIR --models qwen3-8b ambari-7b-base
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "src"))

RULE = {"agree_min": 0.98, "acc_diff_max": 0.01, "hidden_max": 65504.0}


def score(model, tok, its, hidden=False) -> dict:
    import torch
    from kaggle_gate import FORMS
    from shattered.eval.loglik import VERBALIZERS, build_prompt, choice_logprobs
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
        print(f"[score] form {f} done", flush=True)
        out["lp"][f] = a
    return out


def worker(kind: str, m: str, npz: Path) -> int:
    """One precision in a fresh process: load, score the 100 items x 3 forms, write the arrays and timings, exit."""
    import torch
    from kaggle_gate import items
    from shattered.interp.load import load
    its = items(None, "")
    t0 = time.time()
    try:
        print(f"[worker {kind} {m}] loading", flush=True)
        if kind == "fp16":
            model, tok = load(m, "auto", dtype=torch.float16)
        else:
            model, tok = load(m, "auto", dtype=torch.float32, offload=True)
        t_load = time.time() - t0
        print(f"[worker {kind} {m}] loaded in {t_load:.0f}s; scoring", flush=True)
        t1 = time.time()
        r = score(model, tok, its, hidden=(kind == "fp16"))
        np.savez(npz, **{f"lp_{f}": v for f, v in r["lp"].items()}, nonfinite=r["nonfinite"],
                 hidden=(r["hidden_abs_max"] if r["hidden_abs_max"] is not None else -1.0), load_s=t_load, score_s=time.time() - t1)
        return 0
    except Exception as e:  # noqa: BLE001 - reported by the parent
        npz.with_suffix(".err").write_text(repr(e)[:800])
        return 1


def run_worker(kind: str, m: str, tmp: Path) -> tuple[dict | None, str | None]:
    npz = tmp / f"{m}__{kind}.npz"
    for p in (npz, npz.with_suffix(".err")):
        p.unlink(missing_ok=True)
    subprocess.run([sys.executable, __file__, "--worker", kind, "--model", m, "--npz", str(npz)], check=False)
    if npz.exists():
        z = np.load(npz)
        return {k: z[k] for k in z.files}, None
    err = npz.with_suffix(".err")
    return None, (err.read_text() if err.exists() else "worker died without a result (killed or out of host memory)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--models", nargs="+")
    ap.add_argument("--worker")
    ap.add_argument("--model")
    ap.add_argument("--npz")
    a = ap.parse_args()
    if a.worker:
        sys.exit(worker(a.worker, a.model, Path(a.npz)))
    from huggingface_hub import HfApi
    from kaggle_gate import FORMS, items
    from shattered.interp.load import MODELS
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    its = items(None, "")
    lab = np.array([it["label"] for it in its])
    for m in a.models:
        f_out = out / f"precision_{m}.json"
        if f_out.exists():
            continue
        t0 = time.time()
        r = {"model": m, "repo": MODELS[m], "rule": RULE, "reference": "float32_offload"}
        try:
            info = HfApi().model_info(MODELS[m])
            r["parameters"] = info.safetensors.total if info.safetensors else None
        except Exception as e:  # noqa: BLE001
            r["parameters_error"] = repr(e)[:200]
        h, err = run_worker("fp16", m, out)
        ref, err2 = (None, "fp16 worker failed") if h is None else run_worker("ref", m, out)
        if h is None or ref is None:
            r.update({"error": err or err2, "pass": None, "note": "harness error: no verdict"})
        else:
            r.update({"hidden_abs_max_fp16": float(h["hidden"]), "nonfinite_fp16": int(h["nonfinite"]), "nonfinite_ref": int(ref["nonfinite"]),
                      "fp16_load_seconds": float(h["load_s"]), "fp16_score_seconds": float(h["score_s"]),
                      "ref_load_seconds": float(ref["load_s"]), "ref_score_seconds": float(ref["score_s"]), "forms": {}})
            for f in FORMS:
                x, y = h[f"lp_{f}"], ref[f"lp_{f}"]
                d = np.abs(x - y)
                ok = np.isfinite(d)
                g = {"raw_agreement": float((x.argmax(1) == y.argmax(1)).mean()), "acc_fp16": float((x.argmax(1) == lab).mean()),
                     "acc_ref": float((y.argmax(1) == lab).mean()), "mean_abs_dlogprob": float(d[ok].mean()), "max_abs_dlogprob": float(d[ok].max())}
                g["acc_diff"] = g["acc_fp16"] - g["acc_ref"]
                g["pass"] = bool(g["raw_agreement"] >= RULE["agree_min"] and abs(g["acc_diff"]) <= RULE["acc_diff_max"] + 1e-9)
                r["forms"][f] = g
            r["pass"] = bool(all(g["pass"] for g in r["forms"].values()) and r["nonfinite_fp16"] == 0 and r["nonfinite_ref"] == 0
                             and r["hidden_abs_max_fp16"] < RULE["hidden_max"])
        r["seconds"] = time.time() - t0
        f_out.write_text(json.dumps(r, indent=1))
        print(json.dumps({k: v for k, v in r.items() if k != "rule"}), flush=True)


if __name__ == "__main__":
    main()
