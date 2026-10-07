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


def provenance(config: dict) -> dict:
    return {
        "config": config,
        "git_commit": git_commit(),
        "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "argv": sys.argv,
    }


def results_dir(name: str) -> Path:
    d = REPO / "results" / name
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_json(path: Path, payload: dict, config: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"provenance": provenance(config), **payload}, ensure_ascii=False, indent=2,
                               default=lambda o: o.item() if hasattr(o, "item") else str(o)),
                    encoding="utf-8")
    return path


def lower_priority() -> None:
    """Run this process below normal priority (keeps concurrent GPU training fed)."""
    import os

    import psutil
    psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if os.name == "nt" else 10)
