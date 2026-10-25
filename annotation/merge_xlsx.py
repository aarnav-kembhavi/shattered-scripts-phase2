"""Merge returned VERIFY workbooks (.xlsx) into CSV (protocol change of 2026-10-26, RESULTS.md: annotation is
verification of the Gemini drafts, fine / wrong + fix; Annotator B's 40 blind items are typed from scratch).

Checks, per file: the sheet layout and header are as issued; the item IDs equal the expected set exactly (no missing,
extra or duplicate rows, same order); the locked columns (Kannada, English, drafts) and the 3 example rows are
unchanged. Per draft:
  fine            -> verified text = the draft; a fix typed next to "fine" makes the draft invalid;
  wrong           -> the fix must be non-empty and differ from the draft, else invalid;
  empty OK?       -> not done yet (reported as an empty cell); a fix with an empty OK? is invalid.
Blind items (B part 1): both own versions are needed; one of the two missing is invalid.
Structural errors refuse the whole file (nothing written). Invalid drafts are reported, left out of the CSV and listed
in <name>_invalid.csv; the exit code is then 1. With --final every draft must be answered.

Quality report per batch: share of "fine" per form; identical fixes repeated across rows. AutoCorrect check on every
fix (and own text): capitals or Excel AutoCorrect replacements that are not in the draft (annotation/
autocorrect_en_excel16.tsv, exported from Excel 16 on 2026-10-25); reported, never fixed.

Usage:
  python annotation/merge_xlsx.py A annotator_A.xlsx [--final] [--out PATH]
  python annotation/merge_xlsx.py B annotator_B_part1.xlsx [annotator_B_part2.xlsx] [--final] [--out PATH]
  python annotation/merge_xlsx.py agree annotator_A.csv annotator_B.csv [--out PATH]    (kappa fine/wrong, 60 items)
  python annotation/merge_xlsx.py anchor annotator_A.csv annotator_B.csv [--out PATH]   (blind 40, K3 descriptive)
Outputs (default annotation/results/): annotator_<A|B>.csv, <name>_invalid.csv, <name>_flags.csv,
<name>_quality.json; agreement.json; anchoring.json.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO / "scripts"), str(REPO / "src")]

# ---------------------------------------------------------------- the sheet layout (shared with scripts/k_xlsx.py)
CSV_COLS = ["item_id", "annotator", "source", "natural_draft", "natural_verdict", "natural_text", "kanglish_draft",
            "kanglish_verdict", "kanglish_text", "note", "saved_at", "condition"]
OK_OPTS = ["fine", "wrong"]
FORMS = ("natural", "kanglish")
# (field, header, kind): kind = id | locked | ok | text
VERIFY_SHEET = [
    ("native", "Kannada", "locked"), ("english", "English", "locked"),
    ("natural_draft", "Gemini natural", "locked"), ("natural_ok", "Natural OK?", "ok"),
    ("natural_fix", "Natural fix", "text"),
    ("kanglish_draft", "Gemini Kanglish", "locked"), ("kanglish_ok", "Kanglish OK?", "ok"),
    ("kanglish_fix", "Kanglish fix", "text"),
    ("note", "Note", "text"), ("item_id", "Item ID", "id")]
BLIND_SHEET = [
    ("native", "Kannada", "locked"), ("english", "English", "locked"),
    ("natural_own", "Your natural", "text"), ("kanglish_own", "Your Kanglish", "text"),
    ("note", "Note", "text"), ("item_id", "Item ID", "id")]
ITEMS, README = "items", "READ_ME"
N_EXAMPLES = 3  # rows 2-4 of a verify sheet: locked worked examples, item ID "EXAMPLE 1".."EXAMPLE 3"
FIRST_ROW = {"verify": 2 + N_EXAMPLES, "blind": 2}


def example_rows() -> list:
    """The 3 worked examples (not among the 500 items), in verify-sheet fields. One fine, one wrong with a fix, one
    wrong because the meaning changed. Written by Claude Code as teaching material; Annotator A checks them first."""
    E = {e["id"]: e for e in json.load(open(REPO / "annotation/examples_v1.json", encoding="utf-8"))["examples"]}
    a, b, c = E["flores-212"], E["indicsentiment-test-245"], E["flores-993"]
    return [
        {"item_id": "EXAMPLE 1", "native": a["native"], "english": a["english"],
         "natural_draft": a["natural"]["draft"], "natural_ok": "fine", "natural_fix": None,
         "kanglish_draft": "(no Kanglish draft in this example)", "kanglish_ok": None, "kanglish_fix": None,
         "note": "EXAMPLE: fine. This is how people type it; do not change a draft just to match your own spelling."},
        {"item_id": "EXAMPLE 2", "native": b["native"], "english": b["english"],
         "natural_draft": b["natural"]["draft"], "natural_ok": "wrong", "natural_fix": b["natural"]["corrected"],
         "kanglish_draft": b["kanglish"]["draft"], "kanglish_ok": "wrong", "kanglish_fix": b["kanglish"]["corrected"],
         "note": "EXAMPLE: wrong + fix. \"bāsigeya\" has an accent mark and two words are misspelt; \"take "
                 "madkondidivi\" is not how people write."},
        {"item_id": "EXAMPLE 3", "native": c["native"], "english": c["english"],
         "natural_draft": c["natural"]["draft"], "natural_ok": "wrong", "natural_fix": c["natural"]["corrected"],
         "kanglish_draft": c["kanglish"]["draft"], "kanglish_ok": "wrong", "kanglish_fix": c["kanglish"]["corrected"],
         "note": "EXAMPLE: Kanglish wrong because the meaning changed (\"hodhre\" means \"if they go\"); natural wrong "
                 "because one word is still in Kannada script."}]


# ---------------------------------------------------------------- expected content

def expected(role: str, part: int = 1) -> list:
    """Rows a workbook must contain, in order."""
    import k_annotation as K
    blind = set(json.load(open(K.BLIND))["ids"])
    drafts = K.shown_drafts()
    rows = []
    for it in K.items():
        d = {k: drafts[(it["id"], k)]["text"] for k in FORMS}
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
    """R1 a sentence that starts with a capital, R2 a token with two leading capitals, R3 an AutoCorrect replacement
    (a non-ASCII symbol the list produces, the token "I", or a replacement whose misspelling is in the draft or in
    RISKY_KEYS). Each flag says whether the same pattern is already in the draft (then it is probably not AutoCorrect)."""
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
    return [{"rule": rule, "match": what, "also_in_draft": bool(d) and what in d} for rule, what in out]


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


def read_sheet(wb, spec, P: Problems, label: str) -> list:
    if ITEMS not in wb.sheetnames:
        P.add(label, f"sheet '{ITEMS}' missing")
        return []
    ws = wb[ITEMS]
    head = [cell_str(c.value) for c in ws[1]][:len(spec)]
    if head != [h for _, h, _ in spec]:
        P.add(f"{label} {ITEMS}", f"header changed: {head}")
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


def check_ids(got, exp_ids, where, P):
    dup = sorted({x for x in got if got.count(x) > 1})
    missing, extra = [x for x in exp_ids if x not in got], [x for x in got if x not in exp_ids]
    if dup or missing or extra:
        P.add(where, f"item IDs differ from the expected set: missing {missing[:5]}{'…' if len(missing) > 5 else ''}"
                     f" ({len(missing)}), extra {extra[:5]} ({len(extra)}), duplicated {dup[:5]} ({len(dup)})")
    elif got != exp_ids:
        P.add(where, "item rows are in a different order than issued (IDs are complete; order changed)")


def read_verify(path: Path, exp: list, P: Problems, label: str, who: str) -> dict:
    """{recs: {item_id: csv row}, invalid: [...], empty: [...], flags: [...], fixes: [...]}"""
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    rows = read_sheet(wb, VERIFY_SHEET, P, label)
    ex, data = rows[:N_EXAMPLES], rows[N_EXAMPLES:]
    want = example_rows()
    if [cell_str(r["item_id"]) for r in ex] != [w["item_id"] for w in want] or any(
            cell_str(r[f]) != cell_str(w[f]) for r, w in zip(ex, want) for f, _, _ in VERIFY_SHEET):
        P.add(f"{label} {ITEMS}", "the 3 example rows were changed or moved")
    check_ids([cell_str(r["item_id"]) for r in data], [e["item_id"] for e in exp], f"{label} {ITEMS}", P)
    exp_by, when = {e["item_id"]: e for e in exp}, saved_at(wb, path)
    out = {"recs": {}, "invalid": [], "empty": [], "flags": [], "fixes": []}
    for r in data:
        i = cell_str(r["item_id"])
        if i not in exp_by:
            continue
        e, where = exp_by[i], f"{label} {ITEMS}!row {r['_row']} ({i})"
        for f, _, kind in VERIFY_SHEET:
            if kind == "locked" and cell_str(r[f]) != cell_str(e[f]):
                P.add(where, f"locked column '{f}' was changed")
        rec = {"item_id": i, "annotator": who, "source": e["source"], "note": cell_str(r["note"]).strip(),
               "saved_at": when, "condition": "draft"}
        for k in FORMS:
            ok, fix, draft = cell_str(r[f"{k}_ok"]).strip(), cell_str(r[f"{k}_fix"]).strip(), e[f"{k}_draft"]
            rec[f"{k}_draft"] = draft
            rec[f"{k}_verdict"] = rec[f"{k}_text"] = ""
            bad = None
            if not ok:
                if fix:
                    bad = "a fix is typed but OK? is empty"
                else:
                    out["empty"].append({"file": path.name, "row": r["_row"], "item_id": i, "cell": f"{k} OK?"})
                    continue
            elif ok not in OK_OPTS:
                bad = f"OK? is {ok!r}, not fine/wrong"
            elif ok == "fine" and fix:
                bad = "marked fine but a fix is typed"
            elif ok == "wrong" and not fix:
                bad = "marked wrong but the fix is empty"
            elif ok == "wrong" and fix == draft.strip():
                bad = "marked wrong but the fix equals the draft"
            if bad:
                out["invalid"].append({"file": path.name, "row": r["_row"], "item_id": i, "form": k, "ok": ok,
                                       "fix": fix, "problem": bad})
                continue
            rec[f"{k}_verdict"], rec[f"{k}_text"] = ok, (draft if ok == "fine" else fix)
            if ok == "wrong":
                out["fixes"].append({"item_id": i, "form": k, "fix": fix})
                for fl in flags_for(fix, draft):
                    out["flags"].append({"file": path.name, "row": r["_row"], "item_id": i, "field": f"{k} fix", **fl,
                                         "text": fix})
        if any(rec[f"{k}_verdict"] for k in FORMS) or rec["note"]:
            out["recs"][i] = rec
    return out


def read_blind(path: Path, exp: list, P: Problems, label: str, who: str) -> dict:
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    rows = read_sheet(wb, BLIND_SHEET, P, label)
    check_ids([cell_str(r["item_id"]) for r in rows], [e["item_id"] for e in exp], f"{label} {ITEMS}", P)
    exp_by, when = {e["item_id"]: e for e in exp}, saved_at(wb, path)
    out = {"recs": {}, "invalid": [], "empty": [], "flags": [], "fixes": []}
    for r in rows:
        i = cell_str(r["item_id"])
        if i not in exp_by:
            continue
        e, where = exp_by[i], f"{label} {ITEMS}!row {r['_row']} ({i})"
        for f, _, kind in BLIND_SHEET:
            if kind == "locked" and cell_str(r[f]) != cell_str(e[f]):
                P.add(where, f"locked column '{f}' was changed")
        own = {k: cell_str(r[f"{k}_own"]).strip() for k in FORMS}
        if not any(own.values()):
            out["empty"] += [{"file": path.name, "row": r["_row"], "item_id": i, "cell": f"your {k}"} for k in FORMS]
            continue
        if not all(own.values()):
            out["invalid"].append({"file": path.name, "row": r["_row"], "item_id": i, "form": "both", "ok": "",
                                   "fix": "", "problem": "only one of the two versions is written"})
            continue
        rec = {"item_id": i, "annotator": who, "source": e["source"], "note": cell_str(r["note"]).strip(),
               "saved_at": when, "condition": "blind"}
        for k in FORMS:
            rec.update({f"{k}_draft": "", f"{k}_verdict": "", f"{k}_text": own[k]})
            for fl in flags_for(own[k], ""):
                out["flags"].append({"file": path.name, "row": r["_row"], "item_id": i, "field": f"your {k}", **fl,
                                     "text": own[k]})
        out["recs"][i] = rec
    return out


def quality(recs: dict, fixes: list) -> dict:
    q = {}
    for k in FORMS:
        v = [r[f"{k}_verdict"] for r in recs.values() if r[f"{k}_verdict"]]
        q[f"{k}_fine_share"] = (sum(x == "fine" for x in v) / len(v)) if v else None
        q[f"{k}_n_verified"] = len(v)
    c = Counter((f["form"], f["fix"]) for f in fixes)
    q["repeated_fixes"] = [{"form": k, "fix": t, "n_rows": n,
                            "items": [f["item_id"] for f in fixes if (f["form"], f["fix"]) == (k, t)]}
                           for (k, t), n in c.items() if n > 1]
    return q


def write_csv(path: Path, cols, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def read_csv(path) -> list:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- agreement and anchoring (descriptive)

def agreement(a_csv, b_csv) -> dict:
    """Cohen's kappa on fine/wrong, A vs B, on B's 60 verify items (descriptive; replaces the rating kappas)."""
    from sklearn.metrics import cohen_kappa_score
    A = {r["item_id"]: r for r in read_csv(a_csv)}
    B = {r["item_id"]: r for r in read_csv(b_csv) if r["condition"] == "draft"}
    res = {"items_expected": len(expected("B", 2))}
    for k in FORMS:
        ids = [i for i in B if i in A and A[i][f"{k}_verdict"] and B[i][f"{k}_verdict"]]
        a, b = [A[i][f"{k}_verdict"] for i in ids], [B[i][f"{k}_verdict"] for i in ids]
        kap = float(cohen_kappa_score(a, b)) if ids and len(set(a) | set(b)) > 1 else None
        res[k] = {"n": len(ids), "kappa": kap, "agree_share": (sum(x == y for x, y in zip(a, b)) / len(ids)) if ids
                  else None, "fine_share_A": (a.count("fine") / len(a)) if a else None,
                  "fine_share_B": (b.count("fine") / len(b)) if b else None,
                  "table": {f"A {x} / B {y}": sum(p == x and q == y for p, q in zip(a, b)) for x in OK_OPTS
                            for y in OK_OPTS}}
    return res


def k3b_module():
    """scripts/k3b_dakshina.py (the K3b statistics), imported without its command line (it reads sys.argv[2] as the
    language at import; with no arguments it is Kannada)."""
    saved = sys.argv
    sys.argv = [saved[0]]
    try:
        import k3b_dakshina as k3b
    finally:
        sys.argv = saved
    return k3b


def anchoring(a_csv, b_csv) -> dict:
    """Blind 40: B's from-scratch text vs the Gemini draft and vs A's verified text. The K3b statistics (pooled rates,
    ratio with 90% and 95% bootstrap CIs, other / B) and chrF (other against B). Descriptive, no rule (K3 descriptive
    after the 2026-10-26 protocol change)."""
    import pandas as pd
    import english_share as es
    import k_annotation as K
    k3b = k3b_module()
    wl = es.wordlists()["zipf>=3"]
    blind = json.load(open(K.BLIND))["ids"]
    exp = {e["item_id"]: e for e in expected("A")}
    A = {r["item_id"]: r for r in read_csv(a_csv)}
    B = {r["item_id"]: r for r in read_csv(b_csv) if r["condition"] == "blind"}
    stats = {"natural": "natural", "kanglish": "kanglish"}
    res = {"blind_items": len(blind), "status": "descriptive, no rule"}
    for k in stats:
        ids = [i for i in blind if i in B and B[i][f"{k}_text"]]
        texts = {"B": [B[i][f"{k}_text"] for i in ids], "gemini": [exp[i][f"{k}_draft"] for i in ids]}
        ids_a = [i for i in ids if i in A and A[i][f"{k}_text"]]
        out = {"n_B": len(ids), "n_with_A": len(ids_a)}
        H = pd.DataFrame([k3b.counts(t, wl) for t in texts["B"]])
        for other, T, idx in (("gemini", texts["gemini"], ids), ("A_verified", [A[i][f"{k}_text"] for i in ids_a],
                                                                  ids_a)):
            if not idx:
                out[other] = None
                continue
            G = pd.DataFrame([k3b.counts(t, wl) for t in T])
            Hs = H.iloc[[ids.index(i) for i in idx]].reset_index(drop=True)
            o = {}
            for name, num, den in (("vowel_doubling", "vowel_doubling", "letters"),
                                   ("h_digraph", "h_digraph", "letters"), ("english_word_share", "english", "words")):
                r = k3b.ratio_ci(G, Hs, num, den)
                fin = lambda x: x if x == x else None  # noqa: E731  (NaN, e.g. B's rate is 0, -> null)
                o[name] = {"rate_other": fin(r["gemini_rate"]), "rate_B": fin(r["human_rate"]),
                           "ratio_other_to_B": fin(r["ratio"]), "ci90": [fin(x) for x in r["ci90"]],
                           "ci95": [fin(x) for x in r["ci95"]]}
            o["chrf_other_vs_B"] = K.chrf_stats(pd.Series(T), pd.Series([B[i][f"{k}_text"] for i in idx]))
            out[other] = o
        res[k] = out
    return res


# ---------------------------------------------------------------- command line

def main(argv) -> int:
    final = "--final" in argv
    out = None
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])
        argv = argv[:argv.index("--out")] + argv[argv.index("--out") + 2:]
    args = [a for a in argv if a != "--final"]
    if not args:
        print(__doc__)
        return 2
    role, files = args[0], [Path(a) for a in args[1:]]
    res = REPO / "annotation" / "results"
    if role in ("agree", "anchor"):
        r = (agreement if role == "agree" else anchoring)(files[0], files[1])
        out = out or res / ("agreement.json" if role == "agree" else "anchoring.json")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(r, indent=1, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(r, indent=1, ensure_ascii=False))
        return 0
    if role not in ("A", "B"):
        print(__doc__)
        return 2
    P = Problems()
    if role == "A":
        parts = [read_verify(files[0], expected("A"), P, "A", "A")]
    else:
        parts = [read_blind(files[0], expected("B", 1), P, "B part 1", "B")]
        if len(files) > 1:
            parts.append(read_verify(files[1], expected("B", 2), P, "B part 2", "B"))
    recs = {i: r for p in parts for i, r in p["recs"].items()}
    invalid, empty = [x for p in parts for x in p["invalid"]], [x for p in parts for x in p["empty"]]
    flags, fixes = [x for p in parts for x in p["flags"]], [x for p in parts for x in p["fixes"]]
    order = [e["item_id"] for e in expected("A")]
    rows = [recs[i] for i in order if i in recs]
    out = out or res / f"annotator_{role}.csv"
    q = quality({i: r for i, r in recs.items() if r["condition"] == "draft"}, fixes)
    new_flags = [f for f in flags if not f["also_in_draft"]]
    report = {"role": role, "files": [f.name for f in files], "structural_errors": list(P),
              "items_with_answers": len(rows), "empty_cells": len(empty), "invalid": len(invalid),
              "fine_share": {k: q[f"{k}_fine_share"] for k in FORMS},
              "n_verified": {k: q[f"{k}_n_verified"] for k in FORMS},
              "repeated_fixes": len(q["repeated_fixes"]), "autocorrect_flags_not_in_draft": len(new_flags),
              "autocorrect_flag_rules": {k: sum(f["rule"].startswith(k) for f in new_flags) for k in ("R1", "R2", "R3")}}
    if final and empty:
        P.add(role, f"{len(empty)} cells not answered (--final)")
    report["written"] = None
    if not P:
        write_csv(out, CSV_COLS, rows)
        stem = out.with_name(out.stem)
        write_csv(Path(str(stem) + "_invalid.csv"), ["file", "row", "item_id", "form", "ok", "fix", "problem"], invalid)
        write_csv(Path(str(stem) + "_flags.csv"), ["file", "row", "item_id", "field", "rule", "match", "also_in_draft",
                                                    "text"], flags)
        Path(str(stem) + "_quality.json").write_text(json.dumps({**q, "empty_cells": empty}, indent=1,
                                                                ensure_ascii=False), encoding="utf-8")
        report["written"] = str(out)
    report["structural_errors"] = list(P)
    print(json.dumps(report, indent=1, ensure_ascii=False))
    for x in invalid[:30]:
        print(f"  invalid {x['file']} row {x['row']} {x['item_id']} {x['form']}: {x['problem']}")
    for f in new_flags[:30]:
        print(f"  flag {f['file']} row {f['row']} {f['item_id']} {f['field']}: {f['rule']} [{f['match']}]")
    for rf in q["repeated_fixes"][:10]:
        print(f"  repeated fix ({rf['form']}, {rf['n_rows']} rows): {rf['fix'][:60]!r}")
    return 1 if (P or invalid) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
