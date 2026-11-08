"""Read-only generator of results/phase2/RESULTS_READABLE.md, version 2 (2026-11-09): one block per experiment id; each block lists the FULL outcome of every comparison in the registered
rule's result files (every model, form and contrast, with value, CI, n, p, p_holm and verdict as stored), as compact tables, raw numbers, no rounding, no interpretation.
Registration and result entry titles come verbatim from RESULTS.md (commit and date from git blame, through scripts/results_readable.py and scripts/full_results_dump.py). A table is cut only where
a CAP is stated in its header line; every cut says how many rows the file has.
"""
import csv
import importlib.util
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def load(name, fn):
    spec = importlib.util.spec_from_file_location(name, REPO / "scripts" / fn)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


fd = load("fd", "full_results_dump.py")
rr = load("rr", "results_readable.py")
OUT = REPO / "results" / "phase2" / "RESULTS_READABLE.md"
RES = REPO / "results"
IDENT = ("model", "name", "contrast", "measure", "tokenizer", "form", "id", "verdict_line", "language", "lang")
SKIPK = {"provenance", "examples", "argv", "rule", "caveat", "prediction", "text", "label", "note", "registration", "source", "config"}

# (relative path under results/, options). opts: skip (extra keys), maxdepth, cap (rows), filt (CSV row predicate), cols (CSV columns), keep_rule (keep the registered rule text)
SPEC = {
    "E1": [("e01_cost/summary.csv", dict(filt=lambda r: r["lang"] == "kan_Knda" and r["form"] == "native", cols=["tokenizer", "form", "n_sentences", "tokens_total", "fertility", "tax_ratio", "tax_ci_low", "tax_ci_high"], cap=80))],
    "E2": [("e02_translit/roundtrip_flores_plus.json", {}), ("e02_translit/lossy_flores_plus.json", {})],
    "E5": [("e05_pretrain/analysis.json", dict(cap=60))],
    "E9": [("e09_romanize/savings.json", dict(cap=60))],
    "E0": [("e00_gate/summary.json", {})],
    "M1": [("m14_full/gate2/verdicts.json", dict(maxdepth=6))],
    "S3": [("m1_tiny_mdl/analysis.json", dict(maxdepth=5, cap=80))],
    "M4": [("m4b_mapping/summary.csv", {}), ("m4c_natural/summary.csv", {}), ("m4b_surface/verdict.json", dict(maxdepth=4, cap=60)), ("m4b_mapping/verdict.json", dict(maxdepth=2)), ("m4c_natural/verdict.json", dict(maxdepth=4, cap=60))],
    "E0b": [("e0b_familiarity/gate1/verdicts.json", dict(maxdepth=6)), ("e0b_familiarity/gate1/mcnemar.csv", {})],
    "E0c": [("e0c_sib/gate/verdicts.json", dict(maxdepth=6)), ("e0c_sib/gate/mcnemar.csv", {})],
    "BT": [],
    "L": [("l_ladder/verdict.json", dict(maxdepth=6)), ("l_ladder/contrasts.csv", {})],
    "NC": [("nc1/verdict.json", dict(maxdepth=6)), ("nc1/contrasts.csv", {})],
    "K": [("k3b/verdict.json", {}), ("k12/verdict.json", {}), ("k12/k1.csv", {}), ("k12/k2a.csv", {}), ("k12/k2b.csv", {}), ("v_dbl/summary.json", dict(cap=60))],
    "H": [("h_hindi/h1_verdict.json", {}), ("h_hindi/h1.csv", {}), ("h1lf/opt1_verdict.json", {}), ("h1lf/opt1.csv", {}), ("h1lf/opt2_verdict.json", {}), ("h1lf/opt2.csv", {}), ("k3b_hi/verdict.json", {})],
    "EP": [("ep1/predictions.json", dict(maxdepth=5, cap=40)), ("ep2/predictions.json", dict(maxdepth=5, cap=40)), ("ep_robust/main_estimates.csv", {})],
    "X1": [("phase2/x1/t2/analysis/summary.json", dict(maxdepth=6, cap=60)), ("phase2/x1/t2/analysis/ta_primary_mcnemar.csv", {}), ("phase2/x1/t2/analysis/ta_secondary_mcnemar.csv", {}), ("phase2/x1/t2/analysis/tb_verdicts.csv", {})],
    "X2": [("phase2/x2/exposure.json", {})],
    "X3": [("phase2/x3/verdict.json", {}), ("phase2/x3/contrasts.csv", dict(filt=lambda r: r["counted"] in ("True", "true", "1"), cols=["measure", "model", "contrast", "cond", "n", "diff", "ci", "p", "p_holm", "significant", "ci_excludes_0"], cap=200))],
    "X4": [(f"phase2/x4/{l}/{r}.json", dict(cap=60)) for l in ("bn", "te") for r in ("r1", "r2", "r3", "r4")] + [("phase2/x4/k3b_bn/verdict.json", {}), ("phase2/x4/k3b_te/verdict.json", {})],
    "X5": [("phase2/x5/analysis.json", {})],
    "X6": [("phase2/x6/counting.json", {})],
    "X7": [("phase2/x7/analysis.json", {}), ("phase2/x7a/analysis.json", {})],
    "X8": [("phase2/x8/analysis.json", {})],
    "X9a": [("phase2/x9a/analysis.json", {}), ("phase2/x9a/analysis_low.json", {})],
    "X9b": [("phase2/x9b/analysis_sarvam-1.json", {}), ("phase2/x9b/analysis_sarvam-1_seeds0123.json", {}), ("phase2/x9b/analysis_qwen3.5-2b.json", {}), ("phase2/x9b/analysis_qwen3.5-2b_seeds012.json", {})],
    "X10": [("phase2/x10/analysis.json", dict(cap=60))],
    "X11": [("phase2/x11/analysis.json", {})],
    "X12": [("phase2/x12/contrast1.json", {}), ("phase2/x12/contrast2_mdl.json", {})],
    "X13": [("phase2/x13/qwen3-8b/analysis.json", {}), ("phase2/x13/llama-3.1-8b/analysis.json", {}), ("phase2/x13/sarvam-m/analysis.json", {})],
    "X14": [("phase2/x14/analysis.json", {})],
    "X15": [],
    "A": [("kaggle/kaggle_retrieval_gate/2026-11-02T133412/out/gate_retrieval.json", dict(cap=60, skip=["test_acc_per_layer", "train_acc_per_layer"])), ("kaggle/a1r_result.json", {})],
}
NOTES = {
    "A": ["Note (facts from the files and RESULTS.md 3712): gate_passed=false and models.*.pass=false in gate_retrieval.json are the in-kernel flags; the laptop reference file results/m4b_mapping/summary.csv was not in the Kaggle package, so the kernel had no reference to compare with. "
          "The registered comparison (tolerance 0.03) was run locally and is in results/kaggle/a1r_result.json (commit 43865a1, 2026-11-02 19:26:56 +0530): all four cells have pass=true; RESULTS.md 3712 logs it as `A1-R retrieval gate: PASSED`."],
    "X3": ["Note (facts from results/phase2/x3/verdict.json and RESULTS.md 3400-3412): D1 = a minus NC-O is the Phase 1 NC-O contrast on the matched items; D2 = a minus c and D3 = NC-O minus c are the contrasts the registered interpretation uses. "
           "D1|retrieval|m = effect, positive (2 of 2 needed); D2|retrieval|m and D3|retrieval|m = no effect detected (0 of 2 needed). Registered interpretation applied (RESULTS.md 3460-3471): unresolved for all three measures."],
    "X13": ["Note: results/phase2/PHASE2_INVENTORY.md (last changed 2026-11-05 22:15) still lists `X13 Sarvam-m: lossy, lowercase, natural forms and X10` as not run (quota); analysis.json here has forms_scored = six forms and forms_not_reached = [] (RESULTS.md 4049, 2026-11-08 15:33 IST entry: scored 2026-11-07 03:00 to 06:18 on account 3)."],
}


def sc(v):
    return json.dumps(v, ensure_ascii=False)


def scalar_fields(d, skip):
    out = []
    for k, v in d.items():
        if k in skip:
            continue
        if isinstance(v, (str, int, float, bool)) or v is None:
            out.append(f"{k}={sc(v)}")
        elif isinstance(v, list):
            if len(v) <= 4 and all(isinstance(x, (int, float, str, bool)) or x is None for x in v):
                out.append(f"{k}={sc(v)}")
            elif v and all(isinstance(x, (int, float, str)) for x in v):
                out.append(f"{k}=[{len(v)} values]")
    return out


def records(o, path, skip, maxdepth, depth=0):
    if isinstance(o, dict):
        f = scalar_fields(o, skip)
        if f:
            yield path or "(top)", f
        if depth >= maxdepth:
            return
        for k, v in o.items():
            if k in skip or not isinstance(v, (dict, list)):
                continue
            if isinstance(v, list) and not (v and isinstance(v[0], (dict, list))):
                continue
            yield from records(v, f"{path}.{k}" if path else str(k), skip, maxdepth, depth + 1)
    elif isinstance(o, list):
        for i, x in enumerate(o):
            ident = next((f"{k}={x[k]}" for k in IDENT if isinstance(x, dict) and isinstance(x.get(k), (str, int)) and not isinstance(x.get(k), bool)), str(i))
            if isinstance(x, (dict, list)):
                yield from records(x, f"{path}[{ident}]", skip, maxdepth, depth)


def json_table(p: Path, o):
    skip = SKIPK | set(o.get("skip", ()))
    obj = json.loads(p.read_text(encoding="utf-8"))
    rows = [f"{lab} | " + "; ".join(f) for lab, f in records(obj, "", skip, o.get("maxdepth", 8))]
    return rows


def csv_table(p: Path, o):
    rows = list(csv.reader(open(p, encoding="utf-8", errors="replace", newline="")))
    hdr = rows[0]
    recs = [dict(zip(hdr, r)) for r in rows[1:]]
    if o.get("filt"):
        recs = [r for r in recs if o["filt"](r)]
    cols = o.get("cols") or hdr
    return [" | ".join(f"{c}={r.get(c, '')}" for c in cols) for r in recs], len(rows) - 1


def main() -> None:
    lines_md = (REPO / "RESULTS.md").read_text(encoding="utf-8").split("\n")
    bl = fd.blame()
    ents = fd.segment(lines_md)
    p2_start = next(i for i, ln in enumerate(lines_md, 1) if ln.startswith(fd.PHASE2_START_HEADING))
    for e in ents:
        e["phase"] = 2 if e["start"] >= p2_start else 1
    out = ["# Results, readable (one block per experiment id; tables of every comparison of the registered rule; plain facts)", "",
           "Source: result files under results/ (paths in each block) and verbatim RESULTS.md titles (commit and date from git blame). Numbers are raw, not rounded. No interpretation. Each table row is `label | field=value; ...` "
           "as stored in the file (CI as [low, high]; p_holm is the Holm-adjusted p where the file has it; verdict fields are the stored strings). A table is cut only where its header says CAP, with the file's row count. "
           "Phase 1, then Phase 2, then failed, dropped and not run.", ""]
    nblocks = 0
    for phase, groups in ((1, fd.P1), (2, fd.P2)):
        out += [f"## Phase {phase}", ""]
        for gid, name, pat, dirs in groups:
            sel = [e for e in ents if e["phase"] == phase and re.search(pat, e["title"])]

            def reg_ok(e):
                t2 = re.sub(r"^(PRE-)?REGISTRATION( \(.*?\))?\s*[-—]*\s*", "", e["title"])
                if e["kind"] == "###":
                    return e["title"].startswith(gid)
                return bool(re.search(pat, t2[:45])) and bool(re.match(r"(PRE-)?REGISTRATION", e["title"]))

            reg = next((e for e in sel if reg_ok(e)), None)
            res = next((e for e in reversed(sel) if re.search(r"RESULT|[Rr]esults?\b|GATE|supported|refuted|inconclusive|confirmed", e["title"]) and e is not reg), None)
            if res is None:
                res = next((e for e in reversed(sel) if e is not reg), None)

            if gid == "A":
                res = next((e for e in ents if "A1-R retrieval gate: PASSED" in e["title"]), res)

            def ent_line(tag, e):
                f = bl.get(e["start"], {})
                return f"{tag}: {e['title'][:230]} [RESULTS.md {e['start']}-{e['end']}, `{f.get('hash', '?')}` {f.get('date', '?')}]"

            blk = [f"### {gid}: {name}"]
            blk.append(ent_line("Registered", reg) if reg else "Registered: no separate registration entry (see the result entry)")
            fac = rr.facets_of(dirs if dirs else [])
            blk.append(rr.fac_line(fac, ("models",), "Models run"))
            blk.append(rr.fac_line(fac, ("forms", "conditions"), "Forms/conditions run") + "; " + rr.fac_line(fac, ("tasks", "measures"), "tasks/measures") + "; " + rr.fac_line(fac, ("seeds",), "seeds"))
            srcs = []
            for rel, o in SPEC.get(gid, []):
                p = RES / rel
                if not p.exists():
                    blk.append(f"[{rel}] file not found")
                    continue
                srcs.append(f"results/{rel}")
                try:
                    if p.suffix == ".csv":
                        rows, total = csv_table(p, o)
                        shown = rows[: o.get("cap", 400)]
                        note = f"{len(rows)} rows of {total}" + (f"; CAP {o['cap']}" if len(rows) > len(shown) else "")
                    else:
                        rows = json_table(p, o)
                        shown = rows[: o.get("cap", 400)]
                        note = f"{len(rows)} records" + (f"; CAP {o['cap']}" if len(rows) > len(shown) else "")
                except Exception as ex:  # noqa: BLE001
                    blk.append(f"[{rel}] could not be read: {ex}")
                    continue
                blk.append(f"Table [{rel}] ({note}):")
                blk += ["  " + r for r in shown]
            if not SPEC.get(gid):
                blk.append("no result file; the numbers are in the RESULTS.md entry cited below" if gid == "BT" else "not run; no result file")
            blk += NOTES.get(gid, [])
            blk.append(ent_line("Result entry", res) if res else "Result entry: none in RESULTS.md")
            blk.append("Source files: " + ("; ".join(srcs) or "none"))
            out += blk + [""]
            nblocks += 1
    out += ["## Failed, dropped and not run (one line each, as logged)", ""]
    pat = rr_pat = re.compile(r"FAILED|failed|Failure|failure|not run|NOT RUN|did not run|dropped|DROPPED|cancelled|skipped|incident|STALL|CRASH|crash|EXHAUSTED|considered|not built|unavailable|Chain incident|NO INTERNET")
    for e in [x for x in ents if pat.search(x["title"])]:
        f = bl.get(e["start"], {})
        out.append(f"- {f.get('date', '?')[:10]} | {e['title'][:300]} [RESULTS.md {e['start']}-{e['end']}, `{f.get('hash', '?')}`]")
    inv = (REPO / "results" / "phase2" / "PHASE2_INVENTORY.md").read_text(encoding="utf-8").split("\n")
    out += ["", "From results/phase2/PHASE2_INVENTORY.md, the rows listed as not run (verbatim):", ""]
    on = False
    for ln in inv:
        if ln.startswith("## Not run"):
            on = True
            continue
        if ln.startswith("## ") and on:
            on = False
        if on and ln.startswith("|") and not ln.startswith("|---") and not ln.startswith("| Experiment"):
            out.append("- " + ln + (" **SUPERSEDED by later entries:** lossy, lowercase and natural were scored 2026-11-07 03:00 to 06:18 on account 3 (RESULTS.md 4049; x13/sarvam-m/analysis.json forms_scored = six forms, forms_not_reached = []); "
                                    "X10 for Sarvam-m: pilot 2026-11-08 16:23, native finished 2026-11-08 21:37 (RESULTS.md 4056), ITRANS running, lossy, lowercase and natural not run by the decision of 2026-11-08 16:23 (RESULTS.md 4054)." if "X13 Sarvam-m: lossy, lowercase, natural forms and X10" in ln else ""))
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"blocks: {nblocks}; total lines: {len(OUT.read_text(encoding='utf-8').splitlines())}")


if __name__ == "__main__":
    sys.exit(main())
