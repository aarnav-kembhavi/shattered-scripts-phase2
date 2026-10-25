"""Excel annotation workbooks (protocol change of 2026-10-25, RESULTS.md): same items, fields and options as the HTML
pages; the layout is defined in annotation/merge_xlsx.py, which reads the returned files back into the page CSV format.

  python scripts/k_xlsx.py build          # annotation/xlsx/: annotator_A.xlsx, annotator_B_part1.xlsx (40 blind items,
                                          # no Gemini draft anywhere), annotator_B_part2.xlsx (60 items with drafts),
                                          # worked_examples.xlsx (for B, later), template_rater_C.xlsx (empty)
  python scripts/k_xlsx.py leakcheck      # unzip annotator_B_part1.xlsx and search every part for draft text
  python scripts/k_xlsx.py rater B.csv    # Rater C workbook from B's returned blind items (registered K3 pairs, seed 3;
                                          # key in data/annotation/k3_rater_key_v1.json, never in the workbook)

Workbooks: READ_ME first (5 lines and the name cell), one row per item, item ID and source text locked, sheet
protection without a password (accidents only), every label a dropdown with a "stop" error alert, answer text cells
formatted as Text, header row frozen, wrapped text, Nirmala UI (renders Kannada).
"""
from __future__ import annotations

import html
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill, Protection
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO / "annotation"), str(REPO / "scripts")]
import merge_xlsx as M  # noqa: E402

OUT = REPO / "annotation" / "xlsx"
FONT = "Nirmala UI"
WIDTH = {"id": 24, "locked": 40, "rating": 16, "meaning": 14, "text": 44, "check": 18}
WIDE = {"native": 52, "english": 44, "source": 11, "kind_label": 20, "example": 9, "kind": 12, "ex_naturalness": 12,
        "ex_meaning": 12, "why": 50, "v1_naturalness": 18, "v2_naturalness": 18}
HEAD_FILL, ANSWER_FILL = PatternFill("solid", fgColor="E8EEF4"), PatternFill("solid", fgColor="FFF8E1")
WRAP = Alignment(wrap_text=True, vertical="top")

AUTOCORRECT = ("Turn off AutoCorrect before typing: File > Options > Proofing > AutoCorrect Options, and untick "
               "\"Correct TWo INitial CApitals\", \"Capitalize first letter of sentences\" and \"Replace text as you "
               "type\".")
PHONE = ("If you use the Excel app on a phone or tablet, also turn off autocorrect and automatic capitals in your "
         "keyboard settings.")
SAVE = ("Save with File > Save as an Excel Workbook (.xlsx), never as CSV. Type your name in the yellow cell below. "
        "Send the .xlsx file to Aarnav on WhatsApp")
RULES = ("Type the way you really type: there is no single correct spelling. No translation tools, AI tools or "
         "dictionaries; do not discuss the items with anyone. Questions: ask Aarnav.")
README = {
    "A": ["What to do: first check the 3 examples in the sheet \"worked_examples\" (OK, or write your correction), "
          "save, and send this file to Aarnav within a day. Then, in the sheet \"items\", for each AI draft: rate it "
          "first (naturalness 1-5, keeps the meaning yes/no), then correct it in \"your corrected version\" (leave it "
          "as it is if it is fine).", SAVE + " at the end of each week.", AUTOCORRECT, PHONE, RULES],
    "B1": ["What to do: for each Kannada sentence in the sheet \"items\", write it yourself in English letters, the "
           "way you type on a phone, word for word (natural romanization), and as Kanglish (how a young person in "
           "Bengaluru would write it on WhatsApp, keeping the full meaning). Do all 40. Nothing to rate.",
           SAVE + " as soon as all 40 are done.", AUTOCORRECT, PHONE, RULES],
    "B2": ["What to do: first read worked_examples.xlsx. Then, in the sheet \"items\", for each AI draft: rate it first "
           "(naturalness 1-5, keeps the meaning yes/no), then correct it in \"your corrected version\" (leave it as it "
           "is if it is fine).", SAVE + " when you finish.", AUTOCORRECT, PHONE, RULES],
    "C": ["What to do: in the sheet \"items\", rate how natural each version sounds, from 1 (nobody would type this) "
          "to 5 (exactly how people type on a phone). Rate each version on its own; both can get the same rating. Do "
          "not try to guess who or what wrote a version.", SAVE + " when you finish.", AUTOCORRECT, PHONE, RULES],
    "EX": ["These are 3 worked examples (not items you will annotate): the AI draft, how it was rated, and a good "
           "correction. Ratings are your own judgement; the examples show the idea, not the only right answer.",
           "Read them before you start rating the drafts in annotator_B_part2.xlsx.", "Nothing to fill in here.",
           "", ""],
}


def font(**kw):
    return Font(name=FONT, size=11, **kw)


def readme_sheet(wb, lines, name_cell=True):
    ws = wb.active
    ws.title = M.README
    ws.column_dimensions["A"].width = 16
    ws.column_dimensions["B"].width = 120
    for k, t in enumerate(lines, 1):
        ws.cell(k, 1, f"{k}." if t else "").font = font(bold=True)
        c = ws.cell(k, 2, t)
        c.font, c.alignment = font(), WRAP
    if name_cell:
        ws["A7"], ws[M.NAME_CELL] = "Your name:", None
        ws["A7"].font = font(bold=True)
        nc = ws[M.NAME_CELL]
        nc.font, nc.fill, nc.number_format = font(), ANSWER_FILL, "@"
        nc.protection = Protection(locked=False)
    protect(ws)
    return ws


def protect(ws):
    ws.protection.sheet = True  # no password: prevents accidents only
    ws.protection.formatColumns = False  # allowed: resize columns and rows
    ws.protection.formatRows = False


def data_sheet(wb, title, spec, rows):
    ws = wb.create_sheet(title)
    for j, (f, h, kind) in enumerate(spec, 1):
        c = ws.cell(1, j, h)
        c.font, c.alignment, c.fill = font(bold=True), WRAP, HEAD_FILL
        ws.column_dimensions[get_column_letter(j)].width = WIDE.get(f, WIDTH[kind])
    for i, r in enumerate(rows, 2):
        for j, (f, _, kind) in enumerate(spec, 1):
            c = ws.cell(i, j, r.get(f))
            c.font, c.alignment = font(), WRAP
            if kind in ("text", "check"):
                c.number_format = "@"
            if kind in ("rating", "meaning", "text", "check"):
                c.protection, c.fill = Protection(locked=False), ANSWER_FILL
    n = len(rows) + 1
    for j, (f, _, kind) in enumerate(spec, 1):
        opts = {"rating": M.NAT_OPTS, "meaning": M.MEAN_OPTS, "check": M.CHECK_OPTS}.get(kind)
        if opts and rows:
            dv = DataValidation(type="list", formula1='"' + ",".join(opts) + '"', allow_blank=True,
                                showErrorMessage=True, errorStyle="stop", errorTitle="Not an allowed value",
                                error="Please choose one of: " + ", ".join(opts), showInputMessage=False)
            col = get_column_letter(j)
            dv.add(f"{col}2:{col}{n}")
            ws.add_data_validation(dv)
    ws.freeze_panes = "A2"
    protect(ws)
    return ws


def example_rows():
    E = json.load(open(REPO / "annotation/examples_v1.json", encoding="utf-8"))["examples"]
    rows = []
    for n, e in enumerate(E, 1):
        for kind in ("natural", "kanglish"):
            k = e[kind]
            if k:
                rows.append({"example": n, "item_id": e["id"], "native": e["native"], "english": e["english"],
                             "kind": M.KIND_LABEL[kind], "draft": k["draft"], "ex_naturalness": k["naturalness"],
                             "ex_meaning": k["meaning"], "ex_corrected": k["corrected"], "why": k["why"]})
    return rows


def set_props(wb, title):
    p = wb.properties
    p.title, p.creator, p.lastModifiedBy = title, "Shattered Scripts", "Shattered Scripts"
    p.subject = p.description = p.keywords = p.category = None


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    A, B1, B2 = M.expected("A"), M.expected("B", 1), M.expected("B", 2)
    assert (len(A), len(B1), len(B2)) == (500, 40, 60)
    assert {"flores-546", "indicsentiment-test-295"} <= {r["item_id"] for r in A}
    prefill = lambda rs: [{**r, "natural_corrected": r["natural_draft"], "kanglish_corrected": r["kanglish_draft"]}
                          for r in rs]
    # Annotator A: all 500 items as on the page ("All 500 items"), plus the worked examples to check first
    wb = Workbook()
    readme_sheet(wb, README["A"])
    data_sheet(wb, M.ITEMS, M.DRAFT_SHEET, prefill(A))
    data_sheet(wb, M.EXAMPLES, M.EXAMPLES_SHEET + M.EXAMPLES_CHECK, example_rows())
    set_props(wb, "Kannada annotation: Annotator A")
    wb.save(OUT / "annotator_A.xlsx")
    # Annotator B part 1: the 40 blind items, native text only; built from IDs and native text alone
    wb = Workbook()
    readme_sheet(wb, README["B1"])
    data_sheet(wb, M.ITEMS, M.BLIND_SHEET, [{"item_id": r["item_id"], "native": r["native"]} for r in B1])
    set_props(wb, "Kannada annotation: Annotator B, part 1")
    wb.save(OUT / "annotator_B_part1.xlsx")
    # Annotator B part 2: the other 60 double items with drafts (released after B's 40 and A's check of the examples)
    wb = Workbook()
    readme_sheet(wb, README["B2"])
    data_sheet(wb, M.ITEMS, M.DRAFT_SHEET, prefill(B2))
    set_props(wb, "Kannada annotation: Annotator B, part 2")
    wb.save(OUT / "annotator_B_part2.xlsx")
    # worked examples as a standalone file (for B, released with part 2)
    wb = Workbook()
    readme_sheet(wb, README["EX"], name_cell=False)
    data_sheet(wb, M.EXAMPLES, M.EXAMPLES_SHEET, example_rows())
    set_props(wb, "Kannada annotation: worked examples")
    wb.save(OUT / "worked_examples.xlsx")
    # Rater C: empty template (filled by `rater` once B's blind items are in)
    wb = Workbook()
    readme_sheet(wb, README["C"])
    data_sheet(wb, M.ITEMS, M.RATER_SHEET, [])
    set_props(wb, "Kannada rating: Rater C")
    wb.save(OUT / "template_rater_C.xlsx")
    print({"built": sorted(p.name for p in OUT.glob("*.xlsx")), "A": len(A), "B_part1": len(B1), "B_part2": len(B2)})


def leakcheck(path: Path = OUT / "annotator_B_part1.xlsx") -> dict:
    """Search every part of the xlsx (all XML, rels, docProps, anything) for any Gemini draft text of any item:
    the full draft, plain and XML-escaped, and every run of 6 consecutive words from it."""
    import k_annotation as K
    drafts = [r["text"] for r in K.shown_drafts().values()]
    needles = set()
    for d in drafts:
        for v in (d, html.escape(d, quote=True), html.escape(d, quote=False)):
            needles.add(v)
        w = d.split()
        for k in range(max(1, len(w) - 5)):
            seg = " ".join(w[k:k + 6])
            if len(seg) >= 20:
                needles.update({seg, html.escape(seg, quote=False)})
    hits, parts = [], {}
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            text = z.read(name).decode("utf-8", errors="replace")
            parts[name] = len(text)
            low = text.lower()
            found = [n for n in needles if n in text]
            if found:
                hits.append({"part": name, "n": len(found), "example": found[0][:60]})
            if "gemini" in low or "draft" in low:
                hits.append({"part": name, "word": "gemini" if "gemini" in low else "draft"})
    native_ok = {}
    wb = load_workbook(path)
    native_ok["sheets"] = wb.sheetnames
    native_ok["hidden_sheets"] = [ws.title for ws in wb.worksheets if ws.sheet_state != "visible"]
    native_ok["defined_names"] = list(wb.defined_names.keys()) if hasattr(wb.defined_names, "keys") else \
        [d.name for d in wb.defined_names.definedName]
    ws = wb[M.ITEMS]
    native_ok["columns"] = [c.value for c in ws[1]]
    native_ok["hidden_columns"] = [k for k, d in ws.column_dimensions.items() if d.hidden]
    native_ok["comments"] = sum(1 for row in ws.iter_rows() for c in row if c.comment)
    res = {"file": str(path.resolve().relative_to(REPO)), "parts_checked": len(parts), "drafts_searched": len(drafts),
           "needles": len(needles), "hits": hits, **native_ok}
    print(json.dumps(res, indent=1, ensure_ascii=False))
    print("parts:", ", ".join(f"{k} ({v} chars)" for k, v in parts.items()))
    return res


def rater(b_csv: str, out: Path | None = None) -> int:
    import k_annotation as K
    pairs = K.rater_pairs(b_csv)
    if pairs is None:
        return 1
    rows, key = pairs
    out = out or OUT / "rater_C.xlsx"
    shutil.copyfile(OUT / "template_rater_C.xlsx", out)
    wb = load_workbook(out)
    del wb[M.ITEMS]
    data_sheet(wb, M.ITEMS, M.RATER_SHEET, [{**r, "kind_label": M.KIND_LABEL[r["kind"]]} for r in rows])
    wb.save(out)
    key_path = K.RATER_KEY if out == OUT / "rater_C.xlsx" else out.with_name(out.stem + "_key.json")
    key_path.write_text(json.dumps({"seed": K.RATER_SEED, "b_csv": str(b_csv), "pairs": key}, indent=1),
                        encoding="utf-8")
    print({"workbook": str(out), "key": str(key_path), "n_rows": len(rows),
           "human_first": sum(k["v1"] == "human" for k in key)})
    return 0


if __name__ == "__main__":
    step = sys.argv[1]
    if step == "build":
        build()
    elif step == "leakcheck":
        r = leakcheck(Path(sys.argv[2]) if len(sys.argv) > 2 else OUT / "annotator_B_part1.xlsx")
        sys.exit(1 if r["hits"] or r["hidden_sheets"] or r["hidden_columns"] or r["comments"] else 0)
    elif step == "rater":
        sys.exit(rater(sys.argv[2], Path(sys.argv[3]) if len(sys.argv) > 3 else None))
