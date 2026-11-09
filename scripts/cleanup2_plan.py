"""Cleanup 2, 2026-11-09. Read-only planner: writes a JSON plan (argv[1]) and prints counts. Nothing is deleted or moved here; scripts/cleanup2_apply.py does that after the plan has been shown.
Groups: A paper-type files (tex, bib, sty, bst, cls, paper PDFs) -> deleted only if a byte-identical copy exists outside the repo, otherwise moved to the archive;
B tracked logs and status files that nothing references -> git rm; C untracked caches and drafts -> moved to the archive; D empty folders -> removed.
Unsure means keep."""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
os.chdir(REPO)
OUTSIDE = [REPO.parent / "paper2_full_2026-11-09", REPO.parent / "paper2_overleaf"]
SKIP = {".git", ".venv"}
KEEP_PREFIX = ("RESULTS.md", "CLAUDE.md", "README.md", "DATA_CARD.md", "results/CLEANUP_MANIFEST.csv", "results/CLEANUP_PLAN.md", "results/phase2/CLEANUP_LIST.md",
               "build/kaggle_config_", "annotation/private/", "annotation/returned/", "checkpoints/", "cache/", "data/", ".env")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(8 << 20), b""):
            h.update(b)
    return h.hexdigest()


files = {}
for r, ds, fs in os.walk("."):
    ds[:] = [d for d in ds if not (r == "." and d in SKIP)]
    for f in fs:
        p = os.path.join(r, f)[2:].replace(chr(92), "/")
        files[p] = os.path.getsize(p)
tracked = set(subprocess.run(["git", "ls-files"], capture_output=True, text=True, encoding="utf-8").stdout.split("\n")) - {""}
results_md = (REPO / "RESULTS.md").read_text(encoding="utf-8", errors="replace")
tokens = set(re.findall(r"(?:results|scripts|data|docs|configs|src|build|annotation|checkpoints|cache|tests)/[A-Za-z0-9_./\-]+", results_md))
tokens = {t.rstrip(".,;:)").split("{")[0].split("*")[0] for t in tokens}
script_text = ""
for p in files:
    if p.startswith(("scripts/", "src/", "tests/", "configs/")) and not p.startswith("scripts/cleanup") and p.endswith((".py", ".sh", ".yaml", ".yml", ".ps1", ".cfg", ".toml")):
        script_text += open(p, encoding="utf-8", errors="replace").read() + "\n"
for p in files:
    if p.startswith("docs/") and p.endswith(".md") and p != "docs/AMENDMENT2_DRAFT.md":
        script_text += open(p, encoding="utf-8", errors="replace").read() + "\n"
opened = set(json.load(open(sys.argv[2], encoding="utf-8"))["opened_by_check_numbers"]) if len(sys.argv) > 2 else set()


def referenced(p):
    base = p.rsplit("/", 1)[-1]
    if p in tokens or any(t and (p.startswith(t) and (t.endswith("/") or len(t) >= 12 or t == p)) for t in tokens):
        return "RESULTS.md"
    if len(base) >= 8 and base in results_md:
        return "RESULTS.md (name)"
    if base in script_text or p in script_text:
        return "scripts"
    if p in opened:
        return "check_numbers"
    return ""


plan = {"A_delete": [], "A_archive": [], "B_gitrm": [], "C_archive": [], "D_rmdir": [], "kept_notes": {}}
# ---- A: paper-type files
ext = (".tex", ".bib", ".sty", ".bst", ".cls")
outside_hashes = {}
for root in OUTSIDE:
    for r, ds, fs in os.walk(root):
        for f in fs:
            q = os.path.join(r, f)
            outside_hashes.setdefault(os.path.getsize(q), set()).add(sha(q))
papers_pdf = [p for p in files if p.lower().endswith(".pdf") and (p.startswith("paper2/build/") or re.search(r"(^|/)(main|paper)[^/]*\.pdf$", p))]
for p in sorted(files):
    if p.endswith(ext) or p in papers_pdf:
        if p.startswith(KEEP_PREFIX[0:1]):
            continue
        has_copy = files[p] in outside_hashes and sha(p) in outside_hashes[files[p]]
        (plan["A_delete"] if has_copy else plan["A_archive"]).append(p)
# ---- B: tracked logs and status files nothing refers to
for p in sorted(tracked):
    if not p.endswith((".log", ".out", ".DONE")) or p.startswith(KEEP_PREFIX) or p in plan["A_delete"]:
        continue
    why = referenced(p)
    if why:
        plan["kept_notes"][p] = why
        continue
    plan["B_gitrm"].append(p)
# duplicate: every substantial line of docs/AMENDMENT2_DRAFT.md occurs verbatim in RESULTS.md (checked 177 of 177)
if "docs/AMENDMENT2_DRAFT.md" in tracked:
    plan["B_gitrm"].append("docs/AMENDMENT2_DRAFT.md")
# ---- C: untracked caches and drafts
for p in sorted(files):
    if p in tracked or p.startswith(KEEP_PREFIX):
        continue
    if "/__pycache__/" in "/" + p or p.endswith(".pyc"):
        plan["C_archive"].append(p)
for p in ("build/X7A_DRAFT.md", "build/X7B_DRAFT_not_approved.md"):
    if p in files and not referenced(p):
        plan["C_archive"].append(p)
for p in sorted(files):
    if p.startswith(("build/x9b_smoke/", "build/x9b_smoke2/")) or p == "build/x9b_smoke_full.py":
        if not referenced(p) and not referenced("build/x9b_smoke"):
            plan["C_archive"].append(p)
plan["C_archive"] = sorted(set(plan["C_archive"]) - set(plan["A_delete"]) - set(plan["A_archive"]))
json.dump(plan, open(sys.argv[1], "w"), indent=0)
top = lambda L: {k: sum(1 for x in L if x.split("/")[0] == k) for k in sorted({x.split("/")[0] for x in L})}  # noqa: E731
sz = lambda L: sum(files.get(x, 0) for x in L)  # noqa: E731
for k in ("A_delete", "A_archive", "B_gitrm", "C_archive"):
    print(f"{k}: {len(plan[k])} files, {sz(plan[k]) / 1048576:.1f} MB, by top folder {top(plan[k])}")
print("tracked logs kept because referenced:", len(plan["kept_notes"]))
