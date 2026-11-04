"""Kaggle runner (Phase 2, 2026-11-02): package the repo at a commit, push a GPU T4 x2 kernel with internet on, poll, download the
outputs, and record commit, hardware, dtype and runtime. Credentials come from .env (KAGGLE_USERNAME, KAGGLE_API_TOKEN); they are never
printed, written to the package or committed.

Usage: python scripts/kaggle_runner.py run <job> [--include PATH ...] [--timeout-h 11] [--no-wait] -- <job script args>
       python scripts/kaggle_runner.py fetch <job> [<kernel run dir name>]      (download outputs of the last pushed kernel of <job>)
       python scripts/kaggle_runner.py quota                                    (hours used in the last 7 days)
<job> is scripts/<job>.py (for example kaggle_gate). The job receives --out /kaggle/working/out first, then the args after `--`.

Rules enforced here: a session never exceeds 12 h (default timeout 11 h; the kernel stops its own job at the timeout minus 20 minutes
so outputs are saved); the weekly quota (30 h) is tracked in results/kaggle/quota.json and a push that would exceed it is refused;
jobs must be resumable and write one output shard at a time, so a session timeout loses at most one shard (a later push can pass the
previous kernel output as an input with --resume-from <kernel ref>). Remote results count only after the reproducibility gate passed
(results/kaggle/kaggle_gate/gate_passed.json). Uploads are private.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SHARED = REPO / "results" / "kaggle"  # queue state, HOLD, DEFER: shared by both accounts


def account() -> str:
    """Kaggle account of this call: KAGGLE_ACCOUNT=1 (default) or 2 (a teammate's account added 2026-11-04; its own 30 h per rolling 7 days, quota file, job folders and credentials)."""
    return os.environ.get("KAGGLE_ACCOUNT", "1")


def kdir() -> Path:
    return SHARED if account() == "1" else SHARED / "acct2"


def build() -> Path:
    return REPO / "build" / ("kaggle" if account() == "1" else "kaggle_acct2")
WEEK_H, SESSION_H = 30.0, 12.0
PKG_DATASET = "shattered-pkg"
CODE_DIRS = ["src", "scripts", "configs"]
PINS = ["transformers==5.19.0", "accelerate==1.15.0", "safetensors==0.8.0", "tokenizers==0.23.2", "huggingface_hub==1.33.0",
        "sentencepiece==0.2.2", "statsmodels==0.15.0", "pyarrow==25.0.1", "protobuf==7.36.2", "tiktoken==0.14.0", "bitsandbytes>=0.46.1", "peft==0.21.2"]  # local versions (bitsandbytes: A1-P 8-bit reference only)


def env() -> dict:
    e = dict(os.environ)
    for line in (REPO / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            e.setdefault(k.strip(), v.strip())
    if account() == "2":  # the teammate's account: credentials in .env as KAGGLE2_USERNAME / KAGGLE2_API_TOKEN (never printed or committed)
        e["KAGGLE_USERNAME"], e["KAGGLE_API_TOKEN"] = e.get("KAGGLE2_USERNAME", ""), e.get("KAGGLE2_API_TOKEN", "")
    assert e.get("KAGGLE_USERNAME") and e.get("KAGGLE_API_TOKEN"), "Kaggle credentials missing in .env"
    return e


def kaggle(*args, check=True) -> str:
    r = subprocess.run([str(REPO / ".venv" / "Scripts" / "kaggle.exe"), *args], env=env(), capture_output=True, text=True, encoding="utf-8")
    out = (r.stdout or "") + (r.stderr or "")
    tok = env()["KAGGLE_API_TOKEN"]
    out = out.replace(tok, "<token>")  # never echo the token
    if check and r.returncode != 0:
        raise SystemExit(f"kaggle {' '.join(args[:2])} failed: {out[-800:]}")
    return out


def git(*args) -> str:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, check=True).stdout.strip()


def quota() -> dict:
    p = kdir() / "quota.json"
    return json.loads(p.read_text()) if p.exists() else {"sessions": []}


def used_hours(q: dict) -> float:
    cut = datetime.now(timezone.utc) - timedelta(days=7)
    return sum(s["hours"] for s in q["sessions"] if datetime.fromisoformat(s["start_utc"]) >= cut)


def package(commit: str, includes: list[str]) -> Path:
    d = build() / commit[:8]
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    tar = d / "repo.tar"
    subprocess.run(["git", "archive", "--format=tar", "-o", str(tar), commit, "pyproject.toml", *CODE_DIRS], cwd=REPO, check=True)
    z = d / "repo.zip"
    import tarfile
    with tarfile.open(tar) as t, zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for m in t.getmembers():
            if m.isfile():
                zf.writestr(m.name, t.extractfile(m).read())
        for inc in includes:  # untracked or ignored result files the job needs (committed ones are also fine)
            for f in ([REPO / inc] if (REPO / inc).is_file() else sorted((REPO / inc).rglob("*"))):
                if f.is_file() and ".env" not in f.name and "kaggle.json" not in f.name:
                    zf.write(f, f.relative_to(REPO).as_posix())
    tar.unlink()
    (d / "dataset-metadata.json").write_text(json.dumps({"title": PKG_DATASET, "id": f"{env()['KAGGLE_USERNAME']}/{PKG_DATASET}",
                                                         "licenses": [{"name": "other"}]}))
    return d


def upload_dataset(d: Path, commit: str) -> None:
    ref = f"{env()['KAGGLE_USERNAME']}/{PKG_DATASET}"
    exists = PKG_DATASET in kaggle("datasets", "list", "--mine", "-s", PKG_DATASET, check=False)
    if exists:
        print(kaggle("datasets", "version", "-p", str(d), "-m", f"commit {commit[:8]}", "--dir-mode", "zip"), flush=True)
    else:
        print(kaggle("datasets", "create", "-p", str(d), "--dir-mode", "zip"), flush=True)
    for _ in range(60):  # wait until the dataset version is ready
        s = kaggle("datasets", "status", ref, check=False)
        if "ready" in s.lower():
            return
        time.sleep(10)
    raise SystemExit("dataset not ready after 10 minutes: " + s[-300:])


BOOT = '''"""Kaggle bootstrap written by scripts/kaggle_runner.py (commit __COMMIT__)."""
import glob, json, os, subprocess, sys, time, zipfile
t0 = time.time()
root = "/kaggle/working/repo"
zps = glob.glob("/kaggle/input/**/repo.zip", recursive=True)
if zps:
    zipfile.ZipFile(zps[0]).extractall(root)
else:  # Kaggle unpacks uploaded zips: the repo is then a directory tree under /kaggle/input
    import shutil
    hits = glob.glob("/kaggle/input/**/pyproject.toml", recursive=True)
    print("input listing:", os.listdir("/kaggle/input"), hits, flush=True)
    print("datasets (depth 2):", sorted(glob.glob("/kaggle/input/*/*")) + sorted(glob.glob("/kaggle/input/*/*/*"))[:20], flush=True)
    shutil.copytree(os.path.dirname(hits[0]), root)
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--no-deps", "-e", root], check=True)
subprocess.run([sys.executable, "-m", "pip", "install", "-q", *__PINS__], check=True)
# the Kaggle image ships torchao 0.10.0, which peft refuses (ImportError in is_torchao_available when merging a LoRA adapter into a plain fp16 base); nothing here uses torchao
subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "torchao"], check=False)
try:
    from kaggle_secrets import UserSecretsClient
    os.environ["HF_TOKEN"] = UserSecretsClient().get_secret("HF_TOKEN")
except Exception as e:
    print("no HF_TOKEN secret:", repr(e)[:80])
out = "/kaggle/working/out"
os.makedirs(out, exist_ok=True)
smi = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv"], capture_output=True, text=True).stdout
import torch, transformers
prov = {"commit": "__COMMIT__", "job": "__JOB__", "args": __ARGS__, "gpus": smi, "torch": torch.__version__, "cuda": torch.version.cuda,
        "transformers": transformers.__version__, "n_gpus": torch.cuda.device_count(), "bf16_supported": torch.cuda.is_bf16_supported(),
        "python": sys.version.split()[0], "start_epoch": t0}
json.dump(prov, open(out + "/provenance_kaggle.json", "w"), indent=1)
budget = __BUDGET__ - 1200  # seconds the job may run; the kernel then stops it so outputs are saved
env = dict(os.environ, PYTHONPATH=root + "/src", PYTHONIOENCODING="utf-8")
p = subprocess.Popen([sys.executable, "-u", root + "/scripts/__JOB__.py", "--out", out, *__ARGS__], cwd=root, env=env)
try:
    rc = p.wait(timeout=budget)
except subprocess.TimeoutExpired:
    p.terminate(); rc = "timeout"
prov.update({"returncode": rc, "seconds": time.time() - t0})
json.dump(prov, open(out + "/provenance_kaggle.json", "w"), indent=1)
print("job finished", rc, flush=True)
'''


def run(a) -> None:
    job = a.job
    dp = SHARED / "DEFER.json"  # operator deferrals (2026-11-02): [{"job", "model", "requires_pass"?}]; the old driver in memory must not run steps out of the new order
    if dp.exists():
        st = json.loads((SHARED / "queue_state.json").read_text()) if (SHARED / "queue_state.json").exists() else {}
        for d in json.loads(dp.read_text()):
            if d["job"] == job and d["model"] in a.job_args and not (d.get("requires_pass") and st.get("precision", {}).get(d["requires_pass"], {}).get("pass")):
                raise SystemExit(f"deferred by the operator: {d}")
    if (SHARED / "HOLD").exists():  # operator hold (2026-11-02): no new push while this file exists; the in-flight job is unaffected
        raise SystemExit("queue on hold (results/kaggle/HOLD exists): " + (SHARED / "HOLD").read_text()[:200])
    commit = git("rev-parse", "HEAD")
    dirty = git("status", "--porcelain", "--", *CODE_DIRS, "pyproject.toml")
    if dirty and not a.allow_dirty:
        raise SystemExit("tracked code is modified; commit first (or --allow-dirty, recorded):\n" + dirty[:400])
    q = quota()
    used = used_hours(q)
    assert a.timeout_h <= SESSION_H - 0.5, "a session may not exceed 12 h"
    if used + a.timeout_h > WEEK_H:
        raise SystemExit(f"weekly quota: {used:.1f} h used in the last 7 days, this push may use {a.timeout_h} h, limit {WEEK_H} h")
    if job not in ("kaggle_gate", "kaggle_retrieval_gate") and not (kdir() / "kaggle_gate" / "gate_passed.json").exists():
        raise SystemExit("reproducibility gate has not passed: no remote result counts (results/kaggle/kaggle_gate/gate_passed.json)")
    if job == "kaggle_mdl":
        a.include = list(a.include) + ["results/m14_full/words.json"]
    if job == "kaggle_x9b":  # the exclusion report, the removed-id list and the 300 Phase 1 probe words are results files, not code
        a.include = list(a.include) + ["results/phase2/x9b/streams_report.json", "results/phase2/x9b/removed_ids.json", "results/phase2/x9b/pilot_done.json", "results/phase2/x9b/base_reference.json", "results/e09_romanize/best_schemes.json"]
        a.include = [i for i in a.include if (REPO / i).exists()]
    d = package(commit, a.include)
    upload_dataset(d, commit)
    user = env()["KAGGLE_USERNAME"]
    kd = build() / f"kernel_{job}"
    shutil.rmtree(kd, ignore_errors=True)
    kd.mkdir(parents=True)
    budget = int(a.timeout_h * 3600)
    (kd / "kernel.py").write_text(BOOT.replace("__COMMIT__", commit).replace("__JOB__", job).replace("__ARGS__", repr(a.job_args))
                                  .replace("__PINS__", repr(PINS)).replace("__BUDGET__", str(budget)), encoding="utf-8")
    slug = f"shattered-{job.replace('_', '-')}"
    meta = {"id": f"{user}/{slug}", "title": slug, "code_file": "kernel.py", "language": "python", "kernel_type": "script",
            "is_private": True, "enable_gpu": True, "enable_internet": True, "dataset_sources": [f"{user}/{PKG_DATASET}", *[f"{user}/{x}" for x in a.private_data]],
            "kernel_sources": [a.resume_from] if a.resume_from else [], "competition_sources": []}
    (kd / "kernel-metadata.json").write_text(json.dumps(meta, indent=1))
    t_push = datetime.now(timezone.utc)
    pushed = kaggle("kernels", "push", "-p", str(kd), "--accelerator", "NvidiaTeslaT4", "-t", str(budget))
    print(pushed, flush=True)
    if "successfully pushed" not in pushed:  # e.g. Kaggle refuses a third GPU session on the account: no kernel exists, nothing is recorded in the quota file
        raise SystemExit("kernel push was not accepted: " + pushed[-300:])
    rec = {"job": job, "kernel": meta["id"], "commit": commit, "dirty": bool(dirty), "args": a.job_args, "start_utc": t_push.isoformat(),
           "hours": a.timeout_h, "status": "pushed", "accelerator": "NvidiaTeslaT4 (T4 x2)"}  # hours = reserved until the real runtime is known
    q["sessions"].append(rec)
    (kdir()).mkdir(parents=True, exist_ok=True)
    (kdir() / "quota.json").write_text(json.dumps(q, indent=1))
    if a.no_wait:
        return
    fetch(job, wait=True, rec=rec)


def fetch(job: str, wait: bool = False, rec: dict | None = None) -> None:
    q = quota()
    rec = rec or next(s for s in reversed(q["sessions"]) if s["job"] == job)
    ref = rec["kernel"]
    t0 = time.time()
    while True:
        s = kaggle("kernels", "status", ref, check=False)
        low = s.lower()
        if not wait:
            break
        if "kernelworkerstatus." in low:
            if any(k in low for k in ("complete", "error", "cancel")):
                break
            bad = 0
        else:  # the status call itself failed (network blip): keep polling, give up after 30 consecutive failures
            bad = locals().get("bad", 0) + 1
            if bad >= 30:
                break
        print(f"[{time.strftime('%H:%M:%S')}] {s.strip()[-80:]}", flush=True)
        time.sleep(120)
    od = kdir() / job / rec["start_utc"][:19].replace(":", "")
    od.mkdir(parents=True, exist_ok=True)
    kaggle("kernels", "output", ref, "-p", str(od), check=False)
    prov = od / "provenance_kaggle.json"
    P = json.loads(prov.read_text()) if prov.exists() else {}
    rec.update({"status": s.strip()[-120:], "output_dir": str(od.relative_to(REPO)), "hours": (P.get("seconds") or (time.time() - t0)) / 3600,
                "hardware": P.get("gpus"), "torch": P.get("torch"), "bf16_supported": P.get("bf16_supported")})
    for x in q["sessions"]:
        if x["start_utc"] == rec["start_utc"] and x["job"] == job:
            x.update(rec)
    (kdir() / "quota.json").write_text(json.dumps(q, indent=1))
    (kdir() / job / "last_run.json").write_text(json.dumps({**rec, "provenance": P}, indent=1))
    print(json.dumps({k: rec[k] for k in ("job", "commit", "status", "hours", "hardware", "output_dir")}, indent=1))
    print(f"weekly hours used (last 7 days): {used_hours(q):.2f} of {WEEK_H}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("job")
    r.add_argument("--include", nargs="*", default=[])
    r.add_argument("--timeout-h", type=float, default=11.0)
    r.add_argument("--no-wait", action="store_true")
    r.add_argument("--allow-dirty", action="store_true")
    r.add_argument("--resume-from")
    r.add_argument("--private-data", nargs="*", default=[], help="extra PRIVATE datasets of this account (for example shattered-flores-private)")
    f = sub.add_parser("fetch")
    f.add_argument("job")
    sub.add_parser("quota")
    argv = sys.argv[1:]
    jobargs = []
    if "--" in argv:
        i = argv.index("--")
        argv, jobargs = argv[:i], argv[i + 1:]
    a = ap.parse_args(argv)
    a.job_args = jobargs
    if a.cmd == "run":
        run(a)
    elif a.cmd == "fetch":
        fetch(a.job, wait=True)
    else:
        print(f"{used_hours(quota()):.2f} h used in the last 7 days of {WEEK_H}")


if __name__ == "__main__":
    main()
