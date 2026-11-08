"""Cleanup plan, 2026-11-09. Read-only: groups candidates, writes results/CLEANUP_PLAN.md and a machine-readable plan JSON (argv[2]) that scripts/cleanup_apply.py executes.
Uses the list of files check_numbers opens (scripts/cleanup_scan.py output, argv[1]). Deletes and moves nothing."""
import collections
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
os.chdir(REPO)
scan = json.load(open(sys.argv[1], encoding="utf-8"))
OPENED = set(scan["opened_by_check_numbers"])
TRACKED = set(scan["tracked"])
PROTECTED_PREFIX = ["RESULTS.md", "paper2/", "scripts/", "docs/", "results/phase2/dump/", "results/phase2/FULL_RESULTS_DUMP.md", "results/phase2/RESULTS_FLAT.md", "results/phase2/RESULTS_READABLE.md",
                    "results/phase2/CLEANUP_LIST.md", "results/CHAIN_STATUS_X10", "results/phase2/x10", "results/kaggle/acct3", "build/kaggle_acct3",
                    "build/kaggle_config_", "build/kaggle_acct3_aarnavkembhavi_failed", ".git/", ".venv/", ".env", "cache/llm_cache.sqlite", "CLAUDE.md", "README.md", "annotation/private/", "annotation/returned/"]
SKIPDIRS = {".git", ".venv"}
MB = 1024 * 1024


def prot(rel):
    return any(rel == p or rel.startswith(p) for p in PROTECTED_PREFIX)


def walk():
    for r, ds, fs in os.walk("."):
        ds[:] = [d for d in ds if not (r == "." and d in SKIPDIRS)]
        for f in fs:
            p = os.path.join(r, f)[2:].replace(chr(92), "/")
            try:
                yield p, os.path.getsize(p)
            except OSError:
                pass


FILES = dict(walk())
refs_text = (REPO / "RESULTS.md").read_text(encoding="utf-8", errors="replace")
for p, _ in FILES.items():
    if p.startswith("paper2/") and re.search(r"\.(py|tex|md|json)$", p) and not p.startswith("paper2/bib") and "build" not in p.split("/")[:2]:
        try:
            refs_text += "\n" + (REPO / p).read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass


REFS2 = set()
for sp in list(Path("scripts").glob("kaggle_*.py")) + list(Path("scripts").glob("x13*.py")) + list(Path("scripts").glob("x12*.py")) + list(Path("scripts").glob("x9b*.py")) + list(Path("scripts").glob("acct*")) + list(Path("scripts").glob("x10*.py")):
    try:
        REFS2 |= set(re.findall(r"results/[A-Za-z0-9_./-]+", sp.read_text(encoding="utf-8", errors="replace")))
    except OSError:
        pass
REFS2 |= {"results/e0c_sib/scores", "results/m4b_mapping", "results/m14_full/words.json", "results/e09_romanize/best_schemes.json"}


def referenced(rel):
    if any(rel == r or rel.startswith(r.rstrip("/") + "/") for r in REFS2):
        return True
    if rel in OPENED or rel in refs_text:
        return True
    base = rel.rsplit("/", 1)[-1]
    return len(base) >= 12 and base in refs_text


groups = collections.OrderedDict()


def add(name, why, action, files, note=""):
    files = sorted(set(files))
    groups[name] = dict(why=why, action=action, files=files, count=len(files), bytes=sum(FILES.get(f, 0) for f in files), note=note)


# 1 caches under unprotected dirs
add("G1 __pycache__ and *.pyc (src/, tests/, root; untracked)", "Python bytecode, regenerated on import, gitignored.", "delete",
    [p for p in FILES if (("/__pycache__/" in "/" + p) or p.endswith(".pyc")) and not prot(p) and p not in TRACKED])
add("G1b __pycache__ inside scripts/ and paper2/ (protected, not touched)", "Same kind, but the instruction forbids touching scripts/ and paper2/.", "keep (protected)",
    [p for p in FILES if (("/__pycache__/" in "/" + p) or p.endswith(".pyc")) and prot(p)])
add("G2 tool caches (.pytest_cache, .ipynb_checkpoints, .mypy_cache, .ruff_cache; untracked)", "Tool caches, regenerated on the next run.", "delete",
    [p for p in FILES if re.search(r"(^|/)(\.pytest_cache|\.ipynb_checkpoints|\.mypy_cache|\.ruff_cache)/", p) and not prot(p) and p not in TRACKED])
add("G3 temp and partial files (*.tmp, *.part, *.partial, *.swp, *~, *.orig; untracked)", "Leftovers of interrupted writes; no run reads them.", "delete",
    [p for p in FILES if re.search(r"(\.tmp|\.part|\.partial|\.swp|\.orig|~)$", p) and not prot(p) and p not in TRACKED])
# 4 checkpoints
ck = [p for p in FILES if p.startswith("checkpoints/")]
dirs_with_final = {p.rsplit("/", 1)[0] for p in ck if p.endswith("/final.safetensors")}
add("G4a resume checkpoints (checkpoints/e05/*/last.pt; weights and optimizer state of finished runs)", "Each run directory has its final.safetensors; last.pt is only for resuming an interrupted run, and the run is complete.", "delete",
    [p for p in ck if p.endswith("/last.pt") and p.rsplit("/", 1)[0] in dirs_with_final])
add("G4b intermediate snapshots (checkpoints/e05/*/snapshot_step*.safetensors)", "Mid-training copies of runs whose final.safetensors exists; the results derived from them are saved under results/.", "delete",
    [p for p in ck if "/snapshot_step" in p and p.rsplit("/", 1)[0] in dirs_with_final])
add("G4c final weights (checkpoints/e05/*/final.safetensors)", "Needed to rerun any tiny-GPT probe; not in the backup (weights are excluded by instruction); retraining takes GPU days.", "keep",
    [p for p in ck if p.endswith("/final.safetensors")])
# 5 activation cache
add("G5 activation caches (cache/activations/**/*.npz; untracked, gitignored)", "Cache of per-layer activations keyed by model, form and item list; every number derived from them is saved in results/ and the paper numbers are checked from results/.", "delete",
    [p for p in FILES if p.startswith("cache/activations/")], note="Regenerated by rerunning the scoring scripts (GPU hours).")
add("G5b cache/llm_cache.sqlite", "The API response cache; the rules say it is never deleted.", "keep", [p for p in FILES if p == "cache/llm_cache.sqlite"])
# 6 duplicates: same size and sha256, unprotected, outside .venv; keep the preferred copy
by_size = collections.defaultdict(list)
for p, s in FILES.items():
    if s >= 1024 and s < 300 * MB and not p.endswith(".pyc") and (p.startswith("results/kaggle/") and "/repo/" in p or not p.startswith(("results/", "cache/", "checkpoints/", "build/", "data/", "annotation/"))):
        by_size[s].append(p)
dup_del, dup_arch, dup_keep_for = [], [], {}
for s, ps in by_size.items():
    if len(ps) < 2:
        continue
    h = collections.defaultdict(list)
    for p in ps:
        h[hashlib.sha256(open(p, "rb").read()).hexdigest()].append(p)
    for hh, grp in h.items():
        if len(grp) < 2:
            continue
        # keep: protected, then opened by check_numbers, then referenced, then tracked, then shortest path
        snap = lambda p: p.startswith("results/kaggle/") and "/repo/" in p  # noqa: E731
        grp.sort(key=lambda p: (snap(p), not prot(p), p not in TRACKED, len(p), p))
        keep = grp[0]
        for p in grp[1:]:
            if prot(p) or not snap(p) or p in OPENED or p in refs_text or p.endswith(".pyc") or "/__pycache__/" in p:
                continue
            dup_keep_for[p] = keep
            (dup_arch if p in TRACKED else dup_del).append(p)
add("G6a duplicate copies, untracked (identical sha256 to a kept copy)", "Byte-identical to a copy that is kept (listed in the manifest).", "delete", dup_del)
add("G6b duplicate copies, tracked (identical sha256 to a kept copy)", "Byte-identical to a kept copy; tracked, so moved to the archive folder, not deleted.", "archive", dup_arch)
# 7 tracked raw results not referenced
cand = []
for p in sorted(TRACKED):
    if not p.startswith("results/") or prot(p) or p in dup_arch:
        continue
    if p in OPENED or referenced(p) or (p.startswith("results/kaggle/") and "/repo/" in p):
        continue
    if FILES.get(p, 0) < 50 * 1024:
        continue
    cand.append(p)
add("G7 tracked raw results (>= 50 KB) that check_numbers does not open and that RESULTS.md and paper2/ do not name", "Per-item or per-layer files from which the summary files were computed; the summaries are what check_numbers and the paper read. Moved, not deleted.", "archive", cand)
# 8 logs and status files (listed only)
add("G8 stale logs and chain status files (untracked: results/*.log, results/CHAIN_STATUS_*.md, build/*.log)", "Heartbeat and run logs of finished chains. They are evidence for incidents logged in RESULTS.md, so they are listed, not deleted.", "keep (decision)",
    [p for p in FILES if p not in TRACKED and not prot(p) and (re.fullmatch(r"results/[^/]+\.log", p) or re.fullmatch(r"results/CHAIN_STATUS[^/]*\.md", p) or re.fullmatch(r"build/[^/]+\.log", p))])
add("G9 build/ staging folders (untracked, gitignored)", "Kaggle packaging copies; the runners on accounts 1 and 2 may still push from them, so they are kept.", "keep",
    [p for p in FILES if p.startswith("build/") and not prot(p) and p not in dup_del])
add("G10 data/processed derived streams and data/raw downloads", "Inputs for any rerun, not in the backup; regenerable with checksums but slow.", "keep", [p for p in FILES if p.startswith("data/")])
add("G11 Kaggle adapters and weights under results/kaggle (untracked, 25 files)", "Final adapters of the X9b runs and similar; not caches.", "keep",
    [p for p in FILES if p.startswith("results/kaggle/") and re.search(r"\.(safetensors|pt)$", p) and not prot(p)])

total_files = len(FILES)
total_bytes = sum(FILES.values())
plan = {"groups": {k: {kk: vv for kk, vv in v.items()} for k, v in groups.items()}, "dup_keep_for": dup_keep_for, "total_files": total_files, "total_bytes": total_bytes}
Path(sys.argv[2]).write_text(json.dumps(plan), encoding="utf-8")


def fmt(b):
    return f"{b / MB:,.1f} MB" if b < 1024 * MB else f"{b / 1024 / MB:,.2f} GB"


lines = ["# Cleanup plan (2026-11-09)", "",
         "Scope: the repository tree except `.git/` and `.venv/`. Git history and tags are not touched. Protected, never touched: RESULTS.md, paper2/, scripts/, docs/, the dump, flat and readable files under results/phase2, "
         "`results/phase2/CLEANUP_LIST.md`, `C:\\PROJECTS\\PROMPT\\backup_phase2_2026-11-08\\`, and everything the Sarvam-m X10 chain reads or writes (CHAIN_STATUS_X10*, results/phase2/x10*, results/kaggle/acct3*, build/kaggle_acct3*, build/kaggle_config_*) until that run has finished.",
         "Method: `scripts/cleanup_scan.py` records every file `paper2/scripts/check_numbers.py` opens over all 13 sections (554 files, of which 128 under results/); `scripts/cleanup_plan.py` groups candidates.", "",
         f"Tree now: {total_files:,} files, {fmt(total_bytes)}.", "", "| Group | Action | Files | Size | Why it is safe |", "|---|---|---:|---:|---|"]
for k, v in groups.items():
    lines.append(f"| {k} | {v['action']} | {v['count']:,} | {fmt(v['bytes'])} | {v['why']}{(' ' + v['note']) if v['note'] else ''} |")
dele = [v for v in groups.values() if v["action"] == "delete"]
arch = [v for v in groups.values() if v["action"] == "archive"]
lines += ["", "## Totals", "",
          f"- Delete (untracked caches, temp files, duplicates, checkpoints): {sum(v['count'] for v in dele):,} files, {fmt(sum(v['bytes'] for v in dele))}.",
          f"- Move to the archive folder outside the repo (tracked, listed in a manifest, not deleted): {sum(v['count'] for v in arch):,} files, {fmt(sum(v['bytes'] for v in arch))}.",
          f"- Kept: everything else ({total_files - sum(v['count'] for v in dele + arch):,} files).", ""]
lines += ["## Largest folders inside the archive group (G7)", ""]
agg = collections.Counter()
for f in groups["G7 tracked raw results (>= 50 KB) that check_numbers does not open and that RESULTS.md and paper2/ do not name"]["files"]:
    agg["/".join(f.split("/")[:3])] += FILES[f]
for d, b in agg.most_common(25):
    lines.append(f"- `{d}`: {fmt(b)}")
Path(REPO / "results" / "CLEANUP_PLAN.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines[8:]))
