"""Merge returned annotation workbooks (.xlsx) into the CSV format the HTML pages wrote (protocol change of
2026-10-25, RESULTS.md), so downstream code (scripts/k_annotation.py: agreement, rater pairs, K1-K3 scoring) is
unchanged.

Checks, per file: the item IDs equal the expected set exactly (no missing, extra or duplicate rows); the locked
source columns are unchanged; every answered row has every required cell; every value is one of the fixed options.
A row counts as answered as soon as any answer cell differs from its starting value; a partly answered row is an
error (the page would not have saved it). With --final every row must be answered.

AutoCorrect detection (reported, never fixed): in every romanized text the annotator typed or kept, flag
  R1 a sentence that starts with an uppercase letter,
  R2 a token with two leading capitals ("THe"),
  R3 an Excel AutoCorrect replacement (annotation/autocorrect_en_excel16.tsv, exported from Excel 16 on 2026-10-25):
     a non-ASCII character that the list produces (e.g. ’ … ©), the token "I", or a token equal to a replacement
     whose misspelling occurs in the item's draft (or in romanized Kannada at all: i, cafe, thge).
Each flag says whether the same pattern is already in the Gemini draft (then it is probably not AutoCorrect).

Usage:
  python annotation/merge_xlsx.py A annotator_A.xlsx [--final] [--out PATH]
  python annotation/merge_xlsx.py B annotator_B_part1.xlsx [annotator_B_part2.xlsx] [--final] [--out PATH]
  python annotation/merge_xlsx.py C rater_C.xlsx [--final] [--out PATH] [--key KEY.json]
Outputs (default annotation/results/): annotator_<A|B>.csv (page format), rater_C_k3.csv (rater page format), and
<name>_flags.csv / <name>_examples_check.csv / <name>_notes.csv where they apply. Exit code 1 on any error (nothing is
written then).
"""
from __future__ import annotations

import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO / "scripts"), str(REPO / "src")]

# ---------------------------------------------------------------- the sheet layout (shared with scripts/k_xlsx.py)
PAGE_COLS = ["item_id", "annotator", "source", "natural_draft", "natural_corrected", "natural_naturalness",
             "natural_meaning", "kanglish_draft", "kanglish_corrected", "kanglish_naturalness", "kanglish_meaning",
             "note", "saved_at", "condition"]  # annotation/template_v2.html, COLS
RATER_COLS = ["item_id", "kind", "rater", "v1_naturalness", "v2_naturalness", "saved_at"]  # template_rater_v1.html

NAT_OPTS, MEAN_OPTS = ["1", "2", "3", "4", "5"], ["yes", "no"]
CHECK_OPTS = ["OK", "needs correction"]
# (field, header, kind): kind = id | locked | rating | meaning | text | check
DRAFT_SHEET = [
    ("item_id", "Item ID", "id"), ("source", "Source", "locked"), ("native", "Kannada", "locked"),
    ("english", "English", "locked"),
    ("natural_draft", "1. Natural romanization: AI draft", "locked"),
    ("natural_naturalness", "Natural: naturalness of the draft (1 = nobody would type this, 5 = exactly how people "
                            "type)", "rating"),
    ("natural_meaning", "Natural: draft keeps the meaning (yes / no)", "meaning"),
    ("natural_corrected", "Natural: your corrected version (starts as the draft; leave it if it is fine)", "text"),
    ("kanglish_draft", "2. Kanglish: AI draft", "locked"),
    ("kanglish_naturalness", "Kanglish: naturalness of the draft (1-5)", "rating"),
    ("kanglish_meaning", "Kanglish: draft keeps the meaning (yes / no)", "meaning"),
    ("kanglish_corrected", "Kanglish: your corrected version (starts as the draft; leave it if it is fine)", "text"),
    ("note", "Note (optional)", "text")]
BLIND_SHEET = [
    ("item_id", "Item ID", "id"), ("native", "Kannada", "locked"),
    ("natural_corrected", "Natural romanization: your version (Kannada typed in English letters, word for word)",
     "text"),
    ("kanglish_corrected", "Kanglish: your version (as a young person in Bengaluru would write it on WhatsApp)", "text"),
    ("note", "Note (optional)", "text")]
RATER_SHEET = [
    ("item_id", "Item ID", "id"), ("kind_label", "Kind", "locked"), ("native", "Kannada", "locked"),
    ("v1", "Version 1", "locked"),
    ("v1_naturalness", "Version 1: naturalness (1 = nobody would type this, 5 = exactly how people type on a phone)",
     "rating"),
    ("v2", "Version 2", "locked"), ("v2_naturalness", "Version 2: naturalness (1-5)", "rating"),
    ("note", "Note (optional)", "text")]
EXAMPLES_SHEET = [
    ("example", "Example", "locked"), ("item_id", "Item ID", "locked"), ("native", "Kannada", "locked"),
    ("english", "English", "locked"), ("kind", "Kind", "locked"), ("draft", "AI draft", "locked"),
    ("ex_naturalness", "Example rating: naturalness", "locked"), ("ex_meaning", "Example rating: keeps the meaning",
                                                                   "locked"),
    ("ex_corrected", "Example: good corrected version", "locked"), ("why", "Why", "locked")]
EXAMPLES_CHECK = [("check", "Your check (OK / needs correction)", "check"),
                  ("check_comment", "If it needs correction: your correction or comment", "text")]
ITEMS, README, EXAMPLES = "items", "READ_ME", "worked_examples"
NAME_CELL = "B7"  # READ_ME: "Your name:" in A7, the name in B7 (unlocked)
KIND_LABEL = {"natural": "Natural romanization", "kanglish": "Kanglish"}


# ---------------------------------------------------------------- expected content

def expected(role: str, part: int = 1) -> list:
    """Rows a workbook must contain, in order (same order as the page's list())."""
    import k_annotation as K
    blind = set(json.load(open(K.BLIND))["ids"])
    drafts = K.shown_drafts()
    rows = []
    for it in K.items():
        d = {k: drafts[(it["id"], k)]["text"] for k in ("natural", "kanglish")}
        rows.append({"item_id": it["id"], "source": it["source"], "native": it["native"], "english": it["english"],
                     "natural_draft": d["natural"], "kanglish_draft": d["kanglish"], "double": it["double"],
                     "blind": it["id"] in blind})
    if role == "A":
        return rows
    if role == "B":
        return [r for r in rows if r["double"] and (r["blind"] if part == 1 else not r["blind"])]
    raise ValueError(role)


# ---------------------------------------------------------------- AutoCorrect detection

def autocorrect_list() -> list:
    lines = (REPO / "annotation/autocorrect_en_excel16.tsv").read_text(encoding="utf-8").splitlines()
    return [tuple(x.split("\t", 1)) for x in lines if x and not x.startswith("#")]


AC = None
RISKY_KEYS = {"i", "cafe", "thge"}  # AutoCorrect misspellings that occur as tokens in our romanized Kannada


def tokens(t: str) -> list:
    return re.findall(r"[^\W\d_]+(?:['’][^\W\d_]+)?", t)


def flags_for(text: str, draft: str) -> list:
    global AC
    if AC is None:
        AC = autocorrect_list()
    out = []
    t, d = text or "", draft or ""
    d_low = {w.lower() for w in tokens(d)}
    for m in re.finditer(r"(?:^|[.!?]\s+)([^\W\d_])", t):
        if m.group(1).isupper():
            out.append(("R1 sentence starts with a capital", m.group(1) + t[m.end(1):m.end(1) + 12]))
    for w in tokens(t):
        if re.fullmatch(r"[A-Z]{2}[a-z]+", w):
            out.append(("R2 two leading capitals", w))
    nonascii_targets = {ch for _, v in AC for ch in v if ord(ch) > 127}
    for ch in sorted({c for c in t if c in nonascii_targets}):
        out.append(("R3 AutoCorrect symbol", ch))
    tw = tokens(t)
    if "I" in tw:
        out.append(("R3 AutoCorrect i -> I", "I"))
    for k, v in AC:
        if " " in v or not re.fullmatch(r"[^\W\d_]+(?:['’][^\W\d_]+)?", v) or v == "I":
            continue
        if v in tw and k.lower() != v.lower() and (k.lower() in d_low or k.lower() in RISKY_KEYS) \
                and v.lower() not in d_low:
            out.append((f"R3 AutoCorrect {k} -> {v}", v))
    res = []
    for rule, what in out:
        res.append({"rule": rule, "match": what, "also_in_draft": bool(d) and what in d})
    return res


# ---------------------------------------------------------------- reading a workbook

class Problems(list):
    def add(self, where, msg):
        self.append(f"{where}: {msg}")


def cell_str(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v)


def read_sheet(wb, spec, name, P: Problems) -> list:
    if name not in wb.sheetnames:
        P.add(name, "sheet missing")
        return []
    ws = wb[name]
    head = [cell_str(c.value) for c in ws[1]][:len(spec)]
    if head != [h for _, h, _ in spec]:
        P.add(name, f"header changed: {head}")
        return []
    rows = []
    for r in ws.iter_rows(min_row=2, max_col=len(spec)):
        vals = {f: r[j].value for j, (f, _, _) in enumerate(spec)}
        if all(v is None or cell_str(v).strip() == "" for v in vals.values()):
            continue
        vals["_row"] = r[0].row
        rows.append(vals)
    return rows


def saved_at(wb, path: Path) -> str:
    t = wb.properties.modified or datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return t.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def check_ids(rows, exp_ids, where, P):
    got = [cell_str(r["item_id"]) for r in rows]
    dup = sorted({x for x in got if got.count(x) > 1})
    missing, extra = [x for x in exp_ids if x not in got], [x for x in got if x not in exp_ids]
    if dup or missing or extra:
        P.add(where, f"item IDs differ from the expected set: missing {missing[:5]}{'…' if len(missing) > 5 else ''}"
                     f" ({len(missing)}), extra {extra[:5]} ({len(extra)}), duplicated {dup[:5]} ({len(dup)})")
    elif got != exp_ids:
        P.add(where, "item rows are in a different order than issued (IDs are complete; order changed)")


def read_annotator(path: Path, part_spec, exp, final, P: Problems, F: list, label: str):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    name = cell_str(wb[README][NAME_CELL].value).strip() if README in wb.sheetnames else ""
    if not name:
        P.add(f"{label} {README}!{NAME_CELL}", "annotator name is empty")
    rows = read_sheet(wb, part_spec, ITEMS, P)
    exp_by = {e["item_id"]: e for e in exp}
    check_ids(rows, [e["item_id"] for e in exp], f"{label} {ITEMS}", P)
    when, recs = saved_at(wb, path), {}
    blind = part_spec is BLIND_SHEET
    n_todo = 0
    for r in rows:
        i = cell_str(r["item_id"])
        if i not in exp_by:
            continue
        e, where = exp_by[i], f"{label} {ITEMS}!row {r['_row']} ({i})"
        for f, _, kind in part_spec:
            if kind == "locked" and cell_str(r[f]) != cell_str(e[f]):
                P.add(where, f"locked column '{f}' was changed")
        txt = {f: cell_str(r[f]).strip() for f, _, k in part_spec if k == "text"}
        if blind:
            filled = [txt["natural_corrected"] != "", txt["kanglish_corrected"] != ""]
            if not any(filled) and not txt["note"]:
                n_todo += 1
                continue
            if not all(filled):
                P.add(where, "please write both versions (one is empty)")
                continue
            rec = {"natural_draft": "", "natural_naturalness": "", "natural_meaning": "",
                   "kanglish_draft": "", "kanglish_naturalness": "", "kanglish_meaning": "", "condition": "blind"}
        else:
            nat = {k: cell_str(r[f"{k}_naturalness"]).strip() for k in ("natural", "kanglish")}
            mea = {k: cell_str(r[f"{k}_meaning"]).strip() for k in ("natural", "kanglish")}
            changed = any(txt[f"{k}_corrected"] != e[f"{k}_draft"].strip() for k in ("natural", "kanglish"))
            if not any(nat.values()) and not any(mea.values()) and not changed and not txt["note"]:
                n_todo += 1
                continue
            bad = False
            for k in ("natural", "kanglish"):
                if nat[k] not in NAT_OPTS:
                    P.add(where, f"{k} naturalness {'missing' if not nat[k] else repr(nat[k]) + ' is not 1-5'}")
                    bad = True
                if mea[k] not in MEAN_OPTS:
                    P.add(where, f"{k} meaning {'missing' if not mea[k] else repr(mea[k]) + ' is not yes/no'}")
                    bad = True
            if bad:
                continue
            rec = {"condition": "draft"}
            for k in ("natural", "kanglish"):
                rec.update({f"{k}_draft": e[f"{k}_draft"], f"{k}_naturalness": nat[k],
                            f"{k}_meaning": "1" if mea[k] == "yes" else "0"})
        rec.update({"item_id": i, "annotator": name, "source": e["source"], "note": txt["note"], "saved_at": when,
                    "natural_corrected": txt["natural_corrected"], "kanglish_corrected": txt["kanglish_corrected"]})
        recs[i] = rec
        for k in ("natural", "kanglish"):
            for fl in flags_for(rec[f"{k}_corrected"], rec[f"{k}_draft"]):
                F.append({"file": path.name, "row": r["_row"], "item_id": i, "field": f"{k}_corrected", **fl,
                          "text": rec[f"{k}_corrected"]})
    if final and n_todo:
        P.add(f"{label} {ITEMS}", f"{n_todo} rows not answered (--final)")
    examples = []
    if EXAMPLES in wb.sheetnames and label.startswith("A"):
        for r in read_sheet(wb, EXAMPLES_SHEET + EXAMPLES_CHECK, EXAMPLES, P):
            c = cell_str(r["check"]).strip()
            if c and c not in CHECK_OPTS:
                P.add(f"{label} {EXAMPLES}!row {r['_row']}", f"check {c!r} is not one of {CHECK_OPTS}")
            if c == "needs correction" and not cell_str(r["check_comment"]).strip():
                P.add(f"{label} {EXAMPLES}!row {r['_row']}", "marked 'needs correction' but no correction given")
            examples.append({"example": r["example"], "item_id": r["item_id"], "kind": r["kind"], "check": c,
                             "comment": cell_str(r["check_comment"]).strip()})
    return recs, n_todo, examples


def read_rater(path: Path, key: dict, final, P: Problems):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    name = cell_str(wb[README][NAME_CELL].value).strip() if README in wb.sheetnames else ""
    if not name:
        P.add(f"{README}!{NAME_CELL}", "rater name is empty")
    rows = read_sheet(wb, RATER_SHEET, ITEMS, P)
    exp = [(p["item_id"], p["kind"]) for p in key["pairs"]]
    got = [(cell_str(r["item_id"]), {v: k for k, v in KIND_LABEL.items()}.get(cell_str(r["kind_label"]), "?"))
           for r in rows]
    if sorted(got) != sorted(exp) or len(set(got)) != len(got):
        P.add(ITEMS, "item/kind rows differ from the issued set")
    elif got != exp:
        P.add(ITEMS, "rows are in a different order than issued")
    when, recs, notes, n_todo = saved_at(wb, path), [], [], 0
    for r, (i, kind) in zip(rows, got):
        v = [cell_str(r[f"v{j}_naturalness"]).strip() for j in (1, 2)]
        if not any(v):
            n_todo += 1
            continue
        if any(x not in NAT_OPTS for x in v):
            P.add(f"{ITEMS}!row {r['_row']} ({i}, {kind})", f"ratings {v}: both must be 1-5")
            continue
        recs.append({"item_id": i, "kind": kind, "rater": name, "v1_naturalness": v[0], "v2_naturalness": v[1],
                     "saved_at": when})
        if cell_str(r["note"]).strip():
            notes.append({"item_id": i, "kind": kind, "note": cell_str(r["note"]).strip()})
    if final and n_todo:
        P.add(ITEMS, f"{n_todo} rows not rated (--final)")
    return recs, n_todo, notes


def write_csv(path: Path, cols, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:  # BOM, as the pages wrote
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main(argv) -> int:
    final = "--final" in argv
    out = key_path = None
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])
        argv = argv[:argv.index("--out")] + argv[argv.index("--out") + 2:]
    if "--key" in argv:  # rater key (default data/annotation/k3_rater_key_v1.json)
        key_path = Path(argv[argv.index("--key") + 1])
        argv = argv[:argv.index("--key")] + argv[argv.index("--key") + 2:]
    args = [a for a in argv if a != "--final"]
    role, files = args[0], [Path(a) for a in args[1:]]
    P, F = Problems(), []
    res = REPO / "annotation" / "results"
    report = {"role": role, "files": [f.name for f in files]}
    if role in ("A", "B"):
        recs, todo, examples = {}, 0, []
        parts = [(files[0], BLIND_SHEET if role == "B" else DRAFT_SHEET, expected(role, 1), f"{role}"
                  if role == "A" else "B part 1")]
        if role == "B" and len(files) > 1:
            parts.append((files[1], DRAFT_SHEET, expected("B", 2), "B part 2"))
        for path, spec, exp, label in parts:
            r, n, ex = read_annotator(path, spec, exp, final, P, F, label)
            recs.update(r)
            todo += n
            examples += ex
        names = {r["annotator"] for r in recs.values()}
        if len(names) > 1:
            P.add("READ_ME", f"different names in the files: {sorted(names)}")
        order = [e["item_id"] for e in expected("A")]
        rows = [recs[i] for i in order if i in recs]
        out = out or res / f"annotator_{role}.csv"
        report.update({"answered": len(rows), "not_yet_answered": todo, "autocorrect_flags": len(F),
                       "flag_rules": {k: sum(f["rule"].startswith(k) for f in F) for k in ("R1", "R2", "R3")},
                       "flags_new_not_in_draft": {k: sum(f["rule"].startswith(k) and not f["also_in_draft"] for f in F)
                                                  for k in ("R1", "R2", "R3")},
                       "flags_also_in_draft": sum(f["also_in_draft"] for f in F)})
        if examples:
            report["worked_examples_check"] = [f"{e['example']}/{e['kind']}: {e['check'] or '(blank)'}"
                                               for e in examples]
        if not P:
            write_csv(out, PAGE_COLS, rows)
            if F:
                write_csv(out.with_name(out.stem + "_flags.csv"), ["file", "row", "item_id", "field", "rule", "match",
                                                                   "also_in_draft", "text"], F)
            if examples:
                write_csv(out.with_name(out.stem + "_examples_check.csv"), ["example", "item_id", "kind", "check",
                                                                            "comment"], examples)
    elif role == "C":
        import k_annotation as K
        key = json.load(open(key_path or K.RATER_KEY, encoding="utf-8"))
        rows, todo, notes = read_rater(files[0], key, final, P)
        out = out or res / "rater_C_k3.csv"
        report.update({"rated": len(rows), "not_yet_rated": todo, "notes": len(notes)})
        if not P:
            write_csv(out, RATER_COLS, rows)
            if notes:
                write_csv(out.with_name(out.stem + "_notes.csv"), ["item_id", "kind", "note"], notes)
    else:
        print(__doc__)
        return 2
    report["errors"] = list(P)
    report["written"] = None if P else str(out)
    print(json.dumps(report, indent=1, ensure_ascii=False))
    new = [f for f in F if not f["also_in_draft"]]  # patterns the Gemini draft did not already have
    for f in new[:40]:
        print(f"  flag {f['file']} row {f['row']} {f['item_id']} {f['field']}: {f['rule']} [{f['match']}]")
    if len(new) > 40:
        print(f"  ... {len(new) - 40} more")
    if F:
        print(f"  ({len(F) - len(new)} further flags match the draft and are listed in the _flags.csv file only)")
    return 1 if P else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
