"""Read-only generator of results/phase2/RESULTS_READABLE.md (2026-11-08): one block per experiment id (Phase 1, then Phase 2), at most 15 lines each, plain facts.
Headline lines come from the registered rule's own result file (verdict fields and CI-bearing values, raw numbers, no rounding); the verdict is copied verbatim from those files, and the RESULTS.md
registration and result entry titles are copied verbatim with commit and date (git blame). Failed, dropped and not-run items follow as one line each, copied from RESULTS.md entries and from
results/phase2/PHASE2_INVENTORY.md. No interpretation is added.
"""
import csv
import importlib.util
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("fd", REPO / "scripts" / "full_results_dump.py")
fd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fd)
OUT = REPO / "results" / "phase2" / "RESULTS_READABLE.md"
MAXL = 15

# headline files per experiment id (the registered rule's result files)
HEAD = {
    "E1": ["e01_cost/summary.csv"], "E2": ["e02_translit/roundtrip_flores_plus.json", "e02_translit/lossy_flores_plus.json"], "E5": ["e05_pretrain/analysis.json"], "E9": ["e09_romanize/savings.json"],
    "E0": ["e00_gate/summary.json"], "M1": ["m14_full/gate2/verdicts.json"], "S3": ["m1_tiny_mdl/analysis.json"],
    "M4": ["m4b_mapping/verdict.json", "m4c_natural/verdict.json", "m4b_surface/verdict.json", "m4b_robustness/verdict.json"], "E0b": ["e0b_familiarity/gate1/verdicts.json"],
    "E0c": ["e0c_sib/gate/verdicts.json"], "BT": [], "L": ["l_ladder/verdict.json"], "NC": ["nc1/verdict.json"], "K": ["k3b/verdict.json", "k12/k1.csv", "v_dbl/summary.json"],
    "H": ["h_hindi/h1_verdict.json", "h1lf/opt1_verdict.json", "k3b_hi/verdict.json"], "EP": ["ep1/predictions.json", "ep2/predictions.json", "ep_robust/summary.json"],
    "X1": ["phase2/x1/t2/analysis/summary.json"], "X2": ["phase2/x2/exposure.json"], "X3": ["phase2/x3/verdict.json"], "X4": ["phase2/x4/bn/r1.json", "phase2/x4/te/r1.json", "phase2/x4/k3b_bn/verdict.json", "phase2/x4/k3b_te/verdict.json"],
    "X5": ["phase2/x5/analysis.json"], "X6": ["phase2/x6/counting.json"], "X7": ["phase2/x7/analysis.json", "phase2/x7a/analysis.json"], "X8": ["phase2/x8/analysis.json"],
    "X9a": ["phase2/x9a/analysis.json", "phase2/x9a/analysis_low.json"], "X9b": ["phase2/x9b/analysis_sarvam-1.json", "phase2/x9b/analysis_sarvam-1_seeds0123.json", "phase2/x9b/analysis_qwen3.5-2b_seeds012.json"],
    "X10": ["phase2/x10/analysis.json"], "X11": ["phase2/x11/analysis.json"], "X12": ["phase2/x12/contrast1.json", "phase2/x12/contrast2_mdl.json"],
    "X13": ["phase2/x13/qwen3-8b/analysis.json", "phase2/x13/llama-3.1-8b/analysis.json", "phase2/x13/sarvam-m/analysis.json"], "X14": ["phase2/x14/analysis.json"], "X15": [],
    "A": ["kaggle/kaggle_retrieval_gate/2026-11-02T133412/out/gate_retrieval.json"],
}
SKIP = {"provenance", "rule", "text", "label", "prediction", "note", "registration", "source", "config"}
PRIO_KEYS = ("verdict", "P_a", "R1", "R2", "R3", "R4", "K3b", "X10_P", "H1", "H2", "H3", "status", "holds", "n_positive", "n_significant_positive", "needed", "n_counted", "gate_passed")
FACET_KEYS = fd.FACET_KEYS


def flat_pairs(o, pre=""):
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            if k in SKIP:
                continue
            out += flat_pairs(v, f"{pre}.{k}" if pre else str(k))
    elif isinstance(o, list):
        if o and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in o):
            out.append((pre, o))
        elif o and all(isinstance(x, str) for x in o) and len(o) <= 8:
            out.append((pre, o))
        else:
            for i, v in enumerate(o[:40]):
                out += flat_pairs(v, f"{pre}[{i}]")
    else:
        out.append((pre, o))
    return out


def pick_from_json(obj, limit):
    """Priority: verdict-like leaves, then values that have a CI sibling (printed with their CI) and n."""
    pairs = flat_pairs(obj)
    d = dict(pairs)
    chosen, seen = [], set()

    def add(p, text):
        if p not in seen:
            seen.add(p)
            chosen.append(text)

    for p, v in pairs:
        leaf = p.split(".")[-1]
        if (leaf in PRIO_KEYS or leaf.endswith("verdict")) and isinstance(v, (str, bool, int)):
            add(p, f"{p} = {json.dumps(v)}")
    for p, v in pairs:
        leaf = p.split(".")[-1]
        base = p[: -len(leaf)]
        if re.fullmatch(r"(ci|ci95|ci975|ci90|ci_95)", leaf) and isinstance(v, list) and len(v) == 2:
            vk = next((base + k for k in ("point", "diff", "acc", "acc_cal", "ratio", "mean", "gap", "did", "kappa", "cer_mean") if base + k in d), None)
            n = next((d[base + k] for k in ("n", "n_items", "n_test") if base + k in d), None)
            if vk:
                add(vk, f"{vk} = {json.dumps(d[vk])}; CI = {json.dumps(v)}" + (f"; n = {n}" if n is not None else ""))
        m = re.match(r"^(.*)_ci(?:95|975)?$", leaf)
        if m and isinstance(v, list) and len(v) == 2 and base + m.group(1) in d:
            vk = base + m.group(1)
            add(vk, f"{vk} = {json.dumps(d[vk])}; CI = {json.dumps(v)}")
    if len(chosen) < 2:  # no verdict-like or CI-bearing leaves: first and last row of a table (list of dicts), else the first scalar results
        def tables(o, pre=""):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k not in SKIP:
                        yield from tables(v, f"{pre}.{k}" if pre else str(k))
            elif isinstance(o, list) and o and all(isinstance(x, dict) for x in o):
                yield pre, o
        for pre, rows in tables(obj):
            for tag, r in (("first", rows[0]), ("last", rows[-1])) if len(rows) > 1 else (("only", rows[0]),):
                sc = [(k, v) for k, v in r.items() if isinstance(v, (int, float, str, bool)) and k not in SKIP]
                chosen.append(f"{pre}[{tag} of {len(rows)}]: " + "; ".join(f"{k}={json.dumps(v)}" for k, v in sc[:9]))
            if len(chosen) >= limit:
                break
        if len(chosen) < 2:
            for p_, v in pairs:
                if isinstance(v, (int, float)) and not isinstance(v, bool) or isinstance(v, list):
                    chosen.append(f"{p_} = {json.dumps(v)}")
                if len(chosen) >= limit:
                    break
    return chosen[:limit]


def csv_rows(p: Path, k):
    rows = list(csv.reader(open(p, encoding="utf-8", errors="replace", newline="")))
    hdr = rows[0]
    return [f"row {i + 1} of {len(rows) - 1}: " + "; ".join(f"{h}={c}" for h, c in zip(hdr, r)) for i, r in enumerate(rows[1:1 + k])]


def facets_of(dirs):
    fac = {}
    for d in dirs:
        for p in fd.files_in(d):
            if p.suffix.lower() == ".csv" and p.stat().st_size < 3_000_000:
                try:
                    with open(p, encoding="utf-8", errors="replace", newline="") as f:
                        rows = list(csv.reader(f))
                    if 1 < len(rows) <= 20001:
                        for h in rows[0]:
                            fk = FACET_KEYS.get(h)
                            if fk:
                                ci = rows[0].index(h)
                                for r in rows[1:]:
                                    if ci < len(r) and r[ci]:
                                        fac.setdefault(fk, set()).add(r[ci])
                except Exception:  # noqa: BLE001
                    pass
            elif p.suffix.lower() == ".json" and p.stat().st_size <= fd.MAX_JSON_BYTES and "provenance" not in p.name:
                try:
                    fd.collect_facets(json.loads(p.read_text(encoding="utf-8", errors="replace")), fac)
                except Exception:  # noqa: BLE001
                    pass
    return fac


def fac_line(fac, keys, label):
    vs = []
    for k in keys:
        vs += sorted(fac.get(k, []), key=lambda s: (len(s), s))
    vs = list(dict.fromkeys(vs))
    return f"{label}: " + (", ".join(vs[:30]) + (f" (+{len(vs) - 30} more)" if len(vs) > 30 else "") if vs else "not recorded as a column or key in the result files")


def main() -> None:
    lines_md = (REPO / "RESULTS.md").read_text(encoding="utf-8").split("\n")
    bl = fd.blame()
    ents = fd.segment(lines_md)
    p2_start = next(i for i, ln in enumerate(lines_md, 1) if ln.startswith(fd.PHASE2_START_HEADING))
    for e in ents:
        e["phase"] = 2 if e["start"] >= p2_start else 1
    out = ["# Results, readable (one block per experiment id, at most 15 lines each; plain facts)", "",
           "Source: result files under results/ and verbatim RESULTS.md titles (commit and date from git blame). Numbers are raw, not rounded. No interpretation. Phase 1, then Phase 2, then failed, dropped and not run.", ""]
    nblocks = 0
    for phase, groups in ((1, fd.P1), (2, fd.P2)):
        out += [f"## Phase {phase}", ""]
        for gid, name, pat, dirs in groups:
            sel = [e for e in ents if e["phase"] == phase and re.search(pat, e["title"])]
            def reg_ok(e):
                t2 = re.sub(r"^(PRE-)?REGISTRATION( \(.*?\))?\s*[-—]*\s*", "", e["title"])
                if e["kind"] == "###":
                    return e["title"].startswith(gid)  # registration sub-sections are titled "X9b. ...", "A0. ..."
                return bool(re.search(pat, t2[:45])) and bool(re.match(r"(PRE-)?REGISTRATION", e["title"]))
            reg = next((e for e in sel if reg_ok(e)), None)
            res = next((e for e in reversed(sel) if re.search(r"RESULT|[Rr]esults?\b|GATE|supported|refuted|inconclusive|confirmed", e["title"]) and e is not reg), None)
            if res is None:  # no title with result or verdict words: the last entry of the group that is not the registration entry
                res = next((e for e in reversed(sel) if e is not reg), None)
            blk = [f"### {gid}: {name}"]

            def ent_line(tag, e):
                f = bl.get(e["start"], {})
                return f"{tag}: {e['title'][:230]} [RESULTS.md {e['start']}-{e['end']}, `{f.get('hash', '?')}` {f.get('date', '?')}]"

            blk.append(ent_line("Registered", reg) if reg else "Registered: no separate registration entry (see the result entry)")
            fac = facets_of(dirs if dirs else [])
            blk.append(fac_line(fac, ("models",), "Models run"))
            blk.append(fac_line(fac, ("forms", "conditions"), "Forms/conditions run") + "; " + fac_line(fac, ("tasks", "measures"), "tasks/measures") + "; " + fac_line(fac, ("seeds",), "seeds"))
            heads = []
            for rel in HEAD.get(gid, []):
                p = REPO / "results" / rel
                if not p.exists():
                    continue
                if p.suffix == ".json":
                    heads += [f"{x}  [{rel}]" for x in pick_from_json(json.loads(p.read_text(encoding="utf-8")), 4)]
                else:
                    heads += [f"{x}  [{rel}]" for x in csv_rows(p, 2)]
            if not HEAD.get(gid):
                heads.append("no result file; the numbers are in the RESULTS.md entry cited below" if gid == "BT" else "not run; no result file")
            room = MAXL - len(blk) - 3
            blk += heads[:max(room, 1)]
            blk.append(ent_line("Result entry", res) if res else "Result entry: none in RESULTS.md")
            blk.append("Source files: " + ("; ".join(f"results/{r}" for r in HEAD.get(gid, [])) or "none"))
            out += blk[:MAXL] + [""]
            nblocks += 1
    # failed, dropped, not run
    out += ["## Failed, dropped and not run (one line each, as logged)", ""]
    pat = r"FAILED|failed|Failure|failure|not run|NOT RUN|did not run|dropped|DROPPED|cancelled|skipped|incident|STALL|CRASH|crash|EXHAUSTED|considered|not built|unavailable|Chain incident|NO INTERNET|no internet"
    for e in [x for x in ents if re.search(pat, x["title"])]:
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
            out.append("- " + ln)
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    n = len(OUT.read_text(encoding="utf-8").split("\n")) - 1
    print(f"blocks: {nblocks}; total lines: {n}")


if __name__ == "__main__":
    sys.exit(main())
