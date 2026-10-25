"""End-to-end test of the VERIFY workbooks (protocol change of 2026-10-26) on DUMMY answers. Nothing is written under
annotation/results/ or data/: every file goes to the directory given (default: a new temp directory).

1. A: a copy filled with random fine/wrong (seed 0), fixes for "wrong", planted AutoCorrect artefacts and one fix
   repeated in two rows; merged; the CSV must equal the filled answers (fine -> draft, wrong -> fix).
2. A with planted invalid cells (wrong + empty fix, wrong + fix equal to the draft, fine + fix, fix with empty OK?,
   value not fine/wrong) and empty cells: each must be reported, left out, and the exit code 1.
3. Structural refusals: changed item ID, edited locked draft, edited example row; --final with empty cells.
4. B part 1 (blind) + part 2 (verify) merged into one CSV; one blind row with only one version is invalid.
5. Agreement (kappa fine/wrong, A vs B on the 60) and anchoring (blind 40) on the merged CSVs.
6. The filled A workbook opened and saved by Excel itself (COM): protection, dropdown and formats survive, and it
   merges to the same rows.

Usage: python scripts/k_xlsx_selftest.py [OUTDIR]
"""
from __future__ import annotations

import csv
import json
import os
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
                       encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONPATH": str(REPO / "src")})
    out = p.stdout
    rep = json.loads(out[:out.index("\n}") + 2]) if out.startswith("{") else {"raw": (out + p.stderr)[-800:]}
    return p.returncode, rep, out


def col(spec, field):
    return [f for f, _, _ in spec].index(field) + 1


def fill_verify(path, agree_with=None, p_fine=0.7, plant=True):
    """Every OK? cell filled; returns {item_id: {form: (verdict, text)}}. agree_with: copy those verdicts 80% of the
    time (for a non-trivial kappa)."""
    wb = load_workbook(path)
    ws = wb[M.ITEMS]
    truth, first = {}, M.FIRST_ROW["verify"]
    for r in range(first, ws.max_row + 1):
        i = ws.cell(r, col(M.VERIFY_SHEET, "item_id")).value
        truth[i] = {}
        for k in M.FORMS:
            draft = ws.cell(r, col(M.VERIFY_SHEET, f"{k}_draft")).value
            v = agree_with[i][k][0] if agree_with and i in agree_with and RNG.random() < 0.8 else \
                ("fine" if RNG.random() < p_fine else "wrong")
            ws.cell(r, col(M.VERIFY_SHEET, f"{k}_ok")).value = v
            fix = None
            if v == "wrong":
                fix = draft.rstrip(".") + " antha"
                ws.cell(r, col(M.VERIFY_SHEET, f"{k}_fix")).value = fix
            truth[i][k] = (v, draft if v == "fine" else fix)
    if plant:
        rows = list(range(first, first + 5))
        for (rule, text), r in zip(PLANT.items(), rows):
            ws.cell(r, col(M.VERIFY_SHEET, "natural_ok")).value = "wrong"
            ws.cell(r, col(M.VERIFY_SHEET, "natural_fix")).value = text + " " + "idu sari"
            truth[ws.cell(r, col(M.VERIFY_SHEET, "item_id")).value]["natural"] = ("wrong", text + " idu sari")
        for r in rows[3:5]:  # the same fix in two rows
            ws.cell(r, col(M.VERIFY_SHEET, "kanglish_ok")).value = "wrong"
            ws.cell(r, col(M.VERIFY_SHEET, "kanglish_fix")).value = "same fix text"
            truth[ws.cell(r, col(M.VERIFY_SHEET, "item_id")).value]["kanglish"] = ("wrong", "same fix text")
    wb.save(path)
    return truth


def fill_blind(path, one_missing=False):
    wb = load_workbook(path)
    ws = wb[M.ITEMS]
    truth = {}
    for r in range(M.FIRST_ROW["blind"], ws.max_row + 1):
        i = ws.cell(r, col(M.BLIND_SHEET, "item_id")).value
        t = {"natural": f"nanna swanta baraha {r} saaku", "kanglish": f"my own Kanglish {r} type madide"}
        ws.cell(r, col(M.BLIND_SHEET, "natural_own")).value = t["natural"]
        ws.cell(r, col(M.BLIND_SHEET, "kanglish_own")).value = t["kanglish"]
        truth[i] = t
    if one_missing:
        ws.cell(M.FIRST_ROW["blind"], col(M.BLIND_SHEET, "kanglish_own")).value = None
    wb.save(path)
    return truth


def read_out(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        r = csv.reader(f)
        head = next(r)
        return head, [dict(zip(head, x)) for x in r]


def mismatches(rows, truth):
    bad = 0
    for row in rows:
        t = truth[row["item_id"]]
        for k in M.FORMS:
            if (row[f"{k}_verdict"], row[f"{k}_text"]) != tuple(t[k]):
                bad += 1
    return bad


def edit(src, dst, fn):
    shutil.copyfile(src, dst)
    wb = load_workbook(dst)
    fn(wb[M.ITEMS])
    wb.save(dst)
    return dst


def excel_roundtrip(src: Path, dst: Path) -> str:
    """Open and save the workbook with Excel itself (COM); returns Excel's view of the sheet, or the error."""
    r = M.FIRST_ROW["verify"]
    ok, fix, idc = (f"{c}{r}" for c in ("D", "E", "J"))
    ps = (f"$xl = New-Object -ComObject Excel.Application; $xl.DisplayAlerts = $false; "
          f"$wb = $xl.Workbooks.Open('{src}'); $ws = $wb.Worksheets.Item('items'); $null = $ws.Activate(); "
          f"$o = @{{protected = $ws.ProtectContents; valtype = $ws.Range('{ok}').Validation.Type; "
          f"errstyle = $ws.Range('{ok}').Validation.AlertStyle; formula = $ws.Range('{ok}').Validation.Formula1; "
          f"fixfmt = $ws.Range('{fix}').NumberFormat; idlocked = $ws.Range('{idc}').Locked; "
          f"oklocked = $ws.Range('{ok}').Locked; examplelocked = $ws.Range('D2').Locked; "
          f"frozen_row = $xl.ActiveWindow.SplitRow; frozen = $xl.ActiveWindow.FreezePanes}}; "
          f"$wb.SaveAs('{dst}', 51); $wb.Close($false); $xl.Quit(); $o | ConvertTo-Json -Compress")
    p = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True)
    return p.stdout.strip() or p.stderr.strip()[-300:]


def main(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    res = {}
    # 1. A, valid
    a = out / "A_filled.xlsx"
    shutil.copyfile(X / "annotator_A.xlsx", a)
    truth_a = fill_verify(a)
    rc, rep, log = merge("A", a, "--final", "--out", out / "annotator_A.csv")
    head, rows = read_out(out / "annotator_A.csv")
    flags = (out / "annotator_A_flags.csv").read_text(encoding="utf-8-sig")
    res["1_A_valid"] = {"merge_exit": rc, "header": head == M.CSV_COLS, "rows": len(rows),
                        "cells_not_matching_filled_answers": mismatches(rows, truth_a),
                        "fine_share": rep["fine_share"], "empty_cells": rep["empty_cells"], "invalid": rep["invalid"],
                        "repeated_fixes": rep["repeated_fixes"], "flag_rules_not_in_draft": rep["autocorrect_flag_rules"],
                        "planted_flags_found": {k: (k in flags) for k in PLANT}}
    # 2. A, invalid and empty cells
    f = M.FIRST_ROW["verify"]
    C = lambda k: col(M.VERIFY_SHEET, k)  # noqa: E731

    def plant_invalid(ws):
        draft = ws.cell(f + 10, C("natural_draft")).value
        ws.cell(f + 10, C("natural_ok")).value, ws.cell(f + 10, C("natural_fix")).value = "wrong", None
        ws.cell(f + 11, C("natural_ok")).value, ws.cell(f + 11, C("natural_fix")).value = "wrong", \
            ws.cell(f + 11, C("natural_draft")).value
        ws.cell(f + 12, C("natural_ok")).value, ws.cell(f + 12, C("natural_fix")).value = "fine", "some fix"
        ws.cell(f + 13, C("natural_ok")).value, ws.cell(f + 13, C("natural_fix")).value = None, "fix but no OK"
        ws.cell(f + 14, C("natural_ok")).value = "maybe"  # bypasses the dropdown (as a paste can)
        for r in range(f + 20, f + 23):
            ws.cell(r, C("natural_ok")).value = ws.cell(r, C("natural_fix")).value = None
        assert draft
    bad = edit(a, out / "A_invalid.xlsx", plant_invalid)
    rc, rep, log = merge("A", bad, "--out", out / "A_invalid.csv")
    inv = [x for x in csv.DictReader(open(out / "A_invalid_invalid.csv", encoding="utf-8-sig"))]
    res["2_A_invalid_and_empty"] = {"merge_exit": rc, "invalid": rep["invalid"], "empty_cells": rep["empty_cells"],
                                    "problems": sorted(x["problem"] for x in inv),
                                    "rows_written": len(read_out(out / "A_invalid.csv")[1])}
    rc, rep, _ = merge("A", bad, "--final", "--out", out / "A_invalid_final.csv")
    res["2_A_invalid_and_empty"]["final_refused"] = rc == 1 and rep["written"] is None
    # 3. structural refusals
    cases = {
        "changed item ID": lambda ws: setattr(ws.cell(f + 3, C("item_id")), "value", "flores-999999"),
        "edited locked draft": lambda ws: setattr(ws.cell(f + 4, C("natural_draft")), "value", "changed"),
        "edited example row": lambda ws: setattr(ws.cell(2, C("natural_ok")), "value", "wrong"),
    }
    res["3_refusals"] = {}
    for name, fn in cases.items():
        p = edit(a, out / f"A_{name.replace(' ', '_')}.xlsx", fn)
        rc, rep, _ = merge("A", p, "--out", out / f"refused_{name.replace(' ', '_')}.csv")
        res["3_refusals"][name] = {"refused": rc == 1 and rep.get("written") is None,
                                   "message": rep.get("structural_errors", rep)}
    # 4. B part 1 + part 2
    b1, b2 = out / "B1_filled.xlsx", out / "B2_filled.xlsx"
    shutil.copyfile(X / "annotator_B_part1.xlsx", b1)
    shutil.copyfile(X / "annotator_B_part2.xlsx", b2)
    truth_b1 = fill_blind(b1)
    truth_b2 = fill_verify(b2, agree_with=truth_a, plant=False)
    rc, rep, _ = merge("B", b1, b2, "--final", "--out", out / "annotator_B.csv")
    head, rows = read_out(out / "annotator_B.csv")
    blind_rows = [r for r in rows if r["condition"] == "blind"]
    res["4_B"] = {"merge_exit": rc, "rows": len(rows), "blind": len(blind_rows),
                  "blind_text_matches": sum(r["natural_text"] == truth_b1[r["item_id"]]["natural"] and
                                            r["kanglish_text"] == truth_b1[r["item_id"]]["kanglish"]
                                            for r in blind_rows),
                  "blind_drafts_empty": all(not r["natural_draft"] and not r["kanglish_draft"] for r in blind_rows),
                  "part2_cells_not_matching": mismatches([r for r in rows if r["condition"] == "draft"], truth_b2),
                  "page_order": [r["item_id"] for r in rows] == [e["item_id"] for e in M.expected("A")
                                                                 if e["double"]]}
    b1x = out / "B1_one_missing.xlsx"
    shutil.copyfile(X / "annotator_B_part1.xlsx", b1x)
    fill_blind(b1x, one_missing=True)
    rc, rep, _ = merge("B", b1x, "--out", out / "B1_one_missing.csv")
    res["4_B"]["one_version_missing"] = {"merge_exit": rc, "invalid": rep["invalid"]}
    # 5. agreement and anchoring
    rc, agr, _ = merge("agree", out / "annotator_A.csv", out / "annotator_B.csv", "--out", out / "agreement.json")
    res["5_agreement"] = {k: {x: agr[k][x] for x in ("n", "kappa", "agree_share")} for k in M.FORMS}
    rc, anc, _ = merge("anchor", out / "annotator_A.csv", out / "annotator_B.csv", "--out", out / "anchoring.json")
    res["5_anchoring"] = {k: {"n_B": anc[k]["n_B"], "n_with_A": anc[k]["n_with_A"],
                              "vowel_doubling_ratio_gemini_to_B": anc[k]["gemini"]["vowel_doubling"]["ratio_other_to_B"],
                              "ci90": anc[k]["gemini"]["vowel_doubling"]["ci90"],
                              "chrf_gemini_vs_B": round(anc[k]["gemini"]["chrf_other_vs_B"]["mean"], 1),
                              "chrf_A_vs_B": round(anc[k]["A_verified"]["chrf_other_vs_B"]["mean"], 1)}
                          for k in M.FORMS}
    # 6. Excel round trip
    xa = out / "A_saved_by_excel.xlsx"
    res["6_excel_roundtrip"] = {"excel": excel_roundtrip(a.resolve(), xa.resolve())}
    if xa.exists():
        rc, rep, _ = merge("A", xa, "--final", "--out", out / "annotator_A_excel.csv")
        _, rx = read_out(out / "annotator_A_excel.csv")
        _, r0 = read_out(out / "annotator_A.csv")
        strip = lambda rs: [{k: v for k, v in r.items() if k != "saved_at"} for r in rs]  # noqa: E731
        res["6_excel_roundtrip"].update({"merge_exit": rc, "same_rows_apart_from_saved_at": strip(rx) == strip(r0)})
    print(json.dumps(res, indent=1, ensure_ascii=False))
    (out / "selftest.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return res


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp(prefix="kxlsx_selftest_")))
