"""Kaggle queue driver (Amendment 2, approved 2026-11-02): A1-R retrieval gate (read from its fetched output) -> A1-P precision checks -> X12 scoring ->
X13 scoring, one Kaggle job at a time, deciding each step from the registered rules, retrying Hugging Face access between jobs. Idempotent and resumable:
state in results/kaggle/queue_state.json; every decision is logged with the rule it applies. A model is scored only after it passed A1-P; retrieval is
requested only if A1-R passed. Each job goes through scripts/kaggle_runner.py (quota, 12 h cap, commit, hardware record).
Usage: python scripts/kaggle_queue.py [--once]
"""
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
K = REPO / "results" / "kaggle"
STATE = K / "queue_state.json"
PY = str(REPO / ".venv" / "Scripts" / "python.exe")
PRIVATE = "shattered-flores-private"
X12 = ["ambari-7b-base", "llama-2-7b", "ambari-7b-instruct-v0.1", "ambari-7b-instruct-v0.2"]  # X12 endpoints (exempt from the counting rule, subject to A1-P)
X13 = ["qwen3-8b", "llama-3.1-8b"]  # plus the largest Sarvam that fits (named by the screen, added to the state when chosen)
SCORE_ENDPOINTS = ["ambari-7b-base", "llama-2-7b"]  # X12 contrast 1 scoring; the two instruct models enter contrast 2 (MDL job, not scoring)


def state() -> dict:
    return json.loads(STATE.read_text()) if STATE.exists() else {"log": [], "precision": {}, "scored": {}, "a1r": None}


def save(s: dict) -> None:
    STATE.write_text(json.dumps(s, indent=1))


def log(s: dict, msg: str) -> None:
    s["log"].append(f"{time.strftime('%F %T')} {msg}")
    print(msg, flush=True)
    save(s)


def accessible(model: str) -> bool:
    sys.path.insert(0, str(REPO / "src"))
    from dotenv import load_dotenv
    load_dotenv(REPO / ".env")
    import os
    from huggingface_hub import hf_hub_download
    from shattered.interp.load import MODELS
    try:
        hf_hub_download(MODELS[model], "config.json", token=os.environ.get("HF_TOKEN"))
        return True
    except Exception:  # noqa: BLE001 - gated or missing
        return False


def push(job: str, args: list[str], hours: float, include: list[str] | None = None) -> dict:
    cmd = [PY, "scripts/kaggle_runner.py", "run", job, "--timeout-h", str(hours), "--private-data", PRIVATE]
    if include:
        cmd += ["--include", *include]
    cmd += ["--", *args]
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    (K / f"{job}_queue_run.log").write_text((r.stdout or "") + (r.stderr or ""), encoding="utf-8")
    last = json.loads((K / job / "last_run.json").read_text())
    return {"rc": r.returncode, "dir": REPO / last["output_dir"], "status": last["status"], "hours": last["hours"], "commit": last["commit"]}


def read_a1r(s: dict) -> None:
    """The A1-R verdict is `results/kaggle/a1r_result.json` (Kaggle output compared with the laptop summary locally; the in-kernel flag is not used,
    the laptop summary is not in the Kaggle package)."""
    p = K / "a1r_result.json"
    if p.exists():
        g = json.loads(p.read_text())
        if s["a1r"] != {"gate_passed": g["gate_passed"]}:
            s["a1r"] = {"gate_passed": g["gate_passed"]}
            log(s, f"A1-R read: gate_passed={g['gate_passed']}")


def ingest_precision(s: dict) -> None:
    """Take up every fetched precision result not yet in the state (also those of a push whose driver was stopped)."""
    for f in sorted((K / "kaggle_precision").glob("*/out/precision_*.json")):
        d = json.loads(f.read_text())
        if d["model"] not in s["precision"]:
            s["precision"][d["model"]] = {"pass": d.get("pass"), "reference": d.get("reference"), "hidden_abs_max_fp16": d.get("hidden_abs_max_fp16"),
                                          "file": str(f.relative_to(REPO)), "error": d.get("error")}
            log(s, f"A1-P {d['model']}: pass={d.get('pass')} reference={d.get('reference')} error={d.get('error')}")


def precision(s: dict, models: list[str]) -> None:
    ingest_precision(s)
    models = [m for m in models if m not in s["precision"] and accessible(m)]
    if not models:
        return
    r = push("kaggle_precision", ["--models", *models], 1.0 + 0.6 * len(models))
    for m in models:
        f = r["dir"] / "out" / f"precision_{m}.json"
        if f.exists():
            d = json.loads(f.read_text())
            s["precision"][m] = {"pass": d.get("pass"), "reference": d.get("reference"), "hidden_abs_max_fp16": d.get("hidden_abs_max_fp16"),
                                 "file": str(f.relative_to(REPO)), "commit": r["commit"], "error": d.get("error")}
            log(s, f"A1-P {m}: pass={d.get('pass')} reference={d.get('reference')} error={d.get('error')}")
        else:
            log(s, f"A1-P {m}: no result file (kernel status {r['status']})")


def score(s: dict, model: str, hours: float) -> None:
    if model in s["scored"] or not s["precision"].get(model, {}).get("pass"):
        return
    retrieval = bool(s["a1r"] and s["a1r"]["gate_passed"])
    args = ["--models", model] + ([] if retrieval else ["--no-retrieval"])
    r = push("x_score", args, hours, include=["results/e09_romanize/best_schemes.json"])
    done = (r["dir"] / "out" / model / "done.json").exists()
    s["scored"][model] = {"done": done, "retrieval_requested": retrieval, "dir": str((r["dir"] / "out" / model).relative_to(REPO)), "hours": r["hours"],
                          "commit": r["commit"], "status": r["status"]}
    log(s, f"score {model}: done={done} retrieval={retrieval} hours={r['hours']:.2f}")


def main() -> None:
    s = state()
    read_a1r(s)
    if s["a1r"] is None:
        log(s, "A1-R result not available yet; run it first (scripts/kaggle_runner.py run kaggle_retrieval_gate)")
        return
    # A1-P for what is accessible now (Qwen3-8B, Ambari-7B-base, Ambari-7B-Instruct-v0.2; others when access arrives)
    precision(s, ["qwen3-8b", "ambari-7b-base"])
    for m in X12 + X13:
        precision(s, [m])  # retry access for the gated ones between jobs
    score(s, "ambari-7b-base", 5.0)
    score(s, "qwen3-8b", 5.0)
    for m in ("llama-2-7b", "llama-3.1-8b"):
        precision(s, [m])
        score(s, m, 5.0)
    save(s)
    log(s, "queue pass finished")


if __name__ == "__main__":
    main()
