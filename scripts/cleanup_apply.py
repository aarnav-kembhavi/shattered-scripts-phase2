"""Applies the 2026-11-09 cleanup plan (argv[1] = plan JSON from scripts/cleanup_plan.py). Deletes the groups marked delete; copies the groups marked archive to the archive folder
(verified by sha256), then removes the originals from the working tree; writes the manifest. Never touches git history or tags; the git index is updated by the caller."""
import csv
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
os.chdir(REPO)
plan = json.load(open(sys.argv[1], encoding="utf-8"))
ARCH = Path(sys.argv[2])
dup_keep_for = plan["dup_keep_for"]
MB = 1024 * 1024


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(8 * MB), b""):
            h.update(b)
    return h.hexdigest()


def tree_stats():
    n = b = 0
    for r, ds, fs in os.walk("."):
        ds[:] = [d for d in ds if not (r == "." and d in (".git", ".venv"))]
        for f in fs:
            try:
                b += os.path.getsize(os.path.join(r, f))
                n += 1
            except OSError:
                pass
    return n, b


before = tree_stats()
print("before:", before[0], "files", round(before[1] / MB, 1), "MB", flush=True)
ARCH.mkdir(parents=True, exist_ok=True)
rows = []
removed_dirs = set()
for name, g in plan["groups"].items():
    act = g["action"]
    if act not in ("delete", "archive"):
        continue
    gid = name.split(" ")[0]
    for rel in g["files"]:
        if not os.path.exists(rel):
            rows.append([gid, act, rel, "", "", "already absent", ""])
            continue
        size = os.path.getsize(rel)
        if act == "archive":
            keep = dup_keep_for.get(rel, "")
            if keep:
                assert os.path.exists(keep), f"kept copy missing for {rel}: {keep}"
            dst = ARCH / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(rel, dst)
            h1, h2 = sha(rel), sha(dst)
            assert h1 == h2, f"copy mismatch {rel}"
            os.remove(rel)
            rows.append([gid, "moved to archive", rel, size, h1, "", keep])
        else:
            keep = dup_keep_for.get(rel, "")
            h = ""
            if keep:
                assert os.path.exists(keep), f"kept copy missing for {rel}: {keep}"
                h = sha(rel)
                assert h == sha(keep), f"duplicate mismatch {rel}"
            os.remove(rel)
            rows.append([gid, "deleted", rel, size, h, "", keep])
        removed_dirs.add(os.path.dirname(rel))
# remove directories that became empty (bottom-up, only those touched)
for d in sorted(removed_dirs, key=len, reverse=True):
    cur = d
    while cur and cur not in (".", ""):
        try:
            os.rmdir(cur)
        except OSError:
            break
        cur = os.path.dirname(cur)
with open(ARCH / "MANIFEST.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["group", "action", "path", "bytes", "sha256", "note", "identical_to_kept_copy"])
    w.writerows(rows)
shutil.copy2(ARCH / "MANIFEST.csv", REPO / "results" / "CLEANUP_MANIFEST.csv")
after = tree_stats()
print("after:", after[0], "files", round(after[1] / MB, 1), "MB", flush=True)
json.dump({"before": before, "after": after, "rows": len(rows)}, open(ARCH / "stats.json", "w"))
