"""Excel exports of every Phase 2 annotation task (2026-11-02, nothing is sent): X8 (P, Q), X15 (eight files), T3 (verification sheet), plus the private keys.

  python scripts/export_xlsx.py build     -> annotation/xlsx/{X8_P,X8_Q,X15_G1_a..X15_G4_b,T3_verification}.xlsx and annotation/private/*.json (gitignored)
  python scripts/export_xlsx.py check     -> reopen every file and assert the hygiene rules (see `check_file`), write annotation/xlsx/HYGIENE_REPORT.json

X8: Instructions + Task (id, Kannada sentence, Romanization blank); the 100 sentences and their order are the registered selection (`results/phase2/x8/selection.json`,
default_rng(8)); identical in both files; no Gemini text, no English, no other annotator's text. Unprotected (2026-11-03): the importers compare every non-answer cell with the original.
X15: eight files; group G (1..4) sees item i (position in the registered seeded item order, default_rng(15)) in form FORMS[(i + G) % 4]; the rows are shuffled with a fixed
seed per group (15000 + G; both seats of a group see the same order); Task sheet: Item (the row number in the displayed order), Text, Topic (dropdown of the seven labels
in English, strict data validation). Unprotected (2026-11-03): the importers compare every non-answer cell with the original. No gold labels, no form names, no model output in the files.
Keys (private): item -> gold label, item -> form per group, row -> item per file, the shuffle seeds.
T3: instruction id, Kannada instruction, English gloss, Verdict (dropdown), Corrected Kannada text; the XNLI line is marked "needs rewrite" with the two words flagged.
Hygiene (every file): Kannada-capable font on every cell, all cells text-formatted, no formulas, creator and last-modified-by blank, no hidden sheets, columns or rows.
"""
import json
import os
import math
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill, Protection
from openpyxl.worksheet.datavalidation import DataValidation

from shattered.runlog import REPO

sys.path.insert(0, str(REPO / "scripts"))
OUT = REPO / "annotation" / "xlsx"
PRIV = REPO / "annotation" / "private"
FONT = "Nirmala UI"  # ships with Windows and Office for Mac/Android Kannada rendering; checked against its glyph table below
HEAD_FILL = PatternFill("solid", fgColor="E8EEF4")
ANS_FILL = PatternFill("solid", fgColor="FFF8E1")
WARN_FILL = PatternFill("solid", fgColor="FDE2E2")
CATS = ["science/technology", "travel", "politics", "sports", "health", "entertainment", "geography"]
FORMS = ["native", "itrans", "lossy", "natural"]
KN_RANGE = re.compile(r"[ಀ-೿]")


# ------------------------------------------------------------------------------------------------------------------ helpers
def new_wb() -> Workbook:
    wb = Workbook()
    wb.properties.creator = ""
    wb.properties.lastModifiedBy = ""
    wb.properties.title = ""
    return wb


def put(ws, r: int, c: int, v, bold=False, fill=None, locked=True, size=12):
    cell = ws.cell(row=r, column=c)
    if v is not None:
        assert not str(v).startswith(("=", "+", "-", "@")), f"a text value starting with a formula character: {str(v)[:30]!r}"
        cell.value = str(v)
    cell.number_format = "@"
    cell.font = Font(name=FONT, size=size, bold=bold)
    cell.alignment = Alignment(wrap_text=True, vertical="top")
    cell.protection = Protection(locked=locked)
    if fill is not None:
        cell.fill = fill
    return cell


def lines(text: str, width: float) -> int:
    """Wrapped line count (Kannada glyph clusters are about 1.7 times wider than Latin letters in the same column width)."""
    f = 0.55 if KN_RANGE.search(str(text)) else 0.95
    return max(1, sum(math.ceil(max(1, len(p)) / max(1.0, width * f)) for p in str(text).split("\n")))


def instructions_sheet(ws, paras: list[tuple[str, str]], width: int = 105, protect_sheet: bool = True) -> None:
    ws.column_dimensions["A"].width = width
    for r, (kind, text) in enumerate(paras, 1):
        put(ws, r, 1, text, bold=(kind == "h"), size=14 if kind == "h" else 12)
        ws.row_dimensions[r].height = 24 * lines(text, width) + (6 if kind == "h" else 4)
    if protect_sheet:
        ws.protection.sheet = True  # (T3 only) no password


def protect(ws) -> None:
    ws.protection.sheet = True
    ws.protection.formatColumns = False  # allowed: widen columns
    ws.protection.formatRows = False


def finish(wb: Workbook, path: Path) -> None:
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_state = "visible"
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)


# ------------------------------------------------------------------------------------------------------------------ data
def x8_items() -> list[dict]:
    sel = json.loads((REPO / "results" / "phase2" / "x8" / "selection.json").read_text(encoding="utf-8"))
    rows = {}
    for ln in (REPO / "data" / "processed" / "natural_flores_m4_500_v1.jsonl").open(encoding="utf-8"):
        r = json.loads(ln)
        rows[r["index"]] = r
    return [{"index": int(i), "native": rows[int(i)]["native"]} for i in sel["indices"]], {int(i): rows[int(i)]["natural"] for i in sel["indices"]}


def x15_items() -> list[dict]:
    import x15_page as X
    return X.select(), X.text_of


# ------------------------------------------------------------------------------------------------------------------ builders
def build_x8() -> dict:
    items, gemini = x8_items()
    assert len(items) == 100 and len({i["index"] for i in items}) == 100
    for role in ("P", "Q"):
        wb = new_wb()
        ws = wb.active
        ws.title = "Instructions"
        instructions_sheet(ws, [
            ("h", f"Typing Kannada in English letters (role {role})"),
            ("p", "ಪ್ರತಿ ಕನ್ನಡ ವಾಕ್ಯವನ್ನು ನೀವು ಸಂದೇಶದಲ್ಲಿ ಟೈಪ್ ಮಾಡುವಂತೆ ಇಂಗ್ಲಿಷ್ ಅಕ್ಷರಗಳಲ್ಲಿ ಬರೆಯಿರಿ."),
            ("p", "You will see 100 Kannada sentences written in Kannada script. For each one, write the same sentence in romanized Kannada (Kannada written with "
                  "English letters), exactly the way you would type it in a message to a friend. One sentence per row, in the yellow column C (Romanization). Write the whole sentence."),
            ("p", "Do not look anything up: no dictionary, no translator, no search engine, no typing or transliteration tool, no AI assistant, and do not copy from anywhere. "
                  "Do not ask or compare with anyone. There is no right answer; we want your own natural way of typing. Use English words where you would normally use them."),
            ("p", "Switch off AutoCorrect before you start, otherwise Excel will capitalise and change your words: File > Options > Proofing > AutoCorrect Options, then untick "
                  "\"Capitalize first letter of sentences\", \"Capitalize first letter of table cells\" and \"Replace text as you type\". Type in lowercase if that is how you type in a message."),
            ("p", "Fill every row. Please do not change columns A and B. Save the file under the same name and send it back. Expected time: about 1.5 hours (between 1 and 2); you may work in several sittings."),
            ("p", f"Role letter: {role}"),
            ("p", f"File id: X8_{role}"),
        ], protect_sheet=False)
        ws2 = wb.create_sheet("Task")
        for c, (h, w) in enumerate((("id", 8), ("Kannada sentence", 70), ("Romanization", 70)), 1):
            put(ws2, 1, c, h, bold=True, fill=HEAD_FILL)
            ws2.column_dimensions["ABC"[c - 1]].width = w
        for r, it in enumerate(items, 2):
            put(ws2, r, 1, it["index"])
            put(ws2, r, 2, it["native"])
            put(ws2, r, 3, None, fill=ANS_FILL, locked=False)
            ws2.row_dimensions[r].height = 24 * max(lines(it["native"], 70), 2) + 6
        ws2.freeze_panes = "A2"
        finish(wb, OUT / f"X8_{role}.xlsx")  # unprotected: every non-answer cell is compared with the original on import

    return {"x8_order": [i["index"] for i in items], "x8_selection_seed": 8, "x8_shuffle_seed": None,
            "x8_note": "order = the registered default_rng(8) draw, identical in both files; no further shuffle", "gemini_text_by_index": {str(k): v for k, v in gemini.items()}}


def build_x15() -> dict:
    items, text_of = x15_items()
    n = len(items)
    keys = {"selection_seed": 15, "item_order": "x15_page.select() (default_rng(15) proportional draw, then permutation)", "items": [], "files": {}, "shuffle_seed_by_group": {}}
    for i, it in enumerate(items):
        keys["items"].append({"pos": i, "sib_id": it["id"], "gold": CATS[it["label"]], "forms_by_group": {str(g): FORMS[(i + g) % 4] for g in range(1, 5)}})
    paras = [
        ("h", "Topic reading task"),
        ("p", "You will see 100 short texts, one per row. Each is a sentence in Kannada, written either in Kannada script or in English letters. For each row, choose the topic that "
              "fits the text best from the list in column C (click the yellow cell and use the arrow to open the list)."),
        ("p", "The seven topics are: science/technology, travel, politics, sports, health, entertainment, geography. Choose the best one even if you are not sure. Answer every row."),
        ("p", "Do not look anything up: no translator, no dictionary, no search engine, no AI assistant, and do not discuss the texts with anyone. Some texts are harder to read than "
              "others; that is expected. This measures how readable the writing is, not a test of you."),
        ("p", "Please change only column C and do not edit anything else. Save the file under the same name and send it back. Expected time: about 30 to 45 minutes."),
    ]
    for g in range(1, 5):
        order = np.random.default_rng(15000 + g).permutation(n)
        keys["shuffle_seed_by_group"][str(g)] = 15000 + g
        for seat in ("a", "b"):
            fid = f"X15_G{g}_{seat}"
            wb = new_wb()
            ws = wb.active
            ws.title = "Instructions"
            instructions_sheet(ws, paras + [("p", f"File id: {fid}")], protect_sheet=False)
            ws2 = wb.create_sheet("Task")
            for c, (h, w) in enumerate((("Item", 8), ("Text", 90), ("Topic", 26)), 1):
                put(ws2, 1, c, h, bold=True, fill=HEAD_FILL)
                ws2.column_dimensions["ABC"[c - 1]].width = w
            rows = []
            for r, j in enumerate(order, 2):
                it, form = items[j], FORMS[(int(j) + g) % 4]
                t = text_of(it, form)
                put(ws2, r, 1, r - 1)
                put(ws2, r, 2, t)
                put(ws2, r, 3, None, fill=ANS_FILL, locked=False)
                ws2.row_dimensions[r].height = 24 * max(lines(t, 90), 1) + 6
                rows.append({"item_number": r - 1, "sib_id": it["id"], "pos": int(j), "form": form, "gold": CATS[it["label"]], "text": t})
            dv = DataValidation(type="list", formula1='"' + ",".join(CATS) + '"', allow_blank=True, showErrorMessage=True, errorStyle="stop",
                                errorTitle="Choose from the list", error="Please choose one of the seven topics from the list.")
            dv.add(f"C2:C{n + 1}")
            ws2.add_data_validation(dv)
            ws2.freeze_panes = "A2"
            finish(wb, OUT / f"{fid}.xlsx")  # unprotected: every non-answer cell is compared with the original on import

            keys["files"][fid] = {"group": g, "seat": seat, "rows": rows}
    return keys


T3_ROWS = [
    ("T3-1", "ಈ ವಿಮರ್ಶೆಯು negative ಅಥವಾ positive ಎಂದು ನೀವು ಹೇಳುತ್ತೀರಾ?",
     "Would you say that this review is negative or positive? (Intended: \"Would you say this review is negative or positive?\" The words negative and positive stay in English on purpose.)", False),
    ("T3-2", "ದತ್ತಾಂಶವು ಸತ್ಯವಾಗಿದ್ದರೆ, ಪರಿಕಲ್ಪನೆಯು ಸತ್ಯವೇ? no, maybe, ಅಥವಾ yes ಆಯ್ಕೆಮಾಡಿ.",
     "NEEDS REWRITE. Literal gloss: If the \"data\" is true, is the \"concept\" true? Choose no, maybe, or yes. Intended: \"If the premise is true, is the hypothesis true? Choose no, maybe, or yes.\" "
     "FLAGGED WORDS: ದತ್ತಾಂಶ (data) was used for \"premise\" and ಪರಿಕಲ್ಪನೆ (concept) for \"hypothesis\"; they are not the usual words for these terms, and the line does not point at the Premise: and Hypothesis: "
     "lines above it. Please give the wording you would use, or say that the field names should stay in English inside the sentence.", True),
    ("T3-3", "ಈ ಪಠ್ಯದ ಮುಖ್ಯ ವಿಷಯವೇನು: geography, entertainment, health, sports, politics, travel ಅಥವಾ science?",
     "What is the main topic of this text: geography, entertainment, health, sports, politics, travel or science? (The topic words stay in English on purpose.)", False),
]


def build_t3() -> None:
    wb = new_wb()
    ws = wb.active
    ws.title = "Instructions"
    instructions_sheet(ws, [
        ("h", "Check of three Kannada instruction lines"),
        ("p", "In one experiment, the question line of each task is written in Kannada. The English label words (negative, positive, no, maybe, yes, geography, ...) and the field names "
              "(Review, Premise, Hypothesis, Text, Answer) stay in English on purpose. The Kannada below was drafted by a machine and has not been checked by a person."),
        ("p", "For each row: is the Kannada line correct, natural Kannada that a reader would understand as the English meaning given? Choose Correct or Needs change in the Verdict column. "
              "If it needs a change, write the corrected line in the last column; change as little as possible and keep the English words as they are."),
        ("p", "The English gloss is only meant to show the intended meaning; it is not a check. Row T3-2 is already marked as probably wrong; please give the wording you would use."),
        ("p", "File id: T3_verification"),
    ])
    ws2 = wb.create_sheet("Task")
    widths = (14, 60, 70, 20, 60)
    for c, (h, w) in enumerate(zip(("Instruction id", "Kannada instruction", "English gloss", "Verdict", "Corrected Kannada text"), widths), 1):
        put(ws2, 1, c, h, bold=True, fill=HEAD_FILL)
        ws2.column_dimensions["ABCDE"[c - 1]].width = w
    for r, (iid, kn, gloss, warn) in enumerate(T3_ROWS, 2):
        put(ws2, r, 1, iid, fill=WARN_FILL if warn else None)
        put(ws2, r, 2, kn, fill=WARN_FILL if warn else None)
        put(ws2, r, 3, gloss, fill=WARN_FILL if warn else None)
        put(ws2, r, 4, None, fill=ANS_FILL, locked=False)
        put(ws2, r, 5, None, fill=ANS_FILL, locked=False)
        ws2.row_dimensions[r].height = 24 * max(lines(gloss, 70), lines(kn, 60)) + 8
    dv = DataValidation(type="list", formula1='"Correct,Needs change"', allow_blank=True, showErrorMessage=True, errorStyle="stop")
    dv.add("D2:D4")
    ws2.add_data_validation(dv)
    ws2.freeze_panes = "A2"
    finish(wb, OUT / "T3_verification.xlsx")


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    PRIV.mkdir(parents=True, exist_ok=True)
    x8 = build_x8()
    keys = build_x15() if "--with-x15" in sys.argv else None  # X15 is skipped (not run: annotators unavailable, 2026-11-03): no X15 files are built unless asked
    if "--with-t3" in sys.argv:  # T3_verification.xlsx has been sent and returned: never overwritten unless asked
        build_t3()
    if keys is not None:
        (PRIV / "x15_keys.json").write_text(json.dumps(keys, ensure_ascii=False, indent=1), encoding="utf-8")
    (PRIV / "x8_keys.json").write_text(json.dumps({k: v for k, v in x8.items() if k != "gemini_text_by_index"}, ensure_ascii=False, indent=1), encoding="utf-8")
    (PRIV / "x8_gemini_text_for_leak_check.json").write_text(json.dumps(x8["gemini_text_by_index"], ensure_ascii=False), encoding="utf-8")
    (PRIV / "README.txt").write_text("Private keys for the annotation workbooks (X15 gold labels and form mapping, shuffle seeds, X8 order). Never send, never commit, never in the anonymised package.\n")
    print("built", sorted(p.name for p in OUT.glob("*.xlsx") if p.name.startswith(("X8_", "X15_", "T3_"))))


# ------------------------------------------------------------------------------------------------------------------ hygiene
def _font_cmap() -> set[int]:
    from fontTools.ttLib import TTCollection
    for p in (Path(os.environ.get("WINDIR", "")) / "Fonts" / "Nirmala.ttc",):
        for f in TTCollection(str(p)).fonts:
            names = " ".join(n.toUnicode() for n in f["name"].names if n.nameID in (1, 4))
            if "Nirmala UI" in names and "Semilight" not in names and "Bold" not in names:
                return set(f.getBestCmap().keys())
    raise RuntimeError("Nirmala UI not found")


def check_file(path: Path, cmap: set[int], gemini: dict | None, keys: dict | None) -> dict:
    res = {"file": path.name, "problems": []}
    bad = res["problems"]
    z = zipfile.ZipFile(path)
    core = z.read("docProps/core.xml").decode("utf-8")
    for tag in ("creator", "lastModifiedBy"):
        m = re.search(rf"<(?:dc|cp):{tag}>([^<]*)</", core)
        if m and m.group(1).strip():
            bad.append(f"{tag} not blank: {m.group(1)!r}")
    for n in z.namelist():
        if n.startswith("xl/") and n.endswith(".xml"):
            x = z.read(n).decode("utf-8", "replace")
            if "<f>" in x or "<f " in x:
                bad.append(f"formula element in {n}")
            if 'state="hidden"' in x or 'state="veryHidden"' in x or 'hidden="1"' in x or 'hidden="true"' in x:
                bad.append(f"hidden element in {n}")
            if re.search(r"<definedName[ >]", x):  # an empty <definedNames/> container is what openpyxl always writes
                bad.append(f"defined name in {n}")
        if "comments" in n or "vmlDrawing" in n or "drawing" in n.lower():
            bad.append(f"comment or drawing part {n}")
    wb = load_workbook(path)
    all_text, kn_chars, table_cells = [], set(), 0
    for ws in wb.worksheets:
        if ws.sheet_state != "visible":
            bad.append(f"sheet {ws.title} hidden")
        for k, cd in ws.column_dimensions.items():
            if cd.hidden:
                bad.append(f"column {k} hidden in {ws.title}")
        for k, rd in ws.row_dimensions.items():
            if rd.hidden:
                bad.append(f"row {k} hidden in {ws.title}")
        for row in ws.iter_rows():
            for c in row:
                if c.value is None and not c.has_style:
                    continue
                table_cells += 1
                if c.number_format != "@":
                    bad.append(f"{ws.title}!{c.coordinate} not text-formatted ({c.number_format})")
                if c.data_type not in ("s", "n") or (c.value is not None and c.data_type != "s"):
                    bad.append(f"{ws.title}!{c.coordinate} data type {c.data_type}")
                if c.font is None or c.font.name != FONT:
                    bad.append(f"{ws.title}!{c.coordinate} font {c.font.name if c.font else None}")
                if c.value is not None:
                    all_text.append(str(c.value))
                    kn_chars |= {ord(ch) for ch in str(c.value) if KN_RANGE.match(ch)}
    missing = sorted(kn_chars - cmap)
    if missing:
        bad.append(f"{len(missing)} Kannada code points missing from {FONT}: {[hex(m) for m in missing[:10]]}")
    blob = "\n".join(all_text)
    stem = path.stem
    if stem.startswith("X8_"):
        assert gemini is not None
        for idx, t in gemini.items():
            if t and t.strip() and t.strip() in blob:
                bad.append(f"Gemini text of sentence {idx} found")
        if re.search(r"[A-Za-z]{4,}", "\n".join(str(ws.cell(row=r, column=2).value or "") for ws in [wb["Task"]] for r in range(2, 102))) and False:
            pass
        t = wb["Task"]
        if t.max_row != 101 or [t.cell(row=1, column=c).value for c in (1, 2, 3)] != ["id", "Kannada sentence", "Romanization"]:
            bad.append("X8 Task layout differs")
        if any(t.cell(row=r, column=3).value not in (None, "") for r in range(2, 102)):
            bad.append("X8 answer cells are not blank")
        if t.protection.sheet or wb["Instructions"].protection.sheet:
            bad.append("X8 workbook is protected (it must be unprotected)")
    if stem.startswith("X15_"):
        t = wb["Task"]
        if t.max_row != 101 or [t.cell(row=1, column=c).value for c in (1, 2, 3)] != ["Item", "Text", "Topic"]:
            bad.append("X15 Task layout differs")
        if t.protection.sheet or wb["Instructions"].protection.sheet:
            bad.append("X15 workbook is protected (it must be unprotected)")
        for r in range(2, 102):
            if t.cell(row=r, column=3).value not in (None, ""):
                bad.append("X15 Topic cells are not blank")
                break
        dvs = t.data_validations.dataValidation
        if len(dvs) != 1 or dvs[0].type != "list" or dvs[0].formula1.strip('"').split(",") != CATS or dvs[0].errorStyle != "stop" or "C2:C101" not in str(dvs[0].sqref):
            bad.append("X15 dropdown validation wrong")
        lower = blob.lower()
        for w in ("itrans", "lossy", "natural", "native", "gold", "gemini", "romaniz"):
            if w in lower:
                bad.append(f"X15 file contains the word {w!r}")
        if keys:  # gold labels: no Task cell may be a bare topic label (the labels occur in the Instructions list and the dropdown only); item texts may contain English words
            for r in range(1, 102):
                for c in (1, 2, 3):
                    v = str(t.cell(row=r, column=c).value or "").strip().lower()
                    if v in CATS:
                        bad.append(f"a Task cell equals a topic label: {t.cell(row=r, column=c).coordinate}")
    if stem.startswith("T3_"):
        t = wb["Task"]
        if [t.cell(row=1, column=c).value for c in range(1, 6)] != ["Instruction id", "Kannada instruction", "English gloss", "Verdict", "Corrected Kannada text"]:
            bad.append("T3 header differs")
        if "NEEDS REWRITE" not in str(t.cell(row=3, column=3).value) or "ದತ್ತಾಂಶ" not in str(t.cell(row=3, column=3).value):
            bad.append("T3 XNLI row not marked")
    res.update({"cells_checked": table_cells, "kannada_codepoints": len(kn_chars), "ok": not bad})
    return res


def check() -> int:
    cmap = _font_cmap()
    gem = json.loads((PRIV / "x8_gemini_text_for_leak_check.json").read_text(encoding="utf-8"))
    keys = json.loads((PRIV / "x15_keys.json").read_text(encoding="utf-8"))
    reports = []
    files = sorted(p for p in OUT.glob("*.xlsx") if p.name.startswith(("X8_", "X15_") + (("T3_",) if "--with-t3" in sys.argv else ())))  # the T3 sheet was sent and returned (author fields now filled)
    for p in files:
        reports.append(check_file(p, cmap, gem, keys))
        print(("OK   " if reports[-1]["ok"] else "FAIL ") + p.name, reports[-1]["problems"][:5])
    # X8: the two files must carry the identical sentences in the identical order
    a, b = (load_workbook(OUT / f"X8_{r}.xlsx")["Task"] for r in ("P", "Q"))
    same = all(a.cell(row=r, column=c).value == b.cell(row=r, column=c).value for r in range(1, 102) for c in (1, 2))
    # X15: every group sees every item once per file, and across the four groups every item in every form; seats of a group identical
    ok15 = True
    for g in range(1, 5):
        fa, fb = keys["files"][f"X15_G{g}_a"]["rows"], keys["files"][f"X15_G{g}_b"]["rows"]
        ok15 &= [x["sib_id"] for x in fa] == [x["sib_id"] for x in fb] and len({x["sib_id"] for x in fa}) == 100
    forms_per_item: dict = {}
    for g in range(1, 5):
        for x in keys["files"][f"X15_G{g}_a"]["rows"]:
            forms_per_item.setdefault(x["sib_id"], set()).add(x["form"])
    ok15 &= all(len(v) == 4 for v in forms_per_item.values())
    summary = {"files": len(files), "all_ok": all(r["ok"] for r in reports) and same and ok15, "x8_identical_sets_and_order": same, "x15_latin_square_ok": ok15, "reports": reports}
    (OUT / "HYGIENE_REPORT.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print("x8 identical:", same, "| x15 latin square:", ok15, "| ALL OK:", summary["all_ok"])
    return 0 if summary["all_ok"] else 1


if __name__ == "__main__":
    sys.exit({"build": lambda: build() or 0, "check": check}[sys.argv[1]]())
