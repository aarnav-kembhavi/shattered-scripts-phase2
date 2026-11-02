"""Write experiment outputs together with the config and git commit that produced them."""
from __future__ import annotations

import datetime as dt
import json
import platform
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def git_commit() -> str:
    """Current commit hash, suffixed with '-dirty' if tracked files have uncommitted changes."""
    try:
        sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
        dirty = subprocess.run(["git", "diff", "--quiet", "HEAD"], cwd=REPO).returncode != 0
        return sha + ("-dirty" if dirty else "")
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def registration_commit() -> str | None:
    """Commit of the Phase 2 pre-registration (git tag `phase2-registration`, set when it was committed), or None."""
    try:
        return subprocess.check_output(["git", "rev-parse", "--verify", "-q", "phase2-registration^{commit}"], cwd=REPO,
                                       text=True, stderr=subprocess.DEVNULL).strip() or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def amendment2_commit() -> str | None:
    """Commit of Phase 2 Amendment 2 (git tag `phase2-amendment-2`), or None; recorded in every X9 to X15 result."""
    try:
        return subprocess.check_output(["git", "rev-parse", "--verify", "-q", "phase2-amendment-2^{commit}"], cwd=REPO,
                                       text=True, stderr=subprocess.DEVNULL).strip() or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def provenance(config: dict) -> dict:
    return {
        "config": config,
        "git_commit": git_commit(),
        "phase2_registration_commit": registration_commit(),
        "phase2_amendment2_commit": amendment2_commit(),
        "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "argv": sys.argv,
    }


def results_dir(name: str) -> Path:
    d = REPO / "results" / name
    d.mkdir(parents=True, exist_ok=True)
    return d


def tmp_path(path: Path) -> Path:
    """Sibling temp file with the same suffix (np.savez keeps an .npz suffix as is)."""
    return path.with_name(f"{path.stem}.partial{path.suffix}")


def commit(tmp: Path, path: Path) -> Path:
    """Atomically move a finished temp file into place, so a crash never leaves a half-written output that a resume
    would mistake for a finished one."""
    import os
    os.replace(tmp, path)
    return path


def write_json(path: Path, payload: dict, config: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = tmp_path(path)
    tmp.write_text(json.dumps({"provenance": provenance(config), **payload}, ensure_ascii=False, indent=2,
                              default=lambda o: o.item() if hasattr(o, "item") else str(o)),
                   encoding="utf-8")
    return commit(tmp, path)


def lower_priority() -> None:
    """Run this process below normal priority (keeps concurrent GPU training fed)."""
    import os

    import psutil
    psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if os.name == "nt" else 10)
