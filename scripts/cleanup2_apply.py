"""Cleanup 2 (2026-11-09). Usage: python scripts/cleanup2_apply.py <plan.json> verify | apply.
verify: prints counts by top-level folder and checks that no file referenced by RESULTS.md is in the removal set (a referenced paper-type file is reported separately because their removal was ordered).
apply: deletes the paper-type files that have an identical copy outside the repo, moves the other untracked files to C:/PROJECTS/PROMPT/cleanup_archive_2026-11-09, git rm's the tracked files,
removes empty folders (not build/kaggle_config_*), and appends one row per action to results/CLEANUP_MANIFEST.csv. History and tags are not touched."""
import collections
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
os.chdir(REPO)
plan = json.load(open(sys.argv[1], encoding="utf-8"))
mode = sys.argv[2]
ARCH = Path("C:/PROJECTS/PROMPT/cleanup_archive_2026-11-09")
OUTSIDE = [Path("C:/PROJECTS/PROMPT/paper2_full_2026-11-09"), Path("C:/PROJECTS/PROMPT/paper2_overleaf")]
PAPER_EXT = (".tex", ".bib", ".sty", ".bst", ".cls", ".pdf")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(8 << 20), b""):
            h.update(b)
    return h.hexdigest()


removal = {}
for k in ("A_delete", "A_archive", "B_gitrm", "C_archive"):
    for p in plan[k]:
        removal[p] = k
tracked = set(subprocess.run(["git", "ls-files"], capture_output=True, text=True, encoding="utf-8").stdout.split("\n")) - {""}
allfiles = set()
for r, ds, fs in os.walk("."):
    ds[:] = [d for d in ds if not (r == "." and d in (".git", ".venv"))]
    for f in fs:
        allfiles.add(os.path.join(r, f)[2:].replace(chr(92), "/"))
results_md = Path("RESULTS.md").read_text(encoding="utf-8", errors="replace")
toks = set(re.findall(r"(?:results|scripts|data|docs|configs|src|build|annotation|checkpoints|cache|tests|paper2|paper)/[A-Za-z0-9_./\-]+", results_md))
toks = {t.rstrip(".,;:)").split("{")[0].split("*")[0] for t in toks}
ref_files = set()
unresolved = set()
for t in toks:
    if t in allfiles:
        ref_files.add(t)
    else:
        hit = [f for f in allfiles if f.startswith(t.rstrip("/") + "/")] if len(t) > 8 else []
        if hit:
            ref_files |= set(hit)
        else:
            unresolved.add(t)
top = lambda L: dict(collections.Counter(x.split("/")[0] if "/" in x else "(top level)" for x in L))  # noqa: E731
if mode == "verify":
    print("== counts by top-level folder (files)")
    for k, label in (("A_delete", "deleted (paper-type, identical copy outside the repo)"), ("A_archive", "moved to archive (paper-type, no identical outside copy)"), ("B_gitrm", "git rm (tracked)"), ("C_archive", "moved to archive (untracked caches and drafts)")):
        print(f"  {label}: {len(plan[k])}  {top(plan[k])}")
    print(f"  TOTAL touched: {len(removal)}")
    coll = sorted(f for f in ref_files if f in removal)
    coll_paper = [f for f in coll if f.endswith(PAPER_EXT)]
    coll_other_all = [f for f in coll if not f.endswith(PAPER_EXT)]
    coll_pyc = [f for f in coll_other_all if f.endswith(".pyc") or "/__pycache__/" in f]
    coll_other = [f for f in coll_other_all if f not in coll_pyc]
    coll_tracked = [f for f in coll if f in tracked]
    print("\n== RESULTS.md references")
    print(f"  path tokens in RESULTS.md: {len(toks)}; resolving to files that exist now: {len(ref_files)}; tracked among them: {len(ref_files & tracked)}")
    print(f"  TRACKED referenced files in the removal set: {len(coll_tracked)} {coll_tracked[:10]}")
    print(f"  untracked bytecode caches (*.pyc) under run folders that RESULTS.md names as folders: {len(coll_pyc)} (a folder reference does not reference its bytecode)")
    print(f"  referenced files in the removal set, neither paper-type nor bytecode: {len(coll_other)} {coll_other[:10]}")
    print(f"  referenced files in the removal set, paper-type (removal was ordered): {len(coll_paper)} {coll_paper[:6]}")
    print(f"  RESULTS.md tracked: {'RESULTS.md' in tracked}; not in removal set: {'RESULTS.md' not in removal}")
    print(f"  tokens that do not resolve to any file now (pre-existing, not caused by this cleanup): {len(unresolved)}")
    sys.exit(1 if (coll_other or coll_tracked or "RESULTS.md" in removal) else 0)

# ---------------------------------------------------------------- apply
rows = []
ARCH.mkdir(parents=True, exist_ok=True)


def row(group, action, path, size, h, note, same):
    rows.append([group, action, path, size, h, note, same])


for p in plan["A_delete"]:
    if not os.path.exists(p):
        continue
    size = os.path.getsize(p)
    h = sha(p)
    same = ""
    for root in OUTSIDE:
        for r, ds, fs in os.walk(root):
            for f in fs:
                q = os.path.join(r, f)
                if os.path.getsize(q) == size and sha(q) == h:
                    same = q.replace(chr(92), "/")
                    break
            if same:
                break
        if same:
            break
    assert same, f"no identical outside copy for {p}"
    assert p not in tracked
    os.remove(p)
    row("C2-A", "deleted (untracked paper-type file)", p, size, h, "identical copy kept outside the repo", same)
for k, grp in (("A_archive", "C2-A"), ("C_archive", "C2-C")):
    for p in plan[k]:
        if not os.path.exists(p):
            continue
        assert p not in tracked, p
        size = os.path.getsize(p)
        h = sha(p)
        dst = ARCH / "cleanup2" / p
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dst)
        assert sha(dst) == h
        os.remove(p)
        row(grp, "moved to archive (untracked)", p, size, h, "archive folder: cleanup_archive_2026-11-09/cleanup2/", "")
for p in plan["B_gitrm"]:
    if not os.path.exists(p):
        continue
    size = os.path.getsize(p)
    h = sha(p)
    subprocess.run(["git", "rm", "-q", "--", p], check=True)
    row("C2-B", "git rm (tracked; recoverable from history)", p, size, h, "", "")
# empty folders (not the Kaggle config folders)
removed = []
for r, ds, fs in sorted(os.walk("."), key=lambda x: -len(x[0])):
    rel = r[2:].replace(chr(92), "/")
    if not rel or rel.split("/")[0] in (".git", ".venv") or rel.startswith("build/kaggle_config_"):
        continue
    try:
        if not os.listdir(r):
            os.rmdir(r)
            removed.append(rel)
    except OSError:
        pass
for rel in removed:
    row("C2-D", "removed empty folder", rel + "/", 0, "", "", "")
mf = REPO / "results" / "CLEANUP_MANIFEST.csv"
with open(mf, "a", encoding="utf-8", newline="") as f:
    csv.writer(f).writerows(rows)
shutil.copy2(mf, ARCH / "MANIFEST_cleanup2_rows.csv") if False else None
print(f"applied: {len(rows)} manifest rows; empty folders removed: {len(removed)}")
print(collections.Counter(r[0] + " " + r[1] for r in rows))
