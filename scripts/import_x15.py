"""Import returned X15 workbooks (X15_G1_a.xlsx ... X15_G4_b.xlsx) into the registered X15 format and validate them.

Checks per file: sheet and header layout, the file id in the Instructions sheet, 100 rows, the Item and Text columns equal to what was sent (read from the private key
annotation/private/x15_keys.json; a mismatch means a locked cell was edited or rows were moved), duplicate item numbers, missing or blank Topic cells, Topic values not in
the list of seven labels (free text, a different spelling, a number), extra content outside the table. Blockers stop the write unless --partial is given.
Writes results/phase2/x15/x15_g<G>_seat<S>.csv with the columns of the HTML page export (item_id, form, choice, ms, group, seat): item_id = the SIB-200 id, form from the private
key (so no form name was ever in the file the annotator saw), ms empty (not measured in a workbook), group = G (1..4; G4 is the registered g = 0, the Latin-square rule
(i + G) mod 4 is the same), seat = A or B. Plus results/phase2/x15/import_report_g<G>_<seat>.json. Usage: python scripts/import_x15.py returned/X15_G1_a.xlsx ... [--partial]
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

from openpyxl import load_workbook

from shattered.runlog import REPO, results_dir, write_json

CATS = ["science/technology", "travel", "politics", "sports", "health", "entertainment", "geography"]
KEYS = REPO / "annotation" / "private" / "x15_keys.json"


def import_one(path: Path, keys: dict, partial: bool) -> dict:
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
        B.append(f"{len(edited)} rows whose Item or Text differ from what was sent (locked cells edited or rows moved): {edited[:10]}")
    if blank:
        B.append(f"{len(blank)} missing or blank Topic cells: rows {blank[:15]}")
    if bad_label:
        B.append(f"{len(bad_label)} Topic values not in the list of seven: {bad_label[:10]}")
    rep["n_answers"] = len(out)
    if out:
        c = {lab: sum(x["choice"] == lab for x in out) for lab in CATS}
        rep["choice_counts"] = c
        if max(c.values()) > 0.6 * len(out):
            rep["warnings"].append("more than 60% of the answers are one label (straight-lining?)")
    if not B or partial:
        d = results_dir("phase2/x15")
        p = d / f"x15_g{g}_seat{seat}.csv"
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["item_id", "form", "choice", "ms", "group", "seat"])
            w.writeheader()
            w.writerows(out)
        rep["written"] = str(p.relative_to(REPO))
    rep["ok"] = not B
    write_json(results_dir("phase2/x15") / f"import_report_g{g}_{seat.lower()}.json", rep, {"source": path.name})
    return rep


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--partial", action="store_true")
    a = ap.parse_args()
    keys = json.loads(KEYS.read_text(encoding="utf-8"))
    bad = 0
    for f in a.files:
        r = import_one(Path(f), keys, a.partial)
        print(json.dumps(r, ensure_ascii=False, indent=1))
        bad += 0 if r.get("ok") else 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
