"""Anonymized code and data package for the TMLR submission (supplementary material, up to 100 MB, ZIP).

What it does
  1. Runs the paper's table, figure and number-check scripts under a file-open spy and records every file they read, so the
     package contains exactly the result files needed to rebuild every table and figure (no GPU needed).
  2. Copies the code (src/, scripts/, configs/, tests/, paper2/ sources, tables, figures and scripts), the data files the
     annotation pipeline needs, DATA_CARD.md, DATASHEET.md, the registration log RESULTS.md, and the traced result files
     into build/anon_package/, with git history, caches, logs, chain status files, annotator workbooks and messages left out.
  3. Scrubs text files: the lead author's name, user name, institution, e-mail address, absolute paths and other project
     names are replaced by neutral placeholders.
  4. Verifies that no identifying string remains (text and binary files, file names), writes README.md, and zips the package.

Usage: python scripts/anon_package.py [--no-trace]      (rerun after the gating results are in; --no-trace reuses the last trace)
Output: build/anon_package/ (the tree), build/anon_code_and_data.zip, build/anon_package_report.json
"""
import ast
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
PKG = BUILD / "anon_package"
ZIP = BUILD / "anon_code_and_data.zip"
TRACE = BUILD / "anon_trace.json"
PY = ROOT / ".venv" / "Scripts" / "python.exe"
SECTIONS = ["intro", "related", "setup", "controlled", "accuracy", "assembly", "familiarity", "limitations", "conclusion",
            "broader_impact", "abstract", "appendix"]

CODE_DIRS = ["src", "scripts", "configs", "tests", "paper2/scripts", "paper2/tables", "paper2/figures"]
CODE_FILES = ["pyproject.toml", "requirements.in", "requirements.txt", "DATA_CARD.md", "RESULTS.md",
              "paper2/main.tex", "paper2/refs.bib", "paper2/tmlr.sty", "paper2/tmlr.bst", "paper2/fancyhdr.sty",
              "paper2/refs_original.bib", "paper2/BIB_REPORT.md", "annotation/merge_xlsx.py", "annotation/autocorrect_en_excel16.tsv",
              "annotation/examples_v1.json", "annotation/instructions/annotator_A.md", "annotation/instructions/annotator_B.md",
              "data/annotation/DATASHEET.md", "data/annotation/items_v2.jsonl", "data/annotation/items_v1.jsonl",
              "data/annotation/verified_A_v1.jsonl", "data/annotation/drafts_v1.jsonl", "data/annotation/drafts_regen_v1.jsonl",
              "data/annotation/drafts_replace_v1.jsonl", "data/annotation/replacement_draws_v1.jsonl",
              "data/annotation/blind_v1.json", "data/annotation/source_noise_v1.json",
              "data/annotation/natural_spotcheck20_v1.json", "data/annotation/natural_romanization_e0_check_v1.csv",
              "annotation/results/annotator_A.csv"]  # raw verification: Gemini draft, fine or wrong, fix (no annotator names)
# Gemini outputs and the verified texts (included for reviewers at the lead author's request, 2026-10-27; public release upon acceptance)
EXTRA_GLOBS = ["data/processed/natural_*.jsonl", "results/k3b/drafts.jsonl", "results/k3b/sample.json",
               "results/k3b_hi/drafts.jsonl", "results/k3b_hi/sample.json", "results/k_verified/build.json"]
SKIP_DIRS = {"__pycache__", ".pytest_cache", ".venv", ".git", "build", "cache", "logs", "tmlr_template_ref"}
SKIP_NAMES = {"anon_package.py", "hidden.vbs", "detach.ps1", "detach_test.sh", "chain_watch.sh", "xlshot.ps1", "k_xlsx_selftest.py",
              "k_package.py", "k_xlsx.py"}  # local chain and packaging helpers for the annotation hand-out, not needed to reproduce
TEXT_EXT = {".py", ".md", ".json", ".jsonl", ".csv", ".tsv", ".tex", ".bib", ".bst", ".sty", ".yaml", ".yml", ".toml", ".txt",
            ".sh", ".in", ".cfg", ".ini", ".ps1", ".log", ".aux"}

# (pattern, replacement), applied in order to every text file
SCRUB = [
    (r"C:[\\/]+PROJECTS[\\/]+PROMPT[\\/]+shattered-scripts", "<repo>"),
    (r"/c/PROJECTS/PROMPT/shattered-scripts", "<repo>"),
    (r"C:[\\/]+Users[\\/]+kembh", "<home>"),
    (r"/c/Users/kembh", "<home>"),
    (r"C:[\\/]+PROJECTS[\\/]+ISM", "<other-project>"),
    (r"C:[\\/]+PROJECTS[\\/]+PROMPT", "<projects>"),
    (r"aarnavking21@gmail\.com", "[email removed]"),
    (r"Aarnav's", "the lead author's"),
    (r"Aarnav", "the lead author"),
    (r"aarnav", "lead-author"),
    (r"kembh", "user"),
    (r"RVCE", "[institution]"),
    (r"Prof\.? Manonmani S?", "[supervisor]"),  # added 2026-11-03 (lead author)
    (r"manonmanis", "[supervisor]"),
    (r"Manonmani", "[supervisor]"),
    (r"Ashwin Bhat", "[co-author]"),
    (r"Aakarsh Prabhu", "[co-author]"),
    # bare "Bhat", "Prabhu" and "Prabhu, Aakarsh" are NOT scrubbed (other authors' bib entries); they are listed by the check below
    (r"\bISM\b", "another project"),
]
IDENT = [r"manonmani", r"ashwin", r"aakarsh", r"aarnav", r"kembh", r"rvce", r"gmail", r"king21", r"C:[\\/]", r"[\\/]Users[\\/]", r"PROJECTS", r"\bISM\b"]


def run_trace() -> list:
    BUILD.mkdir(exist_ok=True)
    runner = BUILD / "anon_trace_runner.py"
    runner.write_text('''
import builtins, io, json, os, runpy, sys
root, out, targets = os.path.abspath(sys.argv[1]), sys.argv[2], json.loads(sys.argv[3])
seen = set()
_open = builtins.open
def spy(file, *a, **k):
    try:
        if isinstance(file, (str, os.PathLike)):
            p = os.path.abspath(file)
            if p.startswith(root):
                seen.add(p)
    except Exception:
        pass
    return _open(file, *a, **k)
builtins.open = spy
io.open = spy
import pandas as pd
_rp = pd.read_parquet
def rp(path, *a, **k):
    seen.add(os.path.abspath(str(path)))
    return _rp(path, *a, **k)
pd.read_parquet = rp
for t in targets:
    sys.argv = list(t)
    sys.path.insert(0, os.path.dirname(os.path.abspath(t[0])))
    try:
        runpy.run_path(t[0], run_name="__main__")
    except SystemExit:
        pass
    except Exception as e:
        print("trace target failed:", t, repr(e))
    sys.path.pop(0)
json.dump(sorted(seen), open(out, "w"))
''', encoding="utf-8")
    targets = [["paper2/scripts/make_tables.py"], ["paper2/scripts/make_figures.py"]] + \
              [["paper2/scripts/check_numbers.py", "--section", s] for s in SECTIONS]
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    subprocess.run([str(PY), str(runner), str(ROOT), str(TRACE), json.dumps(targets)], cwd=ROOT, env=env, check=True)
    return json.loads(TRACE.read_text(encoding="utf-8"))


def want(p: Path) -> bool:
    rel = p.relative_to(ROOT).as_posix()
    png_dup = rel.startswith("paper2/figures/") and p.suffix == ".png"  # the paper uses the PDFs; PNGs only add noise to the scan
    big_vectors = rel.startswith("results/k12/vectors/")  # regenerable GPU vectors (README of the repo explains how); never in the package
    return (not (set(p.parts) & SKIP_DIRS) and p.name not in SKIP_NAMES and not rel.startswith("results/CHAIN_STATUS") and not png_dup
            and not big_vectors and "shattered-scripts-archive" not in p.as_posix())


def collect(traced: list) -> list:
    files = set()
    for d in CODE_DIRS:
        for p in (ROOT / d).rglob("*"):
            if p.is_file() and want(p):
                files.add(p)
    for f in CODE_FILES:
        if (ROOT / f).is_file():
            files.add(ROOT / f)
    for g in EXTRA_GLOBS:
        for p in ROOT.glob(g):
            if p.is_file() and want(p):
                files.add(p)
    for t in traced:
        p = Path(t)
        rel = p.relative_to(ROOT).as_posix()
        if p.is_file() and want(p) and (rel.startswith(("results/", "data/", "annotation/")) or True):
            files.add(p)
    # tests and figures are fine; local build products and notebooks are not
    return sorted(f for f in files if f.suffix not in {".pyc", ".log"} and "NUMBERS" not in f.name or f.name.startswith("NUMBERS_"))


def scrub(text: str) -> str:
    for pat, rep in SCRUB:
        text = re.sub(pat, rep, text, flags=re.I if pat.lower() in ("aarnav", "kembh", "rvce", "manonmanis", "manonmani") else 0)
    return text


def copy_all(files: list) -> dict:
    if PKG.exists():
        shutil.rmtree(PKG)
    stats = {"files": 0, "scrubbed_text": 0, "binary": 0, "bytes": 0}
    for p in files:
        dest = PKG / p.relative_to(ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix.lower() in TEXT_EXT:
            try:
                t = p.read_text(encoding="utf-8")
                new = scrub(t)
                dest.write_text(new, encoding="utf-8", newline="\n")
                stats["scrubbed_text"] += 1
            except UnicodeDecodeError:
                shutil.copyfile(p, dest)
                stats["binary"] += 1
        else:
            shutil.copyfile(p, dest)
            stats["binary"] += 1
        stats["files"] += 1
        stats["bytes"] += dest.stat().st_size
    return stats


def experiment_index() -> str:
    """Table of scripts with their one-line description and Usage lines, read from their docstrings."""
    groups = [
        ("Forms and data (Section 3)", ["e02_translit", "e09_search", "e09_eval", "e0b_natural", "m4c_natural_flores", "e00_gate", "e01_cost"]),
        ("Tiny GPTs (Section 4)", ["e05_pretrain", "e05_analysis", "m1_tiny_mdl"]),
        ("Accuracy (Section 5)", ["e0b_familiarity", "e0c_sib", "matched_samples", "e0b_backtranslate", "e0b_backtranslate_control"]),
        ("Assembly and patching (Section 6)", ["m14_full", "m14_gate2", "m4b_mapping", "m4b_surface", "m4b_robustness", "m4c_surface",
                                              "ep_patching", "ep_robust"]),
        ("Ladder, segmentation, Hindi, annotation (Section 7)", ["l_ladder", "l_ladder_posthoc", "nc1", "nc1_posthoc", "english_share",
                                                              "h_hindi", "h1lf", "k3b_dakshina", "k_annotation", "k_verified", "v_ver",
                                                              "v_dbl", "k_k12", "codemix_check"]),
    ]
    out = []
    for title, names in groups:
        out.append(f"### {title}\n")
        for n in names:
            f = ROOT / "scripts" / f"{n}.py"
            if not f.exists():
                continue
            doc = ast.get_docstring(ast.parse(f.read_text(encoding="utf-8"))) or ""
            first = re.sub(r"\s+", " ", doc.split("\n\n")[0])[:260]
            usage = [l.strip() for l in doc.splitlines() if l.strip().startswith(("python ", "Usage:"))]
            out.append(f"- `scripts/{n}.py`: {scrub(first)}" + ("\n  " + "\n  ".join(f"`{scrub(u)}`" for u in usage[:4]) if usage else ""))
        out.append("")
    return "\n".join(out)


README = """# Shattered Scripts: code and data package (anonymized for review)

This package accompanies the TMLR submission "Shattered Scripts: Familiarity Outweighs Fragmentation in How Language Models Read
Romanized Kannada". Names, institution, user names, absolute paths and git history have been removed. The complete data
release will follow upon acceptance.

## 1. Rebuild every table, figure and number check (CPU, minutes, no models)

The result files the paper reads are included under `results/`. Python 3.12; the pins are in `requirements.txt`
(`torch` is only needed to run models, not to rebuild tables).

```
pip install -r requirements.txt            # or: uv pip install -r requirements.txt
python paper2/scripts/make_tables.py        # paper2/tables/*.tex from results/ (0 MISSING cells expected)
python paper2/scripts/make_figures.py       # paper2/figures/*.pdf
for s in intro related setup controlled accuracy assembly familiarity limitations conclusion broader_impact abstract appendix; do
  python paper2/scripts/check_numbers.py --section $s   # every number in the section text vs the result files
done
```
`check_numbers.py` prints, per section, the number of claims, the claims that do not match the stored value, and the numbers in
the text that no claim traces; the expected output is no mismatches and no untraced numbers. The generated `paper2/NUMBERS_*.md`
list every claim with the file it is read from. To compile the paper: `cd paper && pdflatex main && bibtex main && pdflatex main`
(needs `tmlr.sty`, `tmlr.bst`, `fancyhdr.sty`, included).

## 2. Which result files back which table

| Paper table or figure | Generated by | Result files |
|---|---|---|
| Models (tab:models) | `make_tables.py` `models_table` | `results/matched/tokens_per_word.csv`, `results/m4b_mapping/summary.csv`, `results/ep1/raw/` |
| Tiny GPTs (tab:tiny) | `tiny_table` | `results/e05_pretrain/T6.csv`, `results/m1_tiny_mdl/summary.csv` |
| Accuracy (tab:accuracy and appendix) | `accuracy_tables`, `xnli_table` | `results/matched/accuracy.csv`, `results/e0c_sib/gate/accuracy.csv`, `results/e0b_familiarity/gate1/accuracy.csv` |
| Word assembly (tab:assembly) | `assembly_table` | `results/m14_full/gate2/paired.csv`, `results/e00_gate/tokens_per_word.csv` |
| Retrieval (appendix) | `retrieval_tables` | `results/m4c_natural/summary.csv`, `results/l_ladder/retrieval.csv`, `results/m14_full/gate2/m4.csv` |
| Contrasts (tab:contrasts, appendix) | `contrasts_table`, `ladder_appendix` | `results/l_ladder/{verdict.json,contrasts.csv}`, `results/nc1/{verdict.json,contrasts.csv}` |
| Hindi (tab:hindi) | `hindi_table` | `results/h_hindi/h1_verdict.json`, `results/h1lf/opt2_verdict.json` |
| Verification, vowel doubling (appendix) | `verification_appendix` | `results/v_ver/differences.csv`, `results/v_dbl/differences.csv` |
| Figures (alignment, patching, tiny GPTs) | `make_figures.py` | `results/m14_full`, `results/ep2/`, `results/e05_pretrain/` |

Other numbers in the text are traced to files by the claims in `paper2/scripts/section_claims.py`, `section_claims7.py` and
`check_numbers.py`.

## 3. Recompute the results (GPU)

All model runs used one RTX 3070 Laptop GPU (8 GB), bf16 for interpretability, one model loaded at a time. Datasets are
downloaded from their official sources by the scripts (revisions and licenses in `DATA_CARD.md`). `RESULTS.md` is the
registration and results log: every experiment was registered before it ran, every outcome is recorded there against its
registration (confirmed, refuted or inconclusive), and every exploratory analysis is labelled as such. Cached model
activations (about 17 GB) are not included; the scripts regenerate them.

Scripts by paper section (usage lines are read from each script's docstring):

{index}

## 4. Gemini drafts, verification and annotation data

Included for reviewers (public release upon acceptance): all Gemini romanizations used in the experiments
(`data/processed/natural_*.jsonl`, with `_verified_` variants where native-speaker verified text replaces a draft), the Gemini
Kanglish and natural drafts shown to annotators (`data/annotation/drafts_*.jsonl`), the Dakshina comparison drafts
(`results/k3b/drafts.jsonl`), and the raw verification (`annotation/results/annotator_A.csv`).

`data/annotation/` has the items, the Gemini drafts shown to annotators, the verification by a pool of native Kannada speakers
(`verified_A_v1.jsonl`: fine or wrong with a fix per draft; natural romanization uses the draft for one item whose fix dropped
content) and the datasheet (`DATASHEET.md`). `annotation/merge_xlsx.py` reads the returned workbooks; no annotator names or
identifiers are included.

## 5. Notes for reviewers

- Every number in the paper's text is read from a file in `results/` by `check_numbers.py`; none is typed by hand.
- Experiments marked exploratory or post hoc in the paper are labelled the same way in `RESULTS.md`.
- Gemini was used only to draft romanizations (`gemini-3.5-flash-lite`); the drafts and cached outputs are in `data/`.
"""


def verify() -> dict:
    pats = [re.compile(p, re.I if p.islower() else 0) for p in IDENT]
    hits, n = [], 0
    for p in PKG.rglob("*"):
        rel = p.relative_to(PKG).as_posix()
        for pat in pats:
            if pat.search(rel):
                hits.append((rel, "file name", pat.pattern))
        if not p.is_file():
            continue
        n += 1
        data = p.read_bytes()
        text = data.decode("latin-1")
        for pat in pats:
            m = pat.search(text)
            if m:
                hits.append((rel, text[max(0, m.start() - 30):m.end() + 30].replace("\n", " "), pat.pattern))
    return {"files_scanned": n, "hits": hits}


def main():
    traced = json.loads(TRACE.read_text(encoding="utf-8")) if "--no-trace" in sys.argv and TRACE.exists() else run_trace()
    files = collect(traced)
    stats = copy_all(files)
    (PKG / "README.md").write_text(scrub(README.replace("{index}", experiment_index())), encoding="utf-8", newline="\n")
    ver = verify()
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(PKG.rglob("*")):
            if p.is_file():
                z.write(p, Path("shattered-scripts-anon") / p.relative_to(PKG))
    rep = {**stats, "zip_bytes": ZIP.stat().st_size, "traced_reads": len(traced), "identifying_hits": len(ver["hits"]),
           "files_scanned": ver["files_scanned"], "hit_details": ver["hits"][:50]}
    (BUILD / "anon_package_report.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: v for k, v in rep.items() if k != "hit_details"}, indent=1))
    for h in ver["hits"][:30]:
        print("HIT", h)
    return 1 if ver["hits"] else 0


if __name__ == "__main__":
    sys.exit(main())
