"""Kaggle queue driver (Amendment 2, approved 2026-11-02; order set by Aarnav 2026-11-02 23:16): A1-P pair (Qwen3-8B, Ambari-7B-base) -> score the ones that pass (X13 Qwen3-8B,
then X12 Ambari-base) -> A1-P Ambari-Instruct v0.1 and v0.2 (one push) -> X9b Sarvam-1 arm when its laptop pilot is done -> gated models retried between jobs. Weekly quota is projected before each push.
(earlier text:) A1-R retrieval gate (read from its fetched output) -> A1-P precision checks -> X12 scoring ->
X13 scoring, one Kaggle job at a time, deciding each step from the registered rules, retrying Hugging Face access between jobs. Idempotent and resumable:
state in results/kaggle/queue_state.json; every decision is logged with the rule it applies. A model is scored only after it passed A1-P; retrieval is
requested only if A1-R passed. Each job goes through scripts/kaggle_runner.py (quota, 12 h cap, commit, hardware record).
Usage: python scripts/kaggle_queue.py [--once]
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ACCT = os.environ.get("KAGGLE_ACCOUNT", "1")  # 1 = Aarnav's account (X9b and, until account 2 is accepted, everything); 2 = a teammate's account (self-contained jobs), own state file
os.environ["KAGGLE_ACCOUNT"] = ACCT
SHARED = REPO / "results" / "kaggle"
K = SHARED if ACCT == "1" else SHARED / "acct2"
STATE = K / os.environ.get("QUEUE_STATE_NAME", "queue_state.json")  # a second driver on the same account (X9b batch 3) uses its own state file
ACCT2_JOBS = ["ambari-7b-instruct-v0.1", "ambari-7b-instruct-v0.2", "llama-3.1-8b"]  # moved to account 2 on 2026-11-04 (self-contained: they mount private model datasets); X9b stays on account 1


def merge_x9b_from_acct2(s: dict) -> None:
    keys = set(s.setdefault("x9b", {}).setdefault("batches_done_keys", []))
    for name in ("queue_state.json", "queue_state_x9b.json"):
        p = SHARED / "acct2" / name
        if p.exists():
            keys |= set(json.loads(p.read_text()).get("x9b", {}).get("batches_done_keys", []))
    if keys != set(s["x9b"]["batches_done_keys"]):
        s["x9b"]["batches_done_keys"] = sorted(keys)
        s["x9b"]["batches_done"] = [k for k in s["x9b"]["batches_done_keys"] if k.startswith("sarvam-1")]
        log(s, f"X9b batches merged from account 2: {s['x9b']['batches_done_keys']}")


def acct2_accepted() -> bool:
    return (SHARED / "acct2" / "ACCEPTED").exists()  # written after the smoke test and the A1-R reproduction on account 2 passed
PY = str(REPO / ".venv" / "Scripts" / "python.exe")
PRIVATE = "shattered-flores-private"
X12 = ["ambari-7b-base", "llama-2-7b", "ambari-7b-instruct-v0.1", "ambari-7b-instruct-v0.2"]  # X12 endpoints (exempt from the counting rule, subject to A1-P)
X13 = ["qwen3-8b", "llama-3.1-8b"]  # plus the largest Sarvam that fits (named by the screen, added to the state when chosen)
INSTRUCT = ["ambari-7b-instruct-v0.1", "ambari-7b-instruct-v0.2"]  # X12 contrast 2 (instruction-pair exposure contrast): scored only if BOTH pass A1-P
X9B_SARVAM_H = 0.0  # reserve LIFTED by Aarnav 2026-11-04 (was 18.0, registered: Sarvam-1 primary arm); a job now only has to fit in the remaining quota hours; X9b batch 3 is pushed the moment it fits
WANT = ["qwen3-8b", "ambari-7b-base", "llama-2-7b", "llama-3.1-8b"] + INSTRUCT


def state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text())
    if ACCT == "2":  # start from the results account 1 already has (A1-P passes, scored models, MDL), so nothing is repeated
        m = json.loads((SHARED / "queue_state.json").read_text())
        return {"log": [], "precision": m["precision"], "scored": m["scored"], "mdl": m.get("mdl", {}), "a1r": m["a1r"], "x9b": m.get("x9b", {}), "x9b_pilot_failures": m.get("x9b_pilot_failures", 0)}
    return {"log": [], "precision": {}, "scored": {}, "a1r": None}


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


CODE_FILES = ["scripts/kaggle_queue.py", "scripts/kaggle_runner.py", "scripts/kaggle_precision.py", "scripts/x_score.py", "scripts/kaggle_mdl.py", "scripts/kaggle_x9b.py", "src/shattered/interp/load.py"]


def code_hash() -> str:
    import hashlib
    return hashlib.sha256(b"".join((REPO / f).read_bytes() for f in CODE_FILES if (REPO / f).exists())).hexdigest()


_CODE_AT_START = code_hash()


def preflight(args: list[str], extra: list[str]) -> str | None:
    """Cheap laptop-side checks before a push costs quota (decided 2026-11-04 after three failed launches). Returns a reason to refuse, or None.
    (1) The datasets the job mounts (the private model datasets) exist and are ready on Kaggle. (2) Any model named in the arguments that is gated on Hugging Face
    (anonymous request to config.json gives 401) has a private dataset. (3) The shipped scripts are the current ones (checked by the caller, which re-executes this process)."""
    sys.path.insert(0, str(REPO / "scripts"))
    sys.path.insert(0, str(REPO / "src"))
    import urllib.error
    import urllib.request

    import kaggle_runner as KR
    from shattered.interp.load import KAGGLE_DATASETS, MODELS
    user = KR.env()["KAGGLE_USERNAME"]
    for slug in [PRIVATE, *extra]:
        s = KR.kaggle("datasets", "status", f"{user}/{slug}", check=False)
        if "ready" not in s.lower():
            return f"dataset {user}/{slug} is not ready on Kaggle: {s.strip()[:120]}"
    for m in args:
        if m in MODELS and m not in KAGGLE_DATASETS:
            try:
                urllib.request.urlopen(urllib.request.Request(f"https://huggingface.co/{MODELS[m]}/resolve/main/config.json", method="HEAD"), timeout=30)
            except urllib.error.HTTPError as e:
                if e.code in (401, 403):
                    return f"{m} ({MODELS[m]}) is gated on Hugging Face and has no private Kaggle dataset"
    return None


def push(job: str, args: list[str], hours: float, include: list[str] | None = None) -> dict:
    if code_hash() != _CODE_AT_START:  # the scripts changed since this process started: restart it so every launch uses the committed code (the stale-driver bug)
        print("driver code changed on disk since this process started; re-executing with the current code (state is saved)", flush=True)
        os.execv(sys.executable, [sys.executable, "-u", *sys.argv])
    sys.path.insert(0, str(REPO / "src"))
    from shattered.interp.load import KAGGLE_DATASETS
    extra = sorted({KAGGLE_DATASETS[m] for m in args if m in KAGGLE_DATASETS})  # gated models come from private datasets
    why = preflight(args, extra)
    if not why:  # never push a kernel whose previous version is still running or queued: the new version replaces it and its result is lost (2026-11-04, account 2, Ambari-Instruct-v0.1)
        sys.path.insert(0, str(REPO / "scripts"))
        import kaggle_runner as KR
        slug = f"{KR.env()['KAGGLE_USERNAME']}/shattered-{job.replace('_', '-')}"
        st = KR.kaggle("kernels", "status", slug, check=False).lower()
        if "running" in st or "queued" in st:
            why = f"kernel {slug} is still running or queued: {st.strip()[-60:]}"
    if why:
        print(f"{job} {args}: preflight refused, nothing pushed, no quota used: {why}", flush=True)
        return None
    cmd = [PY, "scripts/kaggle_runner.py", "run", job, "--timeout-h", str(hours), "--private-data", PRIVATE, *extra]
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
    p = SHARED / "a1r_result.json"
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
    r = push("kaggle_precision", ["--models", *models], a1p_hours(models))
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
    p = REPO / "results" / "phase2" / "x9b" / "pilot_done.json"
    return p.exists() and json.loads(p.read_text(encoding="utf-8")).get("eval_smoke_ok") is True and (REPO / "scripts" / "kaggle_x9b.py").exists()


def x9b_pending(s: dict) -> bool:
    """X9b Sarvam arm still to run (its pilot is done and not every Sarvam batch is finished)."""
    return x9b_ready() and len(s.get("x9b", {}).get("batches_done", [])) < len(SARVAM_BATCHES)


def projection(s: dict, job: str, hours: float, is_x9b: bool = False, x12c1: bool = False) -> bool:
    """Log the weekly-quota projection before a push. The X9b Sarvam arm (18 h) is reserved: a non-X9b push that would leave less than that is refused
    here (the caller then runs X9b first, or skips the step, which is the registered cut order: Llama-3.1-8B, then the instruction pair, then Qwen3.5)."""
    sys.path.insert(0, str(REPO / "scripts"))
    from kaggle_runner import WEEK_H, quota, used_hours
    used = used_hours(quota())
    head = WEEK_H - used - hours
    log(s, f"quota projection before {job}: {used:.2f} h used in the last 7 days, this push up to {hours:.1f} h, headroom {head:.1f} h, "
           f"X9b Sarvam reserve {X9B_SARVAM_H:.0f} h (X9b pending: {x9b_pending(s)})")
    if head < 0:
        log(s, f"{job}: over the weekly quota, not pushed")
        return False
    if x12c1 and head >= 0:
        log(s, f"{job}: X12 contrast 1 runs ahead of the X9b reserve on Aarnav's decision of 2026-11-04 (X9b batch 3 launches as soon as the projection allows; nothing else goes ahead of it)")
        return True
    if ACCT == "1" and not is_x9b and x9b_pending(s):  # Aarnav 2026-11-04: X9b batch 3 launches the moment it fits and nothing queues ahead of it
        log(s, f"{job}: X9b Sarvam batches are still pending; nothing goes ahead of them")
        return False
    return True


def score(s: dict, model: str, hours: float) -> None:
    if model in s["scored"] or not s["precision"].get(model, {}).get("pass"):
        return
    if not projection(s, f"x_score {model}", hours, x12c1=(model == "llama-2-7b")):
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


def mdl(s: dict, models: list[str], hours: float) -> None:
    """MDL assembly-layer job (Phase 1 protocol, 300 probe words, native and ITRANS) for models that passed A1-P."""
    models = [m for m in models if s["precision"].get(m, {}).get("pass") and m not in s.setdefault("mdl", {})]
    if not models or not projection(s, f"kaggle_mdl {models}", hours):
        return
    r = push("kaggle_mdl", ["--models", *models], hours)
    if r is None:
        log(s, "kaggle_mdl: runner did not push; nothing recorded")
        return
    for m in models:
        ok = (r["dir"] / "out" / m / "native.json").exists() and (r["dir"] / "out" / m / "itrans.json").exists()
        s["mdl"][m] = {"done": ok, "dir": str((r["dir"] / "out" / m).relative_to(REPO)), "hours": r["hours"], "commit": r["commit"]}
        log(s, f"MDL {m}: done={ok} hours={r['hours']:.2f}")


def x9b_pilot(s: dict) -> bool:
    """X9b memory/timing pilot on the Kaggle T4 (X9b-D1): right after the A1-P pair, ahead of the scoring."""
    done = REPO / "results" / "phase2" / "x9b" / "pilot_done.json"
    if done.exists():
        return True
    if s.get("x9b_pilot_failures", 0) >= 2 or not (REPO / "scripts" / "kaggle_x9b.py").exists():
        return False
    if not projection(s, "kaggle_x9b pilot", 2.2, is_x9b=True):  # measured: about 11 min per model and condition at micro-batch 16 (50 micro-steps), 6 combinations plus loads and the smoke
        return False
    r = push("kaggle_x9b", ["--mode", "pilot"], 2.2)
    if r is None:
        log(s, "X9b pilot: runner did not push; nothing recorded")
        return False
    src = r["dir"] / "out" / "pilot_done.json"
    if src.exists():
        done.parent.mkdir(parents=True, exist_ok=True)
        done.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        s["x9b_pilot_failures"] = s.get("x9b_pilot_failures", 0) + 1
    s["x9b_pilot_last"] = {"dir": str(r["dir"].relative_to(REPO)), "hours": r["hours"], "commit": r["commit"], "status": r["status"]}
    log(s, f"X9b pilot: pilot_done.json written={src.exists()} hours={r['hours']:.2f}")
    return src.exists()


def x9b_record_b(s: dict) -> bool:
    """Append the fixed B per model (from the pilot) to RESULTS.md with the system-clock stamp and commit that file, before any full run."""
    x = s.setdefault("x9b", {})
    if x.get("b_recorded"):
        return True
    d = json.loads((REPO / "results" / "phase2" / "x9b" / "pilot_done.json").read_text(encoding="utf-8"))
    if not d.get("all_overlap_zero"):
        log(s, "X9b: pilot_done.json reports overlap != 0; nothing runs")
        return False
    stamp = subprocess.run([PY, "scripts/stamp.py"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    rows = "; ".join(f"{m}: B = {v['B']:,} tokens ({v['optimizer_steps_at_B']} optimizer steps), slowest {v['slowest_tokens_per_s']:.0f} tokens/s, micro-batches "
                     + ", ".join(f"{c} {v['conditions'][c]['micro_batch']}" for c in v["conditions"]) + f", pool covers B: {v['pool_covers_B']}" for m, v in d["models"].items())
    entry = (f"\n- **{stamp}, X9b pilot (Kaggle T4, X9b-D1) and fixed token budgets.** {rows}. Tokens per optimizer step {d['tokens_per_optimizer_step']:,} (32 sequences of 512; "
             f"fixed before the pilot), 50 micro-steps timed. Exclusion scan: overlap 0 for every stream (CPU report) and 0 on every consumed stream in the pilot. "
             f"B is the same for the three conditions of a model and is not changed. (Appended by the queue driver from `results/phase2/x9b/pilot_done.json`.)\n")
    with open(REPO / "RESULTS.md", "a", encoding="utf-8") as f:
        f.write(entry)
    subprocess.run(["git", "add", "RESULTS.md", "results/phase2/x9b"], cwd=REPO, check=False)
    subprocess.run(["git", "commit", "-q", "-m", "RESULTS: X9b pilot timing and fixed B", "-m", "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"], cwd=REPO, check=False)
    x["b_recorded"] = True
    log(s, "X9b: B recorded in RESULTS.md and committed")
    return True


SARVAM_BATCHES = [["sarvam-1:itrans:0", "sarvam-1:native:0"], ["sarvam-1:english:0", "sarvam-1:itrans:1"], ["sarvam-1:native:1", "sarvam-1:english:1"]]
QWEN_BATCHES = [["qwen3.5-2b:itrans:0", "qwen3.5-2b:native:0", "qwen3.5-2b:english:0"]]


def x9b_full(s: dict, secondary: bool = False) -> None:
    """X9b full runs: a rehearsal of the whole path first (20 steps, discarded), then the registered runs in batches that fit a session; Qwen3.5-2B last (cut first)."""
    if not x9b_ready() or not x9b_record_b(s):
        return
    x = s["x9b"]
    d = json.loads((REPO / "results" / "phase2" / "x9b" / "pilot_done.json").read_text(encoding="utf-8"))
    if not (x.get("rehearsal") or {}).get("ok"):  # a failed rehearsal is repeated, never skipped
        if not projection(s, "x9b rehearsal", 1.5, is_x9b=True):
            return
        r = push("kaggle_x9b", ["--mode", "full", "--rehearsal", "--runs", "sarvam-1:itrans:0"], 1.5)
        ok = r is not None and (r["dir"] / "out" / "sarvam-1+itrans+s0__rehearsal" / "done.json").exists()
        x["rehearsal"] = {"ok": ok, "hours": (r or {}).get("hours")}
        log(s, f"X9b rehearsal: ok={ok}")
        if not ok:
            return
    batches = [(m, b) for m, bs in (("sarvam-1", SARVAM_BATCHES),) + ((("qwen3.5-2b", QWEN_BATCHES),) if secondary else ()) for b in bs]
    for i, (model, runs) in enumerate(batches):
        key = f"{model}#{i}"
        if key in x.setdefault("batches_done_keys", []):
            continue
        v = d["models"][model]
        per = v["B"] / v["slowest_tokens_per_s"] / 3600 + 0.6
        hours = min(11.0, per * len(runs) + (0.6 if i == 0 else 0.0) + 0.3)
        if not projection(s, f"x9b {model} {runs}", hours, is_x9b=True):
            return
        args = ["--mode", "full", "--runs", *runs, "--base-eval", model]
        r = push("kaggle_x9b", args, hours)
        if r is None:
            log(s, "X9b: runner did not push; stopping")
            return
        done_runs = [run for run in runs if (r["dir"] / "out" / "+".join([run.split(":")[0], run.split(":")[1], "s" + run.split(":")[2]]) / "done.json").exists()]
        if len(done_runs) == len(runs):
            x["batches_done_keys"].append(key)
        x["batches_done"] = [k for k in x["batches_done_keys"] if k.startswith("sarvam-1")]
        log(s, f"X9b batch {runs}: finished {done_runs} hours={r['hours']:.2f} dir={r['dir'].relative_to(REPO)}")
        if len(done_runs) != len(runs):
            log(s, "X9b: a batch did not finish; stopping for the operator")
            return


def a1p_hours(models: list[str]) -> float:
    sys.path.insert(0, str(REPO / "src"))
    from shattered.interp.load import KAGGLE_DATASETS
    # weights mounted from a private dataset load slowly (Llama-3.1-8B on account 2: 48 min fp16 load, 2.78 h in total; one Ambari-Instruct-v0.1 run timed out at 3.07 h)
    return 5.0 if any(m in KAGGLE_DATASETS for m in models) else 2.0 + 1.5 * len(models)


def a1p(s: dict, models: list[str]) -> None:
    models = [m for m in models if m not in s["precision"] and accessible(m)]
    models = [m for m in models if not (REPO / "results" / "kaggle" / f"DATASET_PENDING_{m}").exists()]  # gated model whose private Kaggle dataset is not uploaded yet (RESULTS.md 2026-11-04)
    hours = a1p_hours(models)
    if models and projection(s, f"A1-P {models}", hours, x12c1=(models == ["llama-2-7b"])):
        precision(s, models)


def passed(s: dict, *models: str) -> bool:
    return all(s["precision"].get(m, {}).get("pass") for m in models)


def open_models(s: dict) -> list[str]:
    """Still to do: A1-P not yet run, or passed but not scored (instruct pair only if both pass; Llama-2 only if Ambari-base also passed)."""
    out = []
    for m in WANT:
        if ACCT == "2" and m not in ACCT2_JOBS:
            continue
        if ACCT == "1" and acct2_accepted() and m in ACCT2_JOBS:
            continue
        p = s["precision"].get(m, {}).get("pass")
        if m in INSTRUCT:
            both = [s["precision"].get(x, {}).get("pass") for x in INSTRUCT]
            if False in both:
                continue
            if m not in s["scored"] and (p is None or all(both)):
                out.append(m)
        elif m == "llama-2-7b" and s["precision"].get("ambari-7b-base", {}).get("pass") is False:
            continue
        elif p is None or (p and m not in s["scored"]):
            out.append(m)
    if ACCT == "1" and (x9b_pending(s) or (not x9b_ready() and s.get("x9b_pilot_failures", 0) < 2)):
        out.append("x9b")
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
    if ACCT == "2" and os.environ.get("QUEUE_ONLY") == "x9b":  # X9b batch 3 on account 2 (it needs only the base model, the public Wikipedia pool and the seeds; batches 1 and 2 are not inputs)
        if not acct2_accepted():
            return
        x9b_full(s)
        save(s)
        log(s, "account 2 X9b pass finished; batches done: " + ", ".join(s.get("x9b", {}).get("batches_done_keys", [])))
        return
    if ACCT == "2":  # the teammate's account: the self-contained jobs (instruction pair, Llama-3.1-8B); Kaggle quota is per account
        if not acct2_accepted():
            log(s, "account 2 not accepted yet (smoke test and A1-R reproduction pending): nothing pushed")
            return
        a1p(s, ["ambari-7b-instruct-v0.1"])
        if passed(s, *INSTRUCT):
            for m in INSTRUCT:
                score(s, m, 2.4)
            mdl(s, INSTRUCT, 3.0)
        a1p(s, ["llama-3.1-8b"])
        score(s, "llama-3.1-8b", 2.4)
        save(s)
        log(s, "account 2 queue pass finished; open: " + ", ".join(open_models(s)))
        return
    merge_x9b_from_acct2(s)  # batch 3 may have run on account 2
    if acct2_accepted():  # account 1 keeps X9b only (its checkpoints and datasets live here); X9b batch 3 is first when the quota frees
        x9b_pilot(s)
        x9b_full(s)
        if x9b_ready() and not x9b_pending(s):
            x9b_full(s, secondary=True)
        save(s)
        log(s, "queue pass finished (account 1: X9b only); open: " + ", ".join(open_models(s)))
        return
    a1p(s, ["qwen3-8b", "ambari-7b-base"])                      # in flight / first: the A1-P pair
    x9b_pilot(s)                                                # (a) X9b pilot
    score(s, "qwen3-8b", 5.0)                                   # (b) whichever of the pair passed: X13 Qwen3-8B, then X12 Ambari-base
    score(s, "ambari-7b-base", 5.0)
    mdl(s, ["qwen3-8b"], 2.5)                                   # X13 MDL after scoring
    a1p(s, ["llama-2-7b"])                                      # (c) Llama-2-7B, then contrast 1 if both endpoints passed
    if passed(s, "ambari-7b-base", "llama-2-7b"):
        score(s, "llama-2-7b", 2.4)  # cap lowered from 5.0 on 2026-11-04 to fit the remaining quota; measured: Qwen3-8B scoring 1.71 h, Ambari-7B-base 1.23 h
    a1p(s, INSTRUCT)                                            # (d) Ambari-Instruct v0.1 and v0.2, then the secondary contrast if both pass
    if passed(s, *INSTRUCT):
        for m in INSTRUCT:
            score(s, m, 2.4)
        mdl(s, INSTRUCT, 3.0)                                   # contrast 2 MDL comparison (descriptive only)
    a1p(s, ["llama-3.1-8b"])                                    # (e) Llama-3.1-8B, then X13 scoring if it passes (first to be cut)
    score(s, "llama-3.1-8b", 2.4)
    x9b_full(s)                                                 # (f) X9b full, Sarvam-1 arm; Qwen3.5-2B arm only with enough quota (cut first)
    if x9b_ready() and not x9b_pending(s):
        x9b_full(s, secondary=True)
    save(s)
    log(s, "queue pass finished; open: " + ", ".join(open_models(s)))


if __name__ == "__main__":
    main()
