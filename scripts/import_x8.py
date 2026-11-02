"""Import returned X8 workbooks (X8_P.xlsx, X8_Q.xlsx) into the registered X8 format and validate them.

One command: `python scripts/import_x8.py` reads every X8 workbook in annotation/returned/ (identified by the `File id` line of its Instructions sheet, not by its name; or pass paths),
checks them one by one and as a pair, and writes results/phase2/x8/VALIDATION.md. Options: --partial, --folder DIR, --out DIR (tests).

Per file: sheet and header layout, the role letter and file id, 100 rows, every cell outside the Romanization column equal to the original (the workbooks are unprotected; a difference means an edit, a moved or a deleted row), duplicate ids, missing, blank or non-text Romanization cells. Reported as warnings (never blockers), to catch AutoCorrect damage: the share of cells
starting with an uppercase letter and the share containing characters outside the expected romanization set (ASCII letters, digits, space and ASCII punctuation; curly quotes,
ellipsis, dashes, emoji, Kannada script are listed). As a pair (scripts/import_common.py): P and Q each exactly once, two different files, two different persons (author-field hash),
answers not copies of each other, no file matching a private key. Blockers stop the write unless --partial is given (then only the valid answered rows are written).
Writes results/phase2/x8/x8_annotator_<role>.json in the format of the HTML page export ({"annotator", "n", "answers": [{"index", "romanization"}]}) and
results/phase2/x8/import_report_<role>.json.
"""
import argparse
import json
import re
import sys
from pathlib import Path

from openpyxl import load_workbook

sys.path.insert(0, str(Path(__file__).resolve().parent))
import import_common as C  # noqa: E402

from shattered.runlog import REPO, results_dir, write_json  # noqa: E402

EXPECTED = re.compile(r"^[A-Za-z0-9 .,?!'\"\-:;()/&%+_#*\[\]<>=@$~^|\\{}`]*$")


def expected_items() -> list[dict]:
    import export_xlsx as E
    items, _ = E.x8_items()
    return items


def import_one(path: Path, partial: bool, outdir: Path | None = None, write: bool = True) -> dict:
    rep = {"file": path.name, "blockers": [], "warnings": []}
    B = rep["blockers"]
    wb = load_workbook(path)
    if wb.sheetnames != ["Instructions", "Task"]:
        B.append(f"sheets are {wb.sheetnames}")
        return rep
    ins = "\n".join(str(r[0].value) for r in wb["Instructions"].iter_rows() if r[0].value)
    role = re.search(r"Role letter: ([PQ])\b", ins)
    fid = re.search(r"File id: (\S+)", ins)
    if not role or not fid or fid.group(1) != f"X8_{role.group(1)}":
        B.append("role letter or file id missing or inconsistent")
        return rep
    role = role.group(1)
    rep["role"] = role
    d = C.diff_non_answer(path, f"X8_{role}")
    if d:
        B.append(f"{len(d)} cells outside the answer column differ from the original: {d[:10]}")
    t = wb["Task"]
    if [t.cell(row=1, column=c).value for c in (1, 2, 3)] != ["id", "Kannada sentence", "Romanization"]:
        B.append("header row changed")
    exp = expected_items()
    n_rows = sum(1 for r in range(2, t.max_row + 1) if any(t.cell(row=r, column=c).value not in (None, "") for c in (1, 2, 3)))
    if n_rows != len(exp):
        B.append(f"{n_rows} non-empty rows, expected {len(exp)}")
    ids = [str(t.cell(row=r, column=1).value).strip() if t.cell(row=r, column=1).value is not None else "" for r in range(2, 2 + len(exp))]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        B.append(f"duplicate ids: {dup[:10]}")
    answers, blank, nontext, edited = [], [], [], []
    for k, it in enumerate(exp):
        r = k + 2
        cid, csent, cans = t.cell(row=r, column=1).value, t.cell(row=r, column=2).value, t.cell(row=r, column=3).value
        if str(cid).strip() != str(it["index"]) or csent != it["native"]:
            edited.append(it["index"])
            continue
        if cans is None or (isinstance(cans, str) and not cans.strip()):
            blank.append(it["index"])
            continue
        if not isinstance(cans, str):
            nontext.append(it["index"])
            continue
        answers.append({"index": it["index"], "romanization": cans.strip()})
    if edited:
        B.append(f"{len(edited)} rows whose id or Kannada sentence differ from the registered selection (cells edited, rows moved or deleted): {edited[:10]}")
    if blank:
        B.append(f"{len(blank)} missing or blank Romanization cells: {blank[:10]}")
    if nontext:
        B.append(f"{len(nontext)} non-text Romanization cells: {nontext[:10]}")
    texts = [a["romanization"] for a in answers]
    upper = [a["index"] for a in answers if a["romanization"][:1].isupper()]
    odd = {}
    for a in answers:
        for ch in set(a["romanization"]):
            if not EXPECTED.match(ch):
                odd.setdefault(ch, []).append(a["index"])
    odd_rows = sorted({i for v in odd.values() for i in v})
    rep.update({"n_answers": len(answers), "share_uppercase_first_letter": (len(upper) / len(texts)) if texts else None, "uppercase_first_rows": upper[:20],
                "share_with_unexpected_characters": (len(odd_rows) / len(texts)) if texts else None, "unexpected_characters": {repr(k): len(v) for k, v in odd.items()},
                "share_cells_with_kannada_script": (sum(bool(re.search(r"[ಀ-೿]", x)) for x in texts) / len(texts)) if texts else None,
                "mean_words": (sum(len(x.split()) for x in texts) / len(texts)) if texts else None})
    if texts and rep["share_uppercase_first_letter"] > 0.5:
        rep["warnings"].append("more than half of the cells start with an uppercase letter: AutoCorrect (capitalise first letter) was probably on")
    if texts and rep["share_with_unexpected_characters"] > 0.05:
        rep["warnings"].append("more than 5% of the cells contain characters outside the expected set: AutoCorrect (smart quotes, ellipsis, dashes) was probably on")
    out = outdir or results_dir("phase2/x8")
    if (not B or partial) and write:
        (out / f"x8_annotator_{role}.json").write_text(json.dumps({"annotator": role, "n": len(answers), "answers": answers}, ensure_ascii=False, indent=1), encoding="utf-8")
        rep["written"] = (out / f"x8_annotator_{role}.json").name
    rep["ok"] = not B
    if write:
        write_json(out / f"import_report_{role}.json", rep, {"source": path.name})
    rep["answers"] = answers  # for the pair check only; not in the saved report
    return rep


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--partial", action="store_true", help="write the valid answered rows even if there are blockers")
    ap.add_argument("--folder", default=str(C.RETURNED))
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    outdir = Path(a.out) if a.out else None
    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)
    paths = [Path(f) for f in a.files] or C.returned_files("X8_", Path(a.folder))
    if not paths:
        print(f"no X8 workbook in {a.folder}")
        return 2
    ids = {p: C.file_id(p) for p in paths}
    cross = C.cross_checks(paths, ids, "X8") + [x for x in C.person_overlap_across_kinds(Path(a.folder)) if not x.startswith("WARNING")]
    reports = [import_one(p, a.partial, outdir, write=False) for p in paths]  # first pass: nothing is written until the pair checks are done
    roles = [r.get("role") for r in reports]
    if len(paths) >= 2 and sorted(x for x in roles if x) != ["P", "Q"]:
        cross.append(f"expected one P and one Q file, found roles {roles}")
    ans = {r["role"]: {x["index"]: x["romanization"].strip().lower() for x in r.get("answers", [])} for r in reports if r.get("role")}
    if "P" in ans and "Q" in ans:
        common = set(ans["P"]) & set(ans["Q"])
        same = sum(ans["P"][i] == ans["Q"][i] for i in common)
        if common and same / len(common) > 0.5:
            cross.append(f"P and Q give identical text in {same} of {len(common)} sentences (copied?)")
    if not cross:
        reports = [import_one(p, a.partial, outdir, write=True) for p in paths]
    else:
        print("cross-file blockers: no result file is written")
    out = outdir or results_dir("phase2/x8")
    C.write_md(out / "VALIDATION.md", "X8 import validation", [{k: v for k, v in r.items() if k != "answers"} for r in reports], cross,
               ["", f"Orphan .xlsx files in the folder (no File id): {C.orphans(Path(a.folder))}"])
    for r in reports:
        print(json.dumps({k: v for k, v in r.items() if k not in ("uppercase_first_rows", "answers")}, ensure_ascii=False, indent=1))
    for c in cross:
        print("BLOCKER (cross-file):", c)
    return 1 if (cross or any(not r.get("ok") for r in reports)) else 0


if __name__ == "__main__":
    sys.exit(main())
