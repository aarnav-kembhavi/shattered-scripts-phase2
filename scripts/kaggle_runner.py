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
KDIR = REPO / "results" / "kaggle"
BUILD = REPO / "build" / "kaggle"
WEEK_H, SESSION_H = 30.0, 12.0
PKG_DATASET = "shattered-pkg"
CODE_DIRS = ["src", "scripts", "configs"]
PINS = ["transformers==5.19.0", "accelerate==1.15.0", "safetensors==0.8.0", "tokenizers==0.23.2", "huggingface_hub==1.33.0",
        "sentencepiece==0.2.2", "statsmodels==0.15.0", "pyarrow==25.0.1", "protobuf==7.36.2", "tiktoken==0.14.0"]  # local versions


def env() -> dict:
    e = dict(os.environ)
    for line in (REPO / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            e.setdefault(k.strip(), v.strip())
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
    p = KDIR / "quota.json"
    return json.loads(p.read_text()) if p.exists() else {"sessions": []}


def used_hours(q: dict) -> float:
    cut = datetime.now(timezone.utc) - timedelta(days=7)
    return sum(s["hours"] for s in q["sessions"] if datetime.fromisoformat(s["start_utc"]) >= cut)


def package(commit: str, includes: list[str]) -> Path:
    d = BUILD / commit[:8]
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
zp = glob.glob("/kaggle/input/**/repo.zip", recursive=True)[0]
root = "/kaggle/working/repo"
zipfile.ZipFile(zp).extractall(root)
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--no-deps", "-e", root], check=True)
subprocess.run([sys.executable, "-m", "pip", "install", "-q", *__PINS__], check=True)
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
    commit = git("rev-parse", "HEAD")
    dirty = git("status", "--porcelain", "--", *CODE_DIRS, "pyproject.toml")
    if dirty and not a.allow_dirty:
        raise SystemExit("tracked code is modified; commit first (or --allow-dirty, recorded):\n" + dirty[:400])
    q = quota()
    used = used_hours(q)
    assert a.timeout_h <= SESSION_H - 0.5, "a session may not exceed 12 h"
    if used + a.timeout_h > WEEK_H:
        raise SystemExit(f"weekly quota: {used:.1f} h used in the last 7 days, this push may use {a.timeout_h} h, limit {WEEK_H} h")
    if job != "kaggle_gate" and not (KDIR / "kaggle_gate" / "gate_passed.json").exists():
        raise SystemExit("reproducibility gate has not passed: no remote result counts (results/kaggle/kaggle_gate/gate_passed.json)")
    d = package(commit, a.include)
    upload_dataset(d, commit)
    user = env()["KAGGLE_USERNAME"]
    kd = BUILD / f"kernel_{job}"
    shutil.rmtree(kd, ignore_errors=True)
    kd.mkdir(parents=True)
    budget = int(a.timeout_h * 3600)
    (kd / "kernel.py").write_text(BOOT.replace("__COMMIT__", commit).replace("__JOB__", job).replace("__ARGS__", repr(a.job_args))
                                  .replace("__PINS__", repr(PINS)).replace("__BUDGET__", str(budget)), encoding="utf-8")
    slug = f"shattered-{job.replace('_', '-')}"
    meta = {"id": f"{user}/{slug}", "title": slug, "code_file": "kernel.py", "language": "python", "kernel_type": "script",
            "is_private": True, "enable_gpu": True, "enable_internet": True, "dataset_sources": [f"{user}/{PKG_DATASET}"],
            "kernel_sources": [a.resume_from] if a.resume_from else [], "competition_sources": []}
    (kd / "kernel-metadata.json").write_text(json.dumps(meta, indent=1))
    t_push = datetime.now(timezone.utc)
    print(kaggle("kernels", "push", "-p", str(kd), "--accelerator", "NvidiaTeslaT4", "-t", str(budget)), flush=True)
    rec = {"job": job, "kernel": meta["id"], "commit": commit, "dirty": bool(dirty), "args": a.job_args, "start_utc": t_push.isoformat(),
           "hours": a.timeout_h, "status": "pushed", "accelerator": "NvidiaTeslaT4 (T4 x2)"}  # hours = reserved until the real runtime is known
    q["sessions"].append(rec)
    (KDIR).mkdir(parents=True, exist_ok=True)
    (KDIR / "quota.json").write_text(json.dumps(q, indent=1))
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
        if any(k in low for k in ("complete", "error", "cancel")) or not wait:
            break
        print(f"[{time.strftime('%H:%M:%S')}] {s.strip()[-80:]}", flush=True)
        time.sleep(120)
    od = KDIR / job / rec["start_utc"][:19].replace(":", "")
    od.mkdir(parents=True, exist_ok=True)
    kaggle("kernels", "output", ref, "-p", str(od), check=False)
    prov = od / "provenance_kaggle.json"
    P = json.loads(prov.read_text()) if prov.exists() else {}
    rec.update({"status": s.strip()[-120:], "output_dir": str(od.relative_to(REPO)), "hours": (P.get("seconds") or (time.time() - t0)) / 3600,
                "hardware": P.get("gpus"), "torch": P.get("torch"), "bf16_supported": P.get("bf16_supported")})
    for x in q["sessions"]:
        if x["start_utc"] == rec["start_utc"] and x["job"] == job:
            x.update(rec)
    (KDIR / "quota.json").write_text(json.dumps(q, indent=1))
    (KDIR / job / "last_run.json").write_text(json.dumps({**rec, "provenance": P}, indent=1))
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
