"""Read-only scan for the 2026-11-09 cleanup: records which files check_numbers opens (audit hook, all 13 sections), then groups cleanup candidates. Writes JSON to the path given as argv[1]. Deletes nothing."""
import hashlib
import json
import os
import runpy
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
os.chdir(REPO)
SECTIONS = ["abstract", "intro", "related", "setup", "controlled", "accuracy", "assembly", "familiarity", "scale", "limitations", "conclusion", "broader_impact", "appendix"]
PROTECTED_PREFIX = ["RESULTS.md", "paper2/", "scripts/", "docs/", "results/phase2/dump/", "results/phase2/FULL_RESULTS_DUMP.md", "results/phase2/RESULTS_FLAT.md", "results/phase2/RESULTS_READABLE.md",
                    "results/phase2/CLEANUP_LIST.md", "results/CHAIN_STATUS_X10SM.md", "results/phase2/x10/", "results/phase2/x10sm", "results/phase2/x10pilot", "results/CHAIN_STATUS_X10", "results/kaggle/acct3",
                    "build/kaggle_acct3", "build/kaggle_config_3", ".git/", ".venv/", ".env", "cache/llm_cache.sqlite"]


def is_protected(rel):
    return any(rel == p or rel.startswith(p) for p in PROTECTED_PREFIX)


def opened_by_check_numbers():
    seen = set()

    def hook(event, args):
        if event == "open" and args and isinstance(args[0], (str, os.PathLike)):
            try:
                p = Path(args[0]).resolve()
                if REPO in p.parents and p.is_file():
                    seen.add(str(p.relative_to(REPO)).replace(chr(92), "/"))
            except Exception:  # noqa: BLE001
                pass
    sys.addaudithook(hook)
    sys.path.insert(0, str(REPO / "paper2" / "scripts"))
    sys.path.insert(0, str(REPO / "src"))
    import io
    import contextlib
    for s in SECTIONS:
        sys.argv = ["check_numbers.py", "--section", s + ".tex"]
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                runpy.run_path(str(REPO / "paper2" / "scripts" / "check_numbers.py"), run_name="__main__")
            except SystemExit:
                pass
    return sorted(seen)


def main():
    dest = sys.argv[1]
    out = {}
    out["opened_by_check_numbers"] = opened_by_check_numbers()
    tracked = subprocess.run(["git", "ls-files"], capture_output=True, text=True, encoding="utf-8").stdout.split("\n")
    out["tracked"] = [t for t in tracked if t]
    Path(dest).write_text(json.dumps(out), encoding="utf-8")
    print("opened", len(out["opened_by_check_numbers"]), "tracked", len(out["tracked"]))


if __name__ == "__main__":
    main()
