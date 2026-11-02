"""Import the returned T3 verification workbook (T3_verification.xlsx) and validate it.

One command: `python scripts/import_t3.py` reads the T3 workbook in annotation/returned/ (identified by the `File id: T3_verification` line; or pass a path) and writes
results/phase2/x1/t3_verification_returned.json and results/phase2/x1/VALIDATION_T3.md. Options: --folder DIR, --out DIR (tests).

Checks: sheets and header; the three instruction ids with the Kannada instruction and gloss unchanged (edited cells); every Verdict is Correct or Needs change (blank or other
text is a blocker); "Needs change" without a corrected Kannada text is a blocker; "Correct" with a corrected text is a warning (the corrected text is kept but marked unused); row T3-2
(the XNLI line, marked "needs rewrite") returned as Correct is a warning; a corrected text containing no Kannada script is a warning. The file is not matched against the private keys
(there are none for T3) but the byte-identical and key-name checks of scripts/import_common.py apply.
This script does NOT change any template: if a line is changed, the corrected file becomes the T3 template and the change is logged by the operator as a dated deviation
(T3_verification.md), before any T3 scoring.
"""
import argparse
import json
import re
import sys
from pathlib import Path

from openpyxl import load_workbook

sys.path.insert(0, str(Path(__file__).resolve().parent))
import import_common as C  # noqa: E402

from shattered.runlog import results_dir, write_json  # noqa: E402

VERDICTS = ["Correct", "Needs change"]


def expected_rows() -> list[tuple]:
    import export_xlsx as E
    return E.T3_ROWS


def import_one(path: Path, outdir: Path | None) -> dict:
    rep = {"file": path.name, "blockers": [], "warnings": []}
    B, W = rep["blockers"], rep["warnings"]
    wb = load_workbook(path)
    if wb.sheetnames != ["Instructions", "Task"]:
        B.append(f"sheets are {wb.sheetnames}")
        return rep
    t = wb["Task"]
    if [t.cell(row=1, column=c).value for c in range(1, 6)] != ["Instruction id", "Kannada instruction", "English gloss", "Verdict", "Corrected Kannada text"]:
        B.append("header row changed")
    rows, seen = [], []
    for k, (iid, kn, gloss, warn) in enumerate(expected_rows()):
        r = k + 2
        cid, ckn, cgl, ver, cor = (t.cell(row=r, column=c).value for c in range(1, 6))
        seen.append(cid)
        if cid != iid or ckn != kn or cgl != gloss:
            B.append(f"{iid}: the id, the Kannada instruction or the gloss was edited")
        v = (ver or "").strip() if isinstance(ver, str) else ver
        cor_s = cor.strip() if isinstance(cor, str) else ("" if cor is None else str(cor))
        if v is None or v == "":
            B.append(f"{iid}: Verdict is blank")
        elif v not in VERDICTS:
            B.append(f"{iid}: Verdict {v!r} is not one of {VERDICTS}")
        elif v == "Needs change" and not cor_s:
            B.append(f"{iid}: Needs change but no corrected Kannada text")
        elif v == "Correct" and cor_s:
            W.append(f"{iid}: Correct but a corrected text was typed; kept, marked unused")
        if cor_s and not re.search(r"[ಀ-೿]", cor_s):
            W.append(f"{iid}: the corrected text contains no Kannada script")
        if iid == "T3-2" and v == "Correct":
            W.append("T3-2 (XNLI, marked needs rewrite) was returned as Correct: the premise/hypothesis words were not changed")
        rows.append({"id": iid, "verdict": v, "corrected": cor_s or None, "corrected_used": bool(v == "Needs change" and cor_s)})
    if len(set(seen)) != len(seen):
        B.append("duplicate instruction ids")
    extra = [c.coordinate for row in t.iter_rows() for c in row if c.value not in (None, "") and (c.column > 5 or c.row > 4)]
    if extra:
        B.append(f"content outside the table: {extra[:10]}")
    rep["rows"] = rows
    rep["all_correct"] = all(r["verdict"] == "Correct" for r in rows)
    rep["ok"] = not B
    out = outdir or results_dir("phase2/x1")
    if not B:
        write_json(out / "t3_verification_returned.json", {"rows": rows, "all_correct": rep["all_correct"], "source": path.name},
                   {"note": "returned T3 verification; no template is changed by this script"})
        rep["written"] = "t3_verification_returned.json"
    return rep


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--folder", default=str(C.RETURNED))
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    outdir = Path(a.out) if a.out else None
    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)
    paths = [Path(f) for f in a.files] or C.returned_files("T3_", Path(a.folder))
    if not paths:
        print(f"no T3 workbook in {a.folder}")
        return 2
    ids = {p: C.file_id(p) for p in paths}
    cross = C.cross_checks(paths, ids, "T3")
    if len(paths) > 1:
        cross.append(f"{len(paths)} T3 files returned; expected one")
    reports = [import_one(p, outdir) for p in paths]
    out = outdir or results_dir("phase2/x1")
    C.write_md(out / "VALIDATION_T3.md", "T3 import validation", [{k: v for k, v in r.items() if k != "rows"} for r in reports], cross,
               ["", f"Orphan .xlsx files in the folder (no File id): {C.orphans(Path(a.folder))}"])
    for r in reports:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    for c in cross:
        print("BLOCKER (cross-file):", c)
    return 1 if (cross or any(not r.get("ok") for r in reports)) else 0


if __name__ == "__main__":
    sys.exit(main())
