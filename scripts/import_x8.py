"""Import returned X8 workbooks (X8_P.xlsx, X8_Q.xlsx) into the registered X8 format and validate them.

Checks per file: sheet and header layout, the role letter and file id in the Instructions sheet, 100 rows, the id and Kannada-sentence columns equal to the registered
selection (a mismatch means a locked cell was edited), duplicate ids, missing, blank or non-text Romanization cells. Reported (warnings, never blockers), to catch AutoCorrect damage:
the share of cells starting with an uppercase letter and the share containing characters outside the expected romanization set (ASCII letters, digits, space and ASCII punctuation;
anything else, such as curly quotes, ellipsis, dashes, emoji or Kannada script, is listed). Blockers stop the write unless --partial is given (then only the valid answered rows are written).
Writes results/phase2/x8/x8_annotator_<role>.json in the format of the HTML page export ({"annotator", "n", "answers": [{"index", "romanization"}]}) and
results/phase2/x8/import_report_<role>.json. Usage: python scripts/import_x8.py returned/X8_P.xlsx [returned/X8_Q.xlsx] [--partial]
"""
import argparse
import json
import re
import sys
from pathlib import Path

from openpyxl import load_workbook

from shattered.runlog import REPO, results_dir, write_json

sys.path.insert(0, str(REPO / "scripts"))
EXPECTED = re.compile(r"^[A-Za-z0-9 .,?!'\"\-:;()/&%+_#*\[\]<>=@$~^|\\{}`]*$")


def expected_items() -> list[dict]:
    import export_xlsx as E
    items, _ = E.x8_items()
    return items


def import_one(path: Path, partial: bool) -> dict:
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
        B.append(f"{len(edited)} rows whose id or Kannada sentence differ from the registered selection (locked cells edited, rows moved or deleted): {edited[:10]}")
    if blank:
        B.append(f"{len(blank)} missing or blank Romanization cells: {blank[:10]}")
    if nontext:
        B.append(f"{len(nontext)} non-text Romanization cells: {nontext[:10]}")
    texts = [a["romanization"] for a in answers]
    upper = [a["index"] for a in answers if a["romanization"][:1].isupper()]
    odd = {}
    for a in answers:
        if not EXPECTED.match(a["romanization"]):
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
    if not B or partial:
        out = results_dir("phase2/x8")
        (out / f"x8_annotator_{role}.json").write_text(json.dumps({"annotator": role, "n": len(answers), "answers": answers}, ensure_ascii=False, indent=1), encoding="utf-8")
        rep["written"] = str((out / f"x8_annotator_{role}.json").relative_to(REPO))
    rep["ok"] = not B
    write_json(results_dir("phase2/x8") / f"import_report_{role}.json", rep, {"source": path.name})
    return rep


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--partial", action="store_true", help="write the valid answered rows even if there are blockers")
    a = ap.parse_args()
    bad = 0
    for f in a.files:
        r = import_one(Path(f), a.partial)
        print(json.dumps({k: v for k, v in r.items() if k not in ("uppercase_first_rows",)}, ensure_ascii=False, indent=1))
        bad += 0 if r.get("ok") else 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
