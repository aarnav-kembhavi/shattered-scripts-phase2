"""Annotation workbooks, VERIFY version (protocol change of 2026-10-26, RESULTS.md: verification of the Gemini drafts,
fine / wrong + fix; B's 40 blind items typed from scratch; Rater C dropped). The rate-and-correct workbooks of
2026-10-25 are in git history only.

  python scripts/k_xlsx.py build            -> annotation/xlsx/annotator_A.xlsx (500 items + 3 example rows),
                                               annotator_B_part1.xlsx (40 blind items: Kannada and English only),
                                               annotator_B_part2.xlsx (B's other 60, A's layout + the examples)
  python scripts/k_xlsx.py leakcheck [xlsx] -> every part of the xlsx searched for any Gemini draft text (B part 1)
  python scripts/k_xlsx.py xmlcheck [xlsx]  -> every answer cell empty in the sheet XML; no hidden sheets, columns or
                                               rows, names, comments, or cells outside the layout

Layout and field names come from annotation/merge_xlsx.py, so the merge reads exactly what was built.
"""
from __future__ import annotations

import html
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Protection
from openpyxl.utils import column_index_from_string, get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO / "annotation"), str(REPO / "scripts")]
import merge_xlsx as M  # noqa: E402

OUT = REPO / "annotation" / "xlsx"
FONT = "Nirmala UI"
WIDTH = {"native": 42, "english": 36, "natural_draft": 40, "kanglish_draft": 40, "natural_ok": 12, "kanglish_ok": 12,
         "natural_fix": 40, "kanglish_fix": 40, "natural_own": 44, "kanglish_own": 44, "note": 32, "item_id": 9}
HEAD_FILL, ANSWER_FILL = PatternFill("solid", fgColor="E8EEF4"), PatternFill("solid", fgColor="FFF8E1")
EXAMPLE_FILL, ID_FILL = PatternFill("solid", fgColor="DDE7D4"), PatternFill("solid", fgColor="EEEEEE")
WRAP = Alignment(wrap_text=True, vertical="top")

AUTOCORRECT = ("Turn off AutoCorrect (File > Options > Proofing > AutoCorrect Options, untick the capitals options and "
               "\"Replace text as you type\") and phone autocorrect.")
README = {
    "A": ["For each draft pick \"fine\" if it is how people would type it on WhatsApp and keeps the meaning, otherwise "
          "\"wrong\" and type your fix. No AI or translation tools.", AUTOCORRECT,
          "Save as .xlsx, send to Aarnav weekly."],
    "B1": ["For each Kannada sentence, type it yourself in English letters the way you would on WhatsApp, word for word "
           "(Your natural), and as Kanglish (Your Kanglish). No AI or translation tools; do not look anything up.",
           AUTOCORRECT, "Save as .xlsx, send to Aarnav when all 40 are done."],
    "B2": ["For each draft pick \"fine\" if it is how people would type it on WhatsApp and keeps the meaning, otherwise "
           "\"wrong\" and type your fix. No AI or translation tools.", AUTOCORRECT,
           "Save as .xlsx, send to Aarnav when you finish."],
}


def font(**kw):
    return Font(name=FONT, size=11, **kw)


def protect(ws):
    ws.protection.sheet = True  # no password: prevents accidents only
    ws.protection.formatColumns = False  # allowed: resize columns and rows
    ws.protection.formatRows = False


def readme_sheet(wb, lines):
    ws = wb.active
    ws.title = M.README
    ws.column_dimensions["A"].width = 110
    for k, t in enumerate(lines, 1):
        c = ws.cell(k, 1, f"({k}) {t}")
        c.font, c.alignment = font(), WRAP
    protect(ws)


def items_sheet(wb, spec, rows, examples=()):
    """Header, then the locked example rows (shaded, ID "EXAMPLE n"), then the items. Only ok/text cells of item rows
    are unlocked; ok cells get a fine/wrong dropdown with a stop alert; text cells are Text format and empty."""
    ws = wb.create_sheet(M.ITEMS)
    for j, (f, h, kind) in enumerate(spec, 1):
        c = ws.cell(1, j, h)
        c.font, c.alignment, c.fill = font(bold=True), WRAP, HEAD_FILL
        ws.column_dimensions[get_column_letter(j)].width = WIDTH[f]
    r = 2
    for ex in examples:
        for j, (f, _, kind) in enumerate(spec, 1):
            c = ws.cell(r, j, ex.get(f))
            c.font, c.alignment, c.fill = font(italic=True), WRAP, EXAMPLE_FILL
        r += 1
    first = r
    for row in rows:
        for j, (f, _, kind) in enumerate(spec, 1):
            c = ws.cell(r, j, row.get(f) if kind in ("locked", "id") else None)
            c.font, c.alignment = font(), WRAP
            if kind == "id":
                c.font, c.fill = Font(name=FONT, size=8, color="808080"), ID_FILL
            if kind in ("ok", "text"):
                c.protection, c.fill = Protection(locked=False), ANSWER_FILL
                if kind == "text":
                    c.number_format = "@"
        r += 1
    last = r - 1
    for j, (f, _, kind) in enumerate(spec, 1):
        if kind == "ok" and rows:
            dv = DataValidation(type="list", formula1='"' + ",".join(M.OK_OPTS) + '"', allow_blank=True,
                                showErrorMessage=True, errorStyle="stop", errorTitle="Not an allowed value",
                                error="Please choose fine or wrong", showInputMessage=False)
            col = get_column_letter(j)
            dv.add(f"{col}{first}:{col}{last}")
            ws.add_data_validation(dv)
    ws.freeze_panes = "A2"  # header row only
    protect(ws)
    return ws


def set_props(wb, title):
    p = wb.properties
    p.title, p.creator, p.lastModifiedBy = title, "Shattered Scripts", "Shattered Scripts"
    p.subject = p.description = p.keywords = p.category = None


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    A, B1, B2 = M.expected("A"), M.expected("B", 1), M.expected("B", 2)
    assert (len(A), len(B1), len(B2)) == (500, 40, 60)
    assert {"flores-546", "indicsentiment-test-295"} <= {r["item_id"] for r in A}
    ex = M.example_rows()
    for name, key, spec, rows, examples, title in (
            ("annotator_A.xlsx", "A", M.VERIFY_SHEET, A, ex, "Kannada annotation: Annotator A"),
            # B part 1: built from ID, Kannada and English alone (no draft field is ever read)
            ("annotator_B_part1.xlsx", "B1", M.BLIND_SHEET,
             [{"item_id": r["item_id"], "native": r["native"], "english": r["english"]} for r in B1], (),
             "Kannada annotation: Annotator B, part 1"),
            ("annotator_B_part2.xlsx", "B2", M.VERIFY_SHEET, B2, ex, "Kannada annotation: Annotator B, part 2")):
        wb = Workbook()
        readme_sheet(wb, README[key])
        items_sheet(wb, spec, rows, examples)
        set_props(wb, title)
        wb.save(OUT / name)
    for old in ("worked_examples.xlsx", "template_rater_C.xlsx", "rater_C.xlsx"):  # superseded (git history)
        (OUT / old).unlink(missing_ok=True)
    print({"built": sorted(p.name for p in OUT.glob("*.xlsx")), "A": len(A), "B_part1": len(B1), "B_part2": len(B2)})


def leakcheck(path: Path = OUT / "annotator_B_part1.xlsx") -> dict:
    """Search every part of the xlsx (all XML, rels, docProps) for any Gemini draft text of any item: each line of
    each draft, plain and XML-escaped, and every run of 6 consecutive words; also the words gemini/draft."""
    import k_annotation as K
    drafts = [r["text"] for r in K.shown_drafts().values()]
    needles = set()
    for d in drafts:
        for line in (x.strip() for x in d.splitlines()):
            if not line:
                continue
            needles.update({line, html.escape(line, quote=True), html.escape(line, quote=False)})
            w = line.split()
            for k in range(max(1, len(w) - 5)):
                seg = " ".join(w[k:k + 6])
                if len(seg) >= 20:
                    needles.update({seg, html.escape(seg, quote=False)})
    # a draft run that is also in a shown source text (the English sentence, e.g. a name the Kanglish draft copied)
    # is reported separately: it is source text, not draft text
    sources = [r[f] for r in M.expected("A") for f in ("native", "english")]
    hits, from_source, parts = [], [], {}
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            text = z.read(name).decode("utf-8", errors="replace")
            parts[name] = len(text)
            found = [n for n in needles if n in text]
            src = [n for n in found if any(n in t or html.unescape(n) in t for t in sources)]
            if src:
                from_source.append({"part": name, "n": len(src), "texts": sorted(src)})
            found = [n for n in found if n not in src]
            if found:
                hits.append({"part": name, "n": len(found), "example": found[0][:60]})
            low = text.lower()
            for word in ("gemini", "draft"):
                if word in low:
                    hits.append({"part": name, "word": word})
    res = {"file": str(path.resolve().relative_to(REPO)), "parts_checked": len(parts), "drafts_searched": len(drafts),
           "needles": len(needles), "shortest_needle": min(map(len, needles)), "hits": hits,
           "matches_that_are_source_text": from_source}
    print(json.dumps(res, indent=1, ensure_ascii=False))
    return res


NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def xmlcheck(path: Path) -> dict:
    """From the unzipped XML (not through openpyxl): every answer cell (ok/text columns) of every item row has no
    value, formula or inline string; nothing is hidden; no cell outside the layout."""
    is_blind = "part1" in path.name
    spec = M.BLIND_SHEET if is_blind else M.VERIFY_SHEET
    first = M.FIRST_ROW["blind" if is_blind else "verify"]
    answer_cols = {j for j, (_, _, k) in enumerate(spec, 1) if k in ("ok", "text")}
    with zipfile.ZipFile(path) as z:
        wbx = ET.fromstring(z.read("xl/workbook.xml"))
        sheets = [(s.get("name"), s.get("state", "visible")) for s in wbx.iter(NS + "sheet")]
        names = [d.get("name") for d in wbx.iter(NS + "definedName")]
        rels = z.read("xl/_rels/workbook.xml.rels").decode()
        sheet_parts = sorted(n for n in z.namelist() if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n))
        filled, outside, hidden_cols, hidden_rows, n_cells = [], [], [], [], {}
        for sp in sheet_parts:
            root = ET.fromstring(z.read(sp))
            for col in root.iter(NS + "col"):
                if col.get("hidden") in ("1", "true"):
                    hidden_cols.append((sp, col.get("min"), col.get("max")))
            for row in root.iter(NS + "row"):
                if row.get("hidden") in ("1", "true"):
                    hidden_rows.append((sp, row.get("r")))
            items = sp == sheet_parts[-1]  # READ_ME is sheet1, items is sheet2
            n_cells[sp] = 0
            for c in root.iter(NS + "c"):
                m = re.match(r"([A-Z]+)(\d+)", c.get("r"))
                j, row = column_index_from_string(m.group(1)), int(m.group(2))
                has = any(c.find(NS + t) is not None for t in ("v", "is", "f"))
                n_cells[sp] += has
                if not has:
                    continue
                if items and j in answer_cols and row >= first:
                    filled.append(c.get("r"))
                if (items and j > len(spec)) or (not items and j > 1):
                    outside.append(f"{sp}:{c.get('r')}")
        comments = [n for n in z.namelist() if "comment" in n.lower() or "vml" in n.lower()]
    res = {"file": str(path.resolve().relative_to(REPO)), "sheets": sheets, "sheet_parts": sheet_parts,
           "cells_with_content": n_cells, "answer_columns": [get_column_letter(j) for j in sorted(answer_cols)],
           "first_item_row": first, "filled_answer_cells": filled, "cells_outside_layout": outside,
           "hidden_sheets": [s for s, st in sheets if st != "visible"], "hidden_columns": hidden_cols,
           "hidden_rows": hidden_rows, "defined_names": names, "comment_parts": comments,
           "external_links": "externalLink" in rels}
    res["clean"] = not (filled or outside or res["hidden_sheets"] or hidden_cols or hidden_rows or names or comments
                        or res["external_links"])
    print(json.dumps(res, indent=1, ensure_ascii=False))
    return res


if __name__ == "__main__":
    step = sys.argv[1]
    if step == "build":
        build()
    elif step == "leakcheck":
        r = leakcheck(Path(sys.argv[2]) if len(sys.argv) > 2 else OUT / "annotator_B_part1.xlsx")
        sys.exit(1 if r["hits"] else 0)
    elif step == "xmlcheck":
        paths = [Path(p) for p in sys.argv[2:]] or sorted(OUT.glob("annotator_*.xlsx"))
        sys.exit(0 if all([xmlcheck(p)["clean"] for p in paths]) else 1)
