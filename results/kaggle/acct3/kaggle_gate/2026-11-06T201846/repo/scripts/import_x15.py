"""Import returned X15 workbooks (X15_G1_a.xlsx ... X15_G4_b.xlsx) into the registered X15 format and validate them.

One command: `python scripts/import_x15.py` reads every X15 workbook in annotation/returned/ (identified by the `File id` line of its Instructions sheet; or pass paths) and writes
results/phase2/x15/VALIDATION.md. Options: --partial, --folder DIR, --out DIR (tests).

Per file: sheet and header layout, the file id, 100 rows, the Item and Text columns equal to what was sent (read from the private key annotation/private/x15_keys.json; a mismatch means
a cell was edited or rows were moved), duplicate item numbers, missing or blank Topic cells, Topic values not in the list of seven labels (free text, another spelling, a number),
content outside the table. Across files (scripts/import_common.py): no file id twice, no person (author-field hash) behind two files, no byte-identical files, no file matching a private
key (a file whose answers equal the gold labels on every row counts as the key). Blockers stop the write unless --partial is given.
Writes results/phase2/x15/x15_g<G>_seat<S>.csv with the columns of the HTML page export (item_id, form, choice, ms, group, seat): item_id = the SIB-200 id, form from the private key
(so no form name was ever in the file the annotator saw), ms empty (not measured in a workbook), group = G (1..4; G4 is the registered g = 0, the Latin-square rule (i + G) mod 4 is the
same), seat = A or B; plus results/phase2/x15/import_report_g<G>_<seat>.json.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

from openpyxl import load_workbook

sys.path.insert(0, str(Path(__file__).resolve().parent))
import import_common as C  # noqa: E402

from shattered.runlog import REPO, results_dir, write_json  # noqa: E402

CATS = ["science/technology", "travel", "politics", "sports", "health", "entertainment", "geography"]
KEYS = REPO / "annotation" / "private" / "x15_keys.json"


def import_one(path: Path, keys: dict, partial: bool, outdir: Path | None = None, write: bool = True) -> dict:
    rep = {"file": path.name, "blockers": [], "warnings": []}
    B = rep["blockers"]
    wb = load_workbook(path)
    if wb.sheetnames != ["Instructions", "Task"]:
        B.append(f"sheets are {wb.sheetnames}")
        return rep
    ins = "\n".join(str(r[0].value) for r in wb["Instructions"].iter_rows() if r[0].value)
    m = re.search(r"File id: (X15_G([1-4])_([ab]))\b", ins)
    if not m or m.group(1) not in keys["files"]:
        B.append("file id missing or unknown")
        return rep
    fid, g, seat = m.group(1), int(m.group(2)), m.group(3).upper()
    rep.update({"file_id": fid, "group": g, "seat": seat})
    rows = keys["files"][fid]["rows"]
    d = C.diff_non_answer(path, fid)
    if d:
        B.append(f"{len(d)} cells outside the Topic column differ from the original: {d[:10]}")
    t = wb["Task"]
    if [t.cell(row=1, column=c).value for c in (1, 2, 3)] != ["Item", "Text", "Topic"]:
        B.append("header row changed")
    extra = [c.coordinate for row in t.iter_rows() for c in row if c.value not in (None, "") and (c.column > 3 or c.row > len(rows) + 1)]
    if extra:
        B.append(f"content outside the table: {extra[:10]}")
    items = [t.cell(row=r, column=1).value for r in range(2, len(rows) + 2)]
    dup = sorted({str(i) for i in items if items.count(i) > 1})
    if dup:
        B.append(f"duplicate item numbers: {dup[:10]}")
    out, blank, bad_label, edited = [], [], [], []
    for k, row in enumerate(rows):
        r = k + 2
        num, text, topic = t.cell(row=r, column=1).value, t.cell(row=r, column=2).value, t.cell(row=r, column=3).value
        if str(num).strip() != str(row["item_number"]) or text != row["text"]:
            edited.append(row["item_number"])
            continue
        if topic is None or (isinstance(topic, str) and not topic.strip()):
            blank.append(row["item_number"])
            continue
        if not isinstance(topic, str) or topic not in CATS:
            bad_label.append((row["item_number"], str(topic)[:40]))
            continue
        out.append({"item_id": row["sib_id"], "form": row["form"], "choice": topic, "ms": "", "group": g, "seat": seat})
    if edited:
        B.append(f"{len(edited)} rows whose Item or Text differ from what was sent (cells edited or rows moved): {edited[:10]}")
    if blank:
        B.append(f"{len(blank)} missing or blank Topic cells: rows {blank[:15]}")
    if bad_label:
        B.append(f"{len(bad_label)} Topic values not in the list of seven: {bad_label[:10]}")
    rep["n_answers"] = len(out)
    if len(out) == len(rows):  # a returned file that equals the key
        gold = {r["sib_id"]: r["gold"] for r in rows}
        agree = sum(gold[o["item_id"]] == o["choice"] for o in out) / len(out)
        rep["agreement_with_private_key"] = agree
        if agree == 1.0:
            B.append("every answer equals the private gold label: this file matches the private key")
        elif agree >= 0.97:
            rep["warnings"].append(f"{agree:.0%} of the answers equal the gold labels (unusually high)")
    if out:
        c = {lab: sum(x["choice"] == lab for x in out) for lab in CATS}
        rep["choice_counts"] = c
        if max(c.values()) > 0.6 * len(out):
            rep["warnings"].append("more than 60% of the answers are one label (straight-lining?)")
    d = outdir or results_dir("phase2/x15")
    if (not B or partial) and write:
        p = d / f"x15_g{g}_seat{seat}.csv"
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["item_id", "form", "choice", "ms", "group", "seat"])
            w.writeheader()
            w.writerows(out)
        rep["written"] = p.name
    rep["ok"] = not B
    if write:
        write_json(d / f"import_report_g{g}_{seat.lower()}.json", rep, {"source": path.name})
    return rep


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--partial", action="store_true")
    ap.add_argument("--folder", default=str(C.RETURNED))
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    outdir = Path(a.out) if a.out else None
    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)
    keys = json.loads(KEYS.read_text(encoding="utf-8"))
    paths = [Path(f) for f in a.files] or C.returned_files("X15_", Path(a.folder))
    if not paths:
        print(f"no X15 workbook in {a.folder}")
        return 2
    ids = {p: C.file_id(p) for p in paths}
    cross = C.cross_checks(paths, ids, "X15") + [x for x in C.person_overlap_across_kinds(Path(a.folder)) if not x.startswith("WARNING")]
    reports = [import_one(p, keys, a.partial, outdir, write=False) for p in paths]  # first pass: nothing is written until the cross-file checks are done
    if not cross:
        reports = [import_one(p, keys, a.partial, outdir, write=True) for p in paths]
    else:
        print("cross-file blockers: no result file is written")
    missing = sorted(set(keys["files"]) - {r.get("file_id") for r in reports})
    out = outdir or results_dir("phase2/x15")
    C.write_md(out / "VALIDATION.md", "X15 import validation", reports, cross,
               ["", f"Files still missing (of eight): {missing}", f"Orphan .xlsx files in the folder (no File id): {C.orphans(Path(a.folder))}"])
    n_ok = sum(1 for r in reports if r.get("ok"))
    if cross or n_ok < 8:
        (out / "DEVIATION_NEEDED.md").write_text(f"{n_ok} of 8 valid X15 files. If fewer than eight come back, log the number in RESULTS.md as a deviation BEFORE analysing anything: a line containing exactly `X15 DEVIATION: {n_ok} of 8 files`. scripts/analyze_x15.py refuses to run until that line exists.\n", encoding="utf-8")
    elif (out / "DEVIATION_NEEDED.md").exists():
        (out / "DEVIATION_NEEDED.md").unlink()
    for r in reports:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    for c in cross:
        print("BLOCKER (cross-file):", c)
    print("still missing:", missing, "| valid files:", n_ok, "of 8")
    return 1 if (cross or any(not r.get("ok") for r in reports)) else 0


if __name__ == "__main__":
    sys.exit(main())
