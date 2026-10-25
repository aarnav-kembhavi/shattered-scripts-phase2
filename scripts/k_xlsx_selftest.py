"""End-to-end test of the Excel annotation round trip on DUMMY answers (2026-10-25). Nothing is written under
annotation/results/ or data/: every file goes to the directory given (default: a new temp directory).

For each workbook in annotation/xlsx/: fill a copy with random valid answers (seed 0) plus planted AutoCorrect
artefacts, merge it with annotation/merge_xlsx.py, and check the output against the page CSV format and against the
answers that were filled in. Also: B part 1 + part 2 merge into one CSV; Rater C's workbook is built from that CSV
(registered pairs) and merged back; error cases (partly answered row, invalid value, changed ID, edited locked cell)
must be refused; one filled workbook is opened and saved by Excel itself (COM) and must merge to the same rows.

Usage: python scripts/k_xlsx_selftest.py [OUTDIR]
"""
from __future__ import annotations

import csv
import json
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from openpyxl import load_workbook

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO / "annotation"), str(REPO / "scripts")]
import merge_xlsx as M  # noqa: E402

X = REPO / "annotation" / "xlsx"
PY = sys.executable
RNG = random.Random(0)
PLANT = {"R1": "Nanna hesaru", "R2": "THe", "R3": "don’t"}


def merge(*args):
    p = subprocess.run([PY, str(REPO / "annotation/merge_xlsx.py"), *map(str, args)], capture_output=True, text=True,
                       encoding="utf-8", env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8",
                                              "PYTHONPATH": str(REPO / "src")})
    return p.returncode, p.stdout + p.stderr


def col(spec, field):
    return [f for f, _, _ in spec].index(field) + 1


def fill_drafts(path, n_partial=0, plant=True):
    """Ratings for every row; about a third of the corrections edited; planted artefacts in the first rows."""
    wb = load_workbook(path)
    wb[M.README][M.NAME_CELL] = "Dummy Tester"
    ws = wb[M.ITEMS]
    truth = {}
    for r in range(2, ws.max_row + 1):
        i = ws.cell(r, 1).value
        rec = {}
        for k in ("natural", "kanglish"):
            nat, mea = RNG.choice(M.NAT_OPTS), RNG.choice(M.MEAN_OPTS)
            ws.cell(r, col(M.DRAFT_SHEET, f"{k}_naturalness"), int(nat))
            ws.cell(r, col(M.DRAFT_SHEET, f"{k}_meaning"), mea)
            c = ws.cell(r, col(M.DRAFT_SHEET, f"{k}_corrected"))
            if RNG.random() < 0.33:
                c.value = c.value.lower().replace(" mattu ", " matte ")
            rec.update({f"{k}_naturalness": nat, f"{k}_meaning": "1" if mea == "yes" else "0",
                        f"{k}_corrected": c.value.strip()})
        truth[i] = rec
    if plant:
        for (rule, text), r in zip(PLANT.items(), (2, 3, 4)):
            c = ws.cell(r, col(M.DRAFT_SHEET, "kanglish_corrected"))
            c.value = (text + " " + c.value.lower()) if rule == "R1" else (c.value.lower() + " " + text)
            truth[ws.cell(r, 1).value]["kanglish_corrected"] = c.value.strip()
    if M.EXAMPLES in wb.sheetnames:
        we = wb[M.EXAMPLES]
        for r in range(2, we.max_row + 1):
            we.cell(r, len(M.EXAMPLES_SHEET) + 1, "OK" if r != 3 else "needs correction")
            if r == 3:
                we.cell(r, len(M.EXAMPLES_SHEET) + 2, "dummy comment: spell it chaligaladalli")
    wb.save(path)
    return truth


def fill_blind(path):
    wb = load_workbook(path)
    wb[M.README][M.NAME_CELL] = "Dummy Tester"
    ws, truth = wb[M.ITEMS], {}
    for r in range(2, ws.max_row + 1):
        i = ws.cell(r, 1).value
        nat, kan = f"dummy natural {r} idu ondu vakya", f"dummy kanglish {r} idu one sentence"
        ws.cell(r, col(M.BLIND_SHEET, "natural_corrected"), nat)
        ws.cell(r, col(M.BLIND_SHEET, "kanglish_corrected"), kan)
        truth[i] = {"natural_corrected": nat, "kanglish_corrected": kan}
    wb.save(path)
    return truth


def read_out(path):
    raw = path.read_bytes()
    assert raw.startswith(b"\xef\xbb\xbf"), "no BOM"
    rows = list(csv.DictReader(path.open(encoding="utf-8-sig", newline="")))
    head = path.open(encoding="utf-8-sig").readline().strip().split(",")
    return head, rows


def check_rows(rows, truth, condition):
    bad = 0
    for x in rows:
        t = truth[x["item_id"]]
        bad += x["condition"] != condition or any(x[k] != v for k, v in t.items())
    return bad


def excel_roundtrip(src: Path, dst: Path) -> str:
    """Open and save the workbook with Excel itself (COM); returns 'ok' or the reason it was skipped."""
    ps = (f"$xl = New-Object -ComObject Excel.Application; $xl.DisplayAlerts = $false; "
          f"$wb = $xl.Workbooks.Open('{src}'); $ws = $wb.Worksheets.Item('items'); "
          f"$o = @{{protected = $ws.ProtectContents; valtype = $ws.Range('F2').Validation.Type; "
          f"errstyle = $ws.Range('F2').Validation.AlertStyle; fmt = $ws.Range('H2').NumberFormat; "
          f"idlocked = $ws.Range('A2').Locked; anslocked = $ws.Range('H2').Locked}}; "
          f"$wb.SaveAs('{dst}', 51); $wb.Close($false); $xl.Quit(); $o | ConvertTo-Json -Compress")
    p = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True)
    return (p.stdout.strip() or p.stderr.strip()[-300:])


def main(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    res = {}
    # --- A
    a = out / "A_filled.xlsx"
    shutil.copyfile(X / "annotator_A.xlsx", a)
    truth_a = fill_drafts(a)
    rc, log = merge("A", a, "--final", "--out", out / "annotator_A.csv")
    head, rows = read_out(out / "annotator_A.csv") if rc == 0 else ([], [])
    res["A"] = {"merge_exit": rc, "header_is_page_format": head == M.PAGE_COLS, "rows": len(rows),
                "rows_matching_filled_answers": len(rows) - check_rows(rows, truth_a, "draft"),
                "flags": {k: json.loads(log[:log.index("\n}") + 2])[k] for k in ("flag_rules", "flags_new_not_in_draft")}
                if rc == 0 else log[-600:],
                "planted_flags_found": {k: (out / "annotator_A_flags.csv").read_text(encoding="utf-8-sig").count(k)
                                        > 0 for k in PLANT} if rc == 0 else None,
                "examples_check": json.loads(log[:log.index("\n}") + 2]).get("worked_examples_check") if rc == 0
                else None}
    # --- A, saved by Excel itself
    xa = out / "A_filled_saved_by_excel.xlsx"
    res["A_excel_roundtrip"] = {"excel": excel_roundtrip(a.resolve(), xa.resolve())}
    if xa.exists():
        rc2, log2 = merge("A", xa, "--final", "--out", out / "annotator_A_excel.csv")
        _, rows2 = read_out(out / "annotator_A_excel.csv") if rc2 == 0 else ([], [])
        strip = lambda rs: [{k: v for k, v in r.items() if k != "saved_at"} for r in rs]
        res["A_excel_roundtrip"].update({"merge_exit": rc2, "same_rows_as_before_except_saved_at":
                                         strip(rows2) == strip(rows), "saved_at": rows2[0]["saved_at"] if rows2 else
                                         log2[-400:]})
    # --- B part 1 + part 2
    b1, b2 = out / "B1_filled.xlsx", out / "B2_filled.xlsx"
    shutil.copyfile(X / "annotator_B_part1.xlsx", b1)
    shutil.copyfile(X / "annotator_B_part2.xlsx", b2)
    tb1, tb2 = fill_blind(b1), fill_drafts(b2, plant=False)
    rc, log = merge("B", b1, "--final", "--out", out / "annotator_B_part1only.csv")
    _, rows1 = read_out(out / "annotator_B_part1only.csv") if rc == 0 else ([], [])
    res["B_part1_only"] = {"merge_exit": rc, "rows": len(rows1),
                           "rows_matching": len(rows1) - check_rows(rows1, tb1, "blind"),
                           "drafts_and_ratings_empty": all(not r[k] for r in rows1 for k in (
                               "natural_draft", "kanglish_draft", "natural_naturalness", "natural_meaning",
                               "kanglish_naturalness", "kanglish_meaning"))}
    rc, log = merge("B", b1, b2, "--final", "--out", out / "annotator_B.csv")
    head, rows = read_out(out / "annotator_B.csv") if rc == 0 else ([], [])
    res["B_both_parts"] = {"merge_exit": rc, "header_is_page_format": head == M.PAGE_COLS, "rows": len(rows),
                           "blind": sum(r["condition"] == "blind" for r in rows),
                           "rows_matching": len(rows) - check_rows([r for r in rows if r["condition"] == "blind"], tb1,
                                                                   "blind")
                           - check_rows([r for r in rows if r["condition"] == "draft"], tb2, "draft"),
                           "order_is_page_order": [r["item_id"] for r in rows] ==
                           [e["item_id"] for e in M.expected("A") if e["double"]]}
    # --- C from B's merged CSV (registered pairs), then merged back
    import k_xlsx
    c = out / "C_filled.xlsx"
    rc = k_xlsx.rater(str(out / "annotator_B.csv"), c)
    import k_annotation as K
    wb = load_workbook(c)
    wb[M.README][M.NAME_CELL] = "Dummy Rater"
    ws, truth_c = wb[M.ITEMS], []
    for r in range(2, ws.max_row + 1):
        v = [RNG.choice(M.NAT_OPTS) for _ in range(2)]
        ws.cell(r, col(M.RATER_SHEET, "v1_naturalness"), int(v[0]))
        ws.cell(r, col(M.RATER_SHEET, "v2_naturalness"), int(v[1]))
        truth_c.append(v)
    shown = [ws.cell(r, col(M.RATER_SHEET, f)).value for r in range(2, ws.max_row + 1) for f in ("v1", "v2")]
    wb.save(c)
    drafts = K.shown_drafts()
    gem = {drafts[(p["item_id"], p["kind"])]["text"] for p in json.load(open(out / "C_filled_key.json"))["pairs"]}
    rc, log = merge("C", c, "--final", "--key", out / "C_filled_key.json", "--out", out / "rater_C_k3.csv")
    head, rows = read_out(out / "rater_C_k3.csv") if rc == 0 else ([], [])
    res["C"] = {"merge_exit": rc, "header_is_rater_page_format": head == M.RATER_COLS, "rows": len(rows),
                "rows_matching": sum([r["v1_naturalness"], r["v2_naturalness"]] == t for r, t in zip(rows, truth_c)),
                "versions_shown": len(shown), "of_which_gemini_drafts_source_hidden": sum(s in gem for s in shown),
                "workbook_mentions_gemini_or_human": any(w in json.dumps([c_.value for row in ws.iter_rows()
                                                                          for c_ in row]).lower()
                                                         for w in ("gemini", "human", "\"ai"))}
    # --- refusals
    cases = {}
    for name, edit in {
        "partly answered row": lambda ws: setattr(ws.cell(2, col(M.DRAFT_SHEET, "kanglish_meaning")), "value", None),
        "invalid value": lambda ws: ws.cell(3, col(M.DRAFT_SHEET, "natural_naturalness"), 7),
        "changed item ID": lambda ws: ws.cell(4, 1, "flores-999999"),
        "edited locked draft": lambda ws: ws.cell(5, col(M.DRAFT_SHEET, "natural_draft"), "edited"),
    }.items():
        p = out / f"A_bad_{name.replace(' ', '_')}.xlsx"
        shutil.copyfile(a, p)
        wb = load_workbook(p)
        edit(wb[M.ITEMS])
        wb.save(p)
        bad_out = out / f"should_not_exist_{name.replace(' ', '_')}.csv"
        rc, log = merge("A", p, "--out", bad_out)
        cases[name] = {"refused": rc == 1 and not bad_out.exists(),
                       "message": json.loads(log[:log.index("\n}") + 2])["errors"][:1]}
    res["refusals"] = cases
    # --- partial (weekly) file: half the rows untouched
    p = out / "A_half.xlsx"
    shutil.copyfile(X / "annotator_A.xlsx", p)
    wb = load_workbook(p)
    wb[M.README][M.NAME_CELL] = "Dummy Tester"
    ws = wb[M.ITEMS]
    for r in range(2, 252):
        for k in ("natural", "kanglish"):
            ws.cell(r, col(M.DRAFT_SHEET, f"{k}_naturalness"), 4)
            ws.cell(r, col(M.DRAFT_SHEET, f"{k}_meaning"), "yes")
    wb.save(p)
    rc, log = merge("A", p, "--out", out / "annotator_A_half.csv")
    rcf, _ = merge("A", p, "--final", "--out", out / "should_not_exist2.csv")
    r = json.loads(log[:log.index("\n}") + 2])
    res["A_weekly_partial"] = {"merge_exit": rc, "answered": r["answered"], "not_yet": r["not_yet_answered"],
                               "refused_with_final": rcf == 1}
    print(json.dumps(res, indent=1, ensure_ascii=False))
    return res


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp(prefix="xlsx_selftest_")))
