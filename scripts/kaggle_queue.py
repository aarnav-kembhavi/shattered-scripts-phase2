"""Kaggle queue driver (Amendment 2, approved 2026-11-02; order set by Aarnav 2026-11-02 23:16): A1-P pair (Qwen3-8B, Ambari-7B-base) -> score the ones that pass (X13 Qwen3-8B,
then X12 Ambari-base) -> A1-P Ambari-Instruct v0.1 and v0.2 (one push) -> X9b Sarvam-1 arm when its laptop pilot is done -> gated models retried between jobs. Weekly quota is projected before each push.
(earlier text:) A1-R retrieval gate (read from its fetched output) -> A1-P precision checks -> X12 scoring ->
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
INSTRUCT = ["ambari-7b-instruct-v0.1", "ambari-7b-instruct-v0.2"]  # X12 contrast 2 (instruction-pair exposure contrast): scored only if BOTH pass A1-P
X9B_SARVAM_H = 18.0  # registered: Sarvam-1 primary arm, 6 runs x about 3 GPU hours; the Qwen3.5-2B arm (9 h) is cut first if quota is short
WANT = ["qwen3-8b", "ambari-7b-base", "llama-2-7b", "llama-3.1-8b"] + INSTRUCT


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
    lr = K / job / "last_run.json"
    before = lr.stat().st_mtime if lr.exists() else None
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    (K / f"{job}_queue_run.log").write_text((r.stdout or "") + (r.stderr or ""), encoding="utf-8")
    if r.returncode != 0 or not lr.exists() or lr.stat().st_mtime == before:
        # the runner refused (e.g. dirty tree) or never pushed: never fall back to the previous run's last_run.json
        return None
    last = json.loads(lr.read_text())
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
        if d.get("reference") == "float32_offload" and d.get("pass") is not None and not d.get("error"):  # A1-P-D1 (2026-11-03): results against the withdrawn 8-bit reference are not used; sorted by run time: the latest result of a model wins (a re-run replaces an earlier one; both files stay on disk)
            s["precision"][d["model"]] = {"pass": d.get("pass"), "reference": d.get("reference"), "hidden_abs_max_fp16": d.get("hidden_abs_max_fp16"),
                                          "file": str(f.relative_to(REPO)), "error": d.get("error")}
            log(s, f"A1-P {d['model']}: pass={d.get('pass')} reference={d.get('reference')} error={d.get('error')}")


def precision(s: dict, models: list[str]) -> None:
    ingest_precision(s)
    models = [m for m in models if m not in s["precision"] and accessible(m)]
    if not models:
        return
    r = push("kaggle_precision", ["--models", *models], 2.0 + 1.5 * len(models))
    if r is None:
        log(s, f"A1-P {models}: runner did not push (see results/kaggle/kaggle_precision_queue_run.log); nothing recorded")
        return
    for m in models:
        f = r["dir"] / "out" / f"precision_{m}.json"
        if f.exists():
            d = json.loads(f.read_text())
            if d.get("error") or d.get("pass") is None:  # a harness error is not a verdict: nothing is recorded, the model stays queued
                log(s, f"A1-P {m}: harness error, no verdict, stays queued: {str(d.get('error'))[:200]}")
                continue
            s["precision"][m] = {"pass": d.get("pass"), "reference": d.get("reference"), "hidden_abs_max_fp16": d.get("hidden_abs_max_fp16"),
                                 "file": str(f.relative_to(REPO)), "commit": r["commit"], "error": d.get("error")}
            log(s, f"A1-P {m}: pass={d.get('pass')} reference={d.get('reference')} error={d.get('error')}")
        else:
            log(s, f"A1-P {m}: no result file (kernel status {r['status']})")


def x9b_ready() -> bool:
    return (REPO / "results" / "phase2" / "x9b" / "pilot_done.json").exists() and (REPO / "scripts" / "kaggle_x9b.py").exists()


def projection(s: dict, job: str, hours: float) -> bool:
    """Log the weekly-quota projection before a push (registered reserve: the X9b Sarvam arm). False = do not push now."""
    sys.path.insert(0, str(REPO / "scripts"))
    from kaggle_runner import WEEK_H, quota, used_hours
    used = used_hours(quota())
    head = WEEK_H - used - hours
    x9b_pending = not s.get("x9b_done")
    log(s, f"quota projection before {job}: {used:.2f} h used in the last 7 days, this push up to {hours:.1f} h, headroom {head:.1f} h, "
           f"X9b Sarvam reserve {X9B_SARVAM_H:.0f} h (X9b ready: {x9b_ready()})")
    if x9b_pending and x9b_ready() and head < X9B_SARVAM_H:
        log(s, f"X9b Sarvam goes first: {job} would leave under {X9B_SARVAM_H:.0f} h of headroom; {job} is deferred")
        return False
    return True


def score(s: dict, model: str, hours: float) -> None:
    if model in s["scored"] or not s["precision"].get(model, {}).get("pass"):
        return
    if not projection(s, f"x_score {model}", hours):
        return
    retrieval = bool(s["a1r"] and s["a1r"]["gate_passed"])
    args = ["--models", model] + ([] if retrieval else ["--no-retrieval"])
    r = push("x_score", args, hours, include=["results/e09_romanize/best_schemes.json"])
    if r is None:
        log(s, f"score {model}: runner did not push; nothing recorded")
        return
    done = (r["dir"] / "out" / model / "done.json").exists()
    s["scored"][model] = {"done": done, "retrieval_requested": retrieval, "dir": str((r["dir"] / "out" / model).relative_to(REPO)), "hours": r["hours"],
                          "commit": r["commit"], "status": r["status"]}
    log(s, f"score {model}: done={done} retrieval={retrieval} hours={r['hours']:.2f}")


def x9b_pilot(s: dict) -> bool:
    """X9b memory/timing pilot on the Kaggle T4 (X9b-D1): right after the A1-P pair, ahead of the scoring. Waits (up to 3 h) for the job script to exist."""
    done = REPO / "results" / "phase2" / "x9b" / "pilot_done.json"
    if done.exists() or s.get("x9b_pilot_pushed"):
        return True
    waited = 0
    while not (REPO / "scripts" / "kaggle_x9b.py").exists() and waited < 3 * 3600:
        if waited % 600 == 0:
            log(s, "X9b pilot script not built yet; the scoring waits behind it (operator order)")
        time.sleep(60)
        waited += 60
    if not (REPO / "scripts" / "kaggle_x9b.py").exists():
        return False
    if not projection(s, "kaggle_x9b pilot", 1.0):
        return False
    r = push("kaggle_x9b", ["--mode", "pilot"], 1.0)
    if r is None:
        log(s, "X9b pilot: runner did not push; nothing recorded")
        return False
    s["x9b_pilot_pushed"] = {"dir": str(r["dir"].relative_to(REPO)), "hours": r["hours"], "commit": r["commit"], "status": r["status"]}
    src = r["dir"] / "out" / "pilot_done.json"
    if src.exists():
        done.parent.mkdir(parents=True, exist_ok=True)
        done.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    log(s, f"X9b pilot: pilot_done.json written={src.exists()} hours={r['hours']:.2f}")
    return src.exists()


def a1p(s: dict, models: list[str]) -> None:
    models = [m for m in models if m not in s["precision"] and accessible(m)]
    if models and projection(s, f"A1-P {models}", 2.0 + 1.5 * len(models)):
        precision(s, models)


def open_models(s: dict) -> list[str]:
    """Models still to do: access pending, or passed A1-P but not scored. Instruct models are scored only if both pass."""
    out = []
    for m in WANT:
        p = s["precision"].get(m, {}).get("pass")
        if m in INSTRUCT:
            both = [s["precision"].get(x, {}).get("pass") for x in INSTRUCT]
            if False in both:
                continue
            if m not in s["scored"] and (p is None or all(both)):
                out.append(m)
        elif p is None or (p and m not in s["scored"]):
            out.append(m)
    return out


def main() -> None:
    s = state()
    if "--open" in sys.argv:
        sys.exit(1 if open_models(s) else 0)
    read_a1r(s)
    if s["a1r"] is None:
        log(s, "A1-R result not available yet; run it first (scripts/kaggle_runner.py run kaggle_retrieval_gate)")
        return
    ingest_precision(s)
    a1p(s, ["qwen3-8b", "ambari-7b-base"])                      # (a) the pair
    x9b_pilot(s)                                                # X9b pilot right after the A1-P pair, ahead of the scoring (Aarnav, 2026-11-02)
    score(s, "qwen3-8b", 5.0)                                   # (b) X13 Qwen3-8B, then X12 Ambari-base, whichever passed
    score(s, "ambari-7b-base", 5.0)
    a1p(s, INSTRUCT)                                            # (c) Ambari-Instruct v0.1 and v0.2, one push
    if x9b_ready() and not s.get("x9b_done"):                   # (d) X9b Sarvam arm; the job script is built after the laptop pilot
        log(s, "X9b ready but the Kaggle job runner for it is not wired into this driver yet: stopping for the operator")
    elif not x9b_ready():
        log(s, "X9b Sarvam arm not started: laptop memory pilot not done yet")
    for m in ("llama-2-7b", "llama-3.1-8b"):                    # gated: retried every pass
        a1p(s, [m])
        score(s, m, 5.0)
    if all(s["precision"].get(m, {}).get("pass") for m in INSTRUCT):   # X12 contrast 2 primary statistic: DiD on SIB and retrieval
        for m in INSTRUCT:
            score(s, m, 5.0)
    log(s, "MDL jobs (X13 after scoring, X12 contrast 2 descriptive) are not built into this driver yet")
    save(s)
    log(s, "queue pass finished; open: " + ", ".join(open_models(s)))


if __name__ == "__main__":
    main()
