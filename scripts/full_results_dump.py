"""Read-only generator of results/phase2/FULL_RESULTS_DUMP.md (index) and results/phase2/dump/*.md (2026-11-08, Aarnav's request).

Everything is scraped from RESULTS.md (entries are copied verbatim, with the commit and date of their first line from `git blame`), from the files under results/ (every CSV, JSON, MD and TXT is
dumped in full except the item-level files listed under "Not dumped" in each file) and from the paper tables (paper2/tables). No interpretation is added: the only labels are keywords found in the entry's
own first line. Nothing is rerun and no file outside results/phase2/dump/ and results/phase2/FULL_RESULTS_DUMP.md is written.
Usage: python scripts/full_results_dump.py
"""
import csv
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "results" / "phase2" / "dump"
MAIN = REPO / "results" / "phase2" / "FULL_RESULTS_DUMP.md"
FENCE = "`````"
PHASE2_START_HEADING = "## PHASE 2 PRE-REGISTRATION"
SUBSPLIT = ("## PHASE 2 PRE-REGISTRATION", "## PHASE 2 AMENDMENT 2")
MAX_CSV_ROWS = 2000
MAX_JSON_BYTES = 600_000
FACET_KEYS = {"model": "models", "models": "models", "form": "forms", "forms": "forms", "task": "tasks", "tasks": "tasks", "seed": "seeds", "seeds": "seeds", "language": "languages", "lang": "languages",
              "languages": "languages", "vocab": "vocab", "level": "level", "cond": "conditions", "condition": "conditions", "measure": "measures"}

# ---------------------------------------------------------------------------------------------------------------- groups
# (id, name, regex over the entry title, result directories relative to results/)
P1 = [
    ("E1", "Token cost atlas", r"\bE1\b|E1/E2", ["e01_cost", "e01_cost_flores_plus"]),
    ("E2", "Transliteration round trip and lossy scheme", r"\bE2\b|E1/E2", ["e02_translit"]),
    ("E5", "Controlled pretraining of tiny GPTs", r"\bE5\b", ["e05_pretrain"]),
    ("E9", "Tokenizer-optimal reversible romanization", r"\bE9\b", ["e09_romanize"]),
    ("E0", "Gate, tokens per word, natural romanization checks, Step 0", r"E0 GATE|E0 add-on|E0 natural|Step 0 decisions", ["e00_gate", "e0b_natural_check", "data_kn_wiki"]),
    ("M1", "Detokenization layer (M1) on pretrained models", r"M1 detokenization|GATE 2: full M1|Word-clustered CIs for M1|item-level fragmentation", ["m14_pilot", "m14_full"]),
    ("S3", "Step 3 and 3b: word-identity, MDL and erasure probes on the E5 tiny models", r"Step 3", ["m1_tiny", "m1_tiny_mdl"]),
    ("M4", "M4, M4b, M4c: retrieval, mapping, surface baseline, natural romanization", r"M4b|M4c|M4 |Surface baseline|English alignment|Accuracy vs mechanism|alignment, natural",
     ["m4b_mapping", "m4b_mapping_pilot_qwen25", "m4b_robustness", "m4b_surface", "m4c_curves", "m4c_natural", "m4c_surface"]),
    ("E0b", "Familiarity test (sentiment, XNLI)", r"E0b", ["e0b_familiarity", "matched"]),
    ("E0c", "SIB-200 topic classification", r"E0c", ["e0c_sib"]),
    ("BT", "Back-translation comprehension gap (large model)", r"[Bb]ack-translation|Large-model result", []),
    ("L", "Romanization ladder L1 to L3", r"ladder|L1 casing|L3 on items|ITRANS . lossy", ["l_ladder", "l_ladder_posthoc"]),
    ("NC", "NC1: non-canonical tokenization of lossy text", r"NC1|NC-F", ["nc1", "nc1_posthoc"]),
    ("K", "Kanglish, annotation, K1 to K3, K3b, natural+dbl, V-VER, K2b", r"K1|K2|K3|Kanglish|[Aa]nnotation|annotator|Annotator|natural\+dbl|V-VER|Verify|verify|Verified|Rater|Dakshina|A6|Phase B|K2b|Workbook|workbook",
     ["k_verified", "k12", "k3b", "v_dbl", "v_ver"]),
    ("H", "Hindi: H-Hindi, H1, H1-LF, K3b-hi, English-loan measures", r"Hindi|H1|H-Hindi|English-loan|English-word share|Share of English|English words|English-share|tagger|loan", ["h_hindi", "h1lf", "k3b_hi", "english_share", "codemix_check"]),
    ("EP", "Activation patching E-P1, E-P2, EP-R", r"E-P1|E-P2|EP-R|GPU safety", ["ep1", "ep2", "ep_robust"]),
]
P2 = [
    ("X1", "Second prompt template (T2) and Kannada instruction (T3)", r"\bX1\b|\bT3\b|T-a|T-b", ["phase2/x1"]),
    ("X2", "Measured romanized exposure", r"\bX2\b", ["phase2/x2"]),
    ("X3", "Frequency-matched non-canonical tokenization", r"\bX3\b", ["phase2/x3"]),
    ("X4", "Bengali and Telugu replication, K3b-bn, K3b-te", r"\bX4\b|K3b-bn|K3b-te|Dakshina", ["phase2/x4"]),
    ("X5", "Cross-language consistency", r"\bX5\b", ["phase2/x5"]),
    ("X6", "New models screen and counting", r"\bX6\b", ["phase2/x6"]),
    ("X7", "Tiny-GPT embedding accounting, factorized control, X7-A, X7b", r"\bX7|X7-", ["phase2/x7", "phase2/x7a"]),
    ("X8", "Blind second-annotator sample", r"\bX8\b", ["phase2/x8"]),
    ("X9a", "Tiny GPT, familiarity manipulated, fragmentation fixed; X9a-low and extra seeds", r"X9a", ["phase2/x9a"]),
    ("X9b", "QLoRA continued pretraining (Sarvam-1 primary, Qwen3.5-2B secondary), extra seeds", r"X9b|\bX9\b", ["phase2/x9b"]),
    ("X10", "Generation FLORES+ devtest to English (and post hoc, Sarvam-m)", r"\bX10\b", ["phase2/x10"]),
    ("X11", "Quantization control", r"\bX11\b", ["phase2/x11"]),
    ("X12", "Ambari natural experiment", r"\bX12\b", ["phase2/x12"]),
    ("X13", "7 to 9B and Sarvam-m models", r"\bX13\b", ["phase2/x13"]),
    ("X14", "Black-box hosted models", r"\bX14\b", ["phase2/x14"]),
    ("X15", "Human intelligibility baseline", r"\bX15\b", ["phase2/x15"]),
    ("A", "General rules A0, Kaggle precision and retrieval checks A1-P and A1-R, reproducibility gate", r"^A[01]\b|A1-P|A1-R|A0\.|A1\.|reproducibility gate|Kaggle runner", []),
]


# ---------------------------------------------------------------------------------------------------------------- RESULTS.md
def blame():
    r = subprocess.run(["git", "blame", "--line-porcelain", "--", "RESULTS.md"], cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")
    info, cur = {}, None
    for ln in r.stdout.split("\n"):
        m = re.match(r"^([0-9a-f]{40}) (\d+) (\d+)(?: \d+)?$", ln)
        if m:
            cur = {"hash": m.group(1)[:7], "final": int(m.group(3))}
            continue
        if cur is None:
            continue
        if ln.startswith("author-time "):
            cur["t"] = int(ln.split()[1])
        elif ln.startswith("author-tz "):
            cur["tz"] = ln.split()[1]
        elif ln.startswith("\t"):
            tz = cur.get("tz", "+0000")
            sign = 1 if tz[0] == "+" else -1
            off = dt.timezone(sign * dt.timedelta(hours=int(tz[1:3]), minutes=int(tz[3:5])))
            cur["date"] = dt.datetime.fromtimestamp(cur["t"], off).strftime("%Y-%m-%d %H:%M:%S %z")
            info[cur["final"]] = cur
            cur = None
    return info


def segment(lines):
    """Entries of RESULTS.md: '## ' sections, '### ' sub-sections inside the two big Phase 2 registrations, and '- **20' log bullets. Returns list of dicts with 1-based line range."""
    bounds = []
    in_split = False
    parent = ""
    for i, ln in enumerate(lines, 1):
        if ln.startswith("## "):
            in_split = ln.startswith(SUBSPLIT)
            parent = ln[3:].strip()
            bounds.append((i, "##", ln[3:].strip(), ""))
        elif ln.startswith("### ") and in_split:
            bounds.append((i, "###", ln[4:].strip(), parent))
        elif re.match(r"^- \*\*20", ln):
            bounds.append((i, "-", re.sub(r"\*\*", "", ln[2:]).strip(), ""))
    ents = []
    first = bounds[0][0]
    if first > 1:
        ents.append({"start": 1, "end": first - 1, "kind": "preamble", "title": "RESULTS.md preamble"})
    for k, (s, kind, title, par) in enumerate(bounds):
        e = (bounds[k + 1][0] - 1) if k + 1 < len(bounds) else len(lines)
        ents.append({"start": s, "end": e, "kind": kind, "title": title, "parent": par})
    return ents


LABELS = [("registered", r"PRE-REGISTRATION|REGISTRATION|REGISTERED|registered before|Registration"), ("amended", r"DEVIATION|AMENDMENT|ADDENDUM|PROTOCOL CHANGE|CLARIFICATION|Corrections?\b|CHANGE"),
          ("exploratory", r"[Ee]xploratory"), ("post hoc", r"[Pp]ost hoc"), ("result", r"RESULT|[Rr]esults?\b|GATE|FINISHED|verdict|supported|refuted|inconclusive"),
          ("failed or not run", r"FAILED|failed|Failure|failure|not run|NOT RUN|did not run|dropped|DROPPED|cancelled|skipped|incident|STALL|CRASH|crash|EXHAUSTED")]


def labels_of(title, parent=""):
    """Keyword labels from the entry's own title; for a sub-section the parent heading's words are used too."""
    return [name for name, pat in LABELS if re.search(pat, title + " " + parent)]


# ---------------------------------------------------------------------------------------------------------------- result files
def git_first(path):
    r = subprocess.run(["git", "log", "--diff-filter=A", "--format=%h %ai", "--", path], cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")
    ls = [x for x in r.stdout.strip().split("\n") if x]
    return ls[-1] if ls else "untracked"


def flat(o, pre=""):
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            out += flat(v, f"{pre}.{k}" if pre else str(k))
    elif isinstance(o, list):
        if o and all(isinstance(x, (int, float, str, bool)) or x is None for x in o):
            out.append(f"{pre} = {json.dumps(o, ensure_ascii=False)}")
        else:
            for i, v in enumerate(o):
                out += flat(v, f"{pre}[{i}]")
    else:
        out.append(f"{pre} = {json.dumps(o, ensure_ascii=False)}")
    return out


def collect_facets(o, facets):
    if isinstance(o, dict):
        for k, v in o.items():
            fk = FACET_KEYS.get(k)
            if fk:
                vs = v if isinstance(v, list) else [v]
                for x in vs:
                    if isinstance(x, (str, int, float)):
                        facets.setdefault(fk, set()).add(str(x))
            collect_facets(v, facets)
    elif isinstance(o, list):
        for x in o[:5000]:
            collect_facets(x, facets)


def dump_file(p: Path, rel: str, facets):
    """Markdown for one result file; returns (lines, note_if_not_dumped)."""
    suf = p.suffix.lower()
    size = p.stat().st_size
    L = [f"#### `{rel}` ({size:,} bytes; first commit {git_first(rel)})", ""]
    try:
        if suf == ".csv":
            with open(p, encoding="utf-8", errors="replace", newline="") as f:
                rows = list(csv.reader(f))
            if not rows:
                return L + ["(empty file)", ""], None
            hdr = rows[0]
            for h in hdr:
                fk = FACET_KEYS.get(h)
                if fk:
                    ci = hdr.index(h)
                    for r in rows[1:]:
                        if ci < len(r):
                            facets.setdefault(fk, set()).add(r[ci])
            if len(rows) - 1 > MAX_CSV_ROWS:
                return None, f"`{rel}`: {len(rows) - 1:,} data rows, columns {hdr} (item-level file, not dumped)"
            L.append("| " + " | ".join(hdr) + " |")
            L.append("|" + "---|" * len(hdr))
            for r in rows[1:]:
                L.append("| " + " | ".join(c.replace("|", "\\|").replace("\n", " ") for c in r) + " |")
            return L + [""], None
        if suf == ".json":
            if size > MAX_JSON_BYTES:
                return None, f"`{rel}`: {size:,} bytes JSON (item-level or curve file, not dumped)"
            o = json.loads(p.read_text(encoding="utf-8", errors="replace"))
            collect_facets(o, facets)
            L.append(FENCE + "text")
            L += flat(o)
            L += [FENCE, ""]
            return L, None
        if suf in (".md", ".txt", ".out", ".tsv"):
            txt = p.read_text(encoding="utf-8", errors="replace")
            if len(txt) > 400_000:
                return None, f"`{rel}`: {len(txt):,} characters of text (not dumped)"
            return L + [FENCE + "text", txt.rstrip("\n"), FENCE, ""], None
    except Exception as e:  # noqa: BLE001
        return L + [f"(could not be read: {e!r})", ""], None
    return None, f"`{rel}`: {suf or 'no extension'} file, {size:,} bytes (binary or per-item data, not dumped)"


def files_in(dirrel):
    base = REPO / "results" / dirrel
    if not base.exists():
        return []
    out = []
    for p in sorted(base.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            out.append(p)
    return out


# ---------------------------------------------------------------------------------------------------------------- writers
def entry_block(e, lines, bl):
    first = bl.get(e["start"], {})
    last = bl.get(e["end"], {})
    head = f"##### {e['title'][:240]}"
    meta = (f"RESULTS.md lines {e['start']} to {e['end']}; first line committed in `{first.get('hash', '?')}` on {first.get('date', '?')}; last line in `{last.get('hash', '?')}` on {last.get('date', '?')}; "
            f"labels from the title and parent heading: {', '.join(labels_of(e['title'], e.get('parent', ''))) or 'none'}")
    return [head, "", meta, "", FENCE + "text"] + lines[e["start"] - 1:e["end"]] + [FENCE, ""]


def write_group(gid, name, phase, ents, dirs, lines, bl, fname):
    facets = {}
    notdumped = []
    body = []
    for d in dirs:
        for p in files_in(d):
            rel = p.relative_to(REPO).as_posix()
            if p.suffix.lower() in (".csv", ".json", ".md", ".txt", ".out", ".tsv"):
                blk, note = dump_file(p, rel, facets)
                if blk:
                    body += blk
                if note:
                    notdumped.append(note)
            else:
                _, note = dump_file(p, rel, facets) if False else (None, f"`{rel}`: {p.suffix or 'no extension'} file, {p.stat().st_size:,} bytes (binary or per-item data, not dumped)")
                notdumped.append(note)
    L = [f"# {gid}: {name} (Phase {phase})", "", "Source: RESULTS.md entries (verbatim) and result files (paths given with every file). No interpretation added.", ""]
    L += ["## Registration and log entries in RESULTS.md (commit and date of the first line from git blame)", "", "| status labels (keywords in the title and parent heading) | commit | date | lines | title |", "|---|---|---|---|---|"]
    for e in ents:
        f = bl.get(e["start"], {})
        L.append(f"| {', '.join(labels_of(e['title'], e.get('parent', ''))) or 'none'} | `{f.get('hash', '?')}` | {f.get('date', '?')} | {e['start']}-{e['end']} | {e['title'][:160].replace('|', '/')} |")
    L += ["", "## Values observed in the result files (read from the files' own columns and keys)", ""]
    if facets:
        for k in ("models", "languages", "forms", "tasks", "seeds", "vocab", "level", "conditions", "measures"):
            if k in facets:
                vs = sorted(facets[k], key=lambda s: (len(s), s))
                L.append(f"- {k}: {', '.join(vs[:80])}{' ... (' + str(len(vs)) + ' values in all)' if len(vs) > 80 else ''}")
    else:
        L.append("- no model, form, task or seed columns in the dumped files; see the entries")
    L += ["", "Result directories: " + (", ".join(f"`results/{d}`" for d in dirs) if dirs else "none (numbers are in the RESULTS.md entries)"), ""]
    L += ["## RESULTS.md entries, verbatim", ""]
    for e in ents:
        L += entry_block(e, lines, bl)
    L += ["## Result files, every number", ""]
    L += body if body else ["(no result files for this experiment)", ""]
    L += ["## Not dumped (item-level, binary or too large; path and size only)", ""]
    L += [f"- {n}" for n in notdumped] if notdumped else ["- none"]
    L.append("")
    (OUT / fname).write_text("\n".join(L), encoding="utf-8")
    return len(L), len(ents), len(body)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.md"):
        old.unlink()
    lines = (REPO / "RESULTS.md").read_text(encoding="utf-8").split("\n")
    bl = blame()
    ents = segment(lines)
    p2_start = next(i for i, ln in enumerate(lines, 1) if ln.startswith(PHASE2_START_HEADING))
    for e in ents:
        e["phase"] = 2 if e["start"] >= p2_start else 1
    index_rows, total = [], 0
    n_exp = 0

    def run(groups, phase, prefix):
        nonlocal total, n_exp
        assigned = set()
        for gid, name, pat, dirs in groups:
            sel = [e for e in ents if e["phase"] == phase and re.search(pat, e["title"])]
            for e in sel:
                assigned.add(id(e))
            fn = f"P{phase}_{gid}.md"
            nl, ne, nb = write_group(gid, name, phase, sel, dirs, lines, bl, fn)
            index_rows.append((phase, gid, name, fn, nl, ne))
            total += nl
            n_exp += 1
        rest = [e for e in ents if e["phase"] == phase and id(e) not in assigned]
        return rest

    rest1 = run(P1, 1, "P1")
    rest2 = run(P2, 2, "P2")
    for phase, rest in ((1, rest1), (2, rest2)):
        fn = f"P{phase}_OTHER_ENTRIES.md"
        L = [f"# Phase {phase}: RESULTS.md entries not matched to an experiment id above (verbatim, nothing omitted)", ""]
        for e in rest:
            L += entry_block(e, lines, bl)
        (OUT / fn).write_text("\n".join(L), encoding="utf-8")
        index_rows.append((phase, "OTHER", "Entries not matched to an experiment id", fn, len(L), len(rest)))
        total += len(L)

    # Kaggle run outputs (Phase 2): small JSON of every run
    kfac, knd, kb = {}, [], []
    for p in sorted((REPO / "results" / "kaggle").rglob("*")):
        if not p.is_file():
            continue
        parts = p.relative_to(REPO / "results" / "kaggle").parts
        if "repo" in parts or p.suffix.lower() in (".log", ".html", ".pt", ".tmp", ".safetensors", ".npy", ".parquet") or p.name == "adapter_config.json" or p.name.endswith(".meta.json") and False:
            if p.suffix.lower() not in (".log", ".html") and "repo" not in parts:
                knd.append(f"`{p.relative_to(REPO).as_posix()}`: {p.suffix} file, {p.stat().st_size:,} bytes (binary or per-item data, not dumped)")
            continue
        if p.suffix.lower() in (".json", ".csv", ".md", ".txt"):
            blk, note = dump_file(p, p.relative_to(REPO).as_posix(), kfac)
            if blk:
                kb += blk
            if note:
                knd.append(note)
    L = ["# Phase 2: Kaggle and laptop run outputs (results/kaggle), every small result file", "", "Per-run done.json (loss logs), retrieval.json, sib meta files, gate and precision outputs, quota ledgers. `repo/` copies, logs, adapters, checkpoints and per-item parquet/npy files are not dumped.", ""]
    for k in ("models", "forms", "tasks", "seeds", "conditions"):
        if k in kfac:
            L.append(f"- {k}: {', '.join(sorted(kfac[k], key=lambda s: (len(s), s))[:80])}")
    L += [""] + kb + ["## Not dumped", ""] + ([f"- {n}" for n in knd] or ["- none"])
    (OUT / "P2_KAGGLE_RUNS.md").write_text("\n".join(L), encoding="utf-8")
    index_rows.append((2, "KAGGLE", "Kaggle and laptop run outputs (results/kaggle)", "P2_KAGGLE_RUNS.md", len(L), 0))
    total += len(L)

    # Phase 2 results folder files not under an x directory (model sizes, ledgers)
    L = ["# Phase 2: other result files in results/phase2 (outside the experiment folders)", ""]
    fac = {}
    for p in sorted((REPO / "results" / "phase2").glob("*")):
        if p.is_file() and p.suffix.lower() in (".json", ".csv", ".md") and p.name not in ("FULL_RESULTS_DUMP.md",):
            blk, note = dump_file(p, p.relative_to(REPO).as_posix(), fac)
            if blk:
                L += blk
    (OUT / "P2_OTHER_FILES.md").write_text("\n".join(L), encoding="utf-8")
    index_rows.append((2, "FILES", "Other files in results/phase2 (ledgers, model sizes, claims table, inventory)", "P2_OTHER_FILES.md", len(L), 0))
    total += len(L)


    # Phase 1 files at the top of results/ (not in a folder): OVERNIGHT.md dumped, logs and markers listed
    L = ["# Phase 1: files at the top level of results/ (outside the experiment folders)", ""]
    nd = []
    fac = {}
    for p in sorted((REPO / "results").glob("*")):
        if p.is_file() and not p.name.startswith("CHAIN_STATUS_"):
            if p.suffix.lower() in (".md", ".json", ".csv", ".txt"):
                blk, note = dump_file(p, p.relative_to(REPO).as_posix(), fac)
                if blk:
                    L += blk
                if note:
                    nd.append(note)
            else:
                nd.append(f"`{p.relative_to(REPO).as_posix()}`: {p.suffix or 'no extension'} file, {p.stat().st_size:,} bytes (process log or marker, not dumped)")
    L += ["## Not dumped", ""] + ([f"- {n}" for n in nd] or ["- none"])
    (OUT / "P1_OTHER_FILES.md").write_text(chr(10).join(L), encoding="utf-8")
    index_rows.append((1, "FILES", "Other files at the top of results/ (OVERNIGHT.md, logs, markers)", "P1_OTHER_FILES.md", len(L), 0))
    total += len(L)

    # cross-cutting lists
    def listing(fname, title, pat, extra=None):
        sel = [e for e in ents if re.search(pat, e["title"])]
        L = [f"# {title}", "", f"Entries whose title matches the keywords `{pat}` (verbatim, with commit and date). Phase 1 first.", ""]
        for ph in (1, 2):
            L += [f"## Phase {ph}", ""]
            for e in [x for x in sel if x["phase"] == ph]:
                L += entry_block(e, lines, bl)
        if extra:
            L += extra
        (OUT / fname).write_text("\n".join(L), encoding="utf-8")
        return len(L), len(sel)

    n1, c1 = listing("LIST_DEVIATIONS.md", "Every deviation, amendment, protocol change and clarification in RESULTS.md", r"DEVIATION|deviation|AMENDMENT|ADDENDUM|PROTOCOL CHANGE|CLARIFICATION|Corrections?\b|Correction|CHANGE|Target change|NOTE|Note:",
                     ["## The deviations table of the paper (paper2/tables/deviations.tex, verbatim)", "", FENCE + "text", (REPO / "paper2" / "tables" / "deviations.tex").read_text(encoding="utf-8"), FENCE, ""])
    index_rows.append((0, "LIST", "Deviations, amendments, protocol changes (all phases)", "LIST_DEVIATIONS.md", n1, c1))
    n2, c2 = listing("LIST_FAILED_DROPPED_NOT_RUN.md", "Runs that failed, were dropped or were not run (entries with the reason as logged)", r"FAILED|failed|Failure|failure|not run|NOT RUN|did not run|dropped|DROPPED|cancelled|skipped|incident|STALL|CRASH|crash|EXHAUSTED|considered|not built|unavailable|Chain incident")
    index_rows.append((0, "LIST", "Failed, dropped, not run (all phases)", "LIST_FAILED_DROPPED_NOT_RUN.md", n2, c2))
    L = ["# Experiments still running or waiting (every results/CHAIN_STATUS_*.md, verbatim)", ""]
    for p in sorted((REPO / "results").glob("CHAIN_STATUS_*.md")):
        L += [f"## `{p.relative_to(REPO).as_posix()}`", "", FENCE + "text", p.read_text(encoding="utf-8").rstrip("\n"), FENCE, ""]
    arch = REPO / "results" / "phase2"
    for p in sorted(arch.glob("CHAIN_STATUS_*.md")):
        L += [f"## `{p.relative_to(REPO).as_posix()}` (archived status)", "", FENCE + "text", p.read_text(encoding="utf-8").rstrip("\n"), FENCE, ""]
    (OUT / "LIST_RUNNING_AND_CHAIN_STATUS.md").write_text("\n".join(L), encoding="utf-8")
    index_rows.append((0, "LIST", "Chain status files (running, waiting, done, failed)", "LIST_RUNNING_AND_CHAIN_STATUS.md", len(L), 0))
    L = ["# Paper tables (paper2/tables, verbatim)", ""]
    for p in sorted((REPO / "paper2" / "tables").rglob("*.tex")):
        L += [f"## `{p.relative_to(REPO).as_posix()}`", "", FENCE + "text", p.read_text(encoding="utf-8").rstrip("\n"), FENCE, ""]
    (OUT / "PAPER_TABLES.md").write_text("\n".join(L), encoding="utf-8")
    index_rows.append((0, "LIST", "Paper tables", "PAPER_TABLES.md", len(L), 0))
    L = ["# Full RESULTS.md ledger (every entry in file order, verbatim, with commit and date)", ""]
    for e in ents:
        L += entry_block(e, lines, bl)
    (OUT / "RESULTS_MD_LEDGER.md").write_text("\n".join(L), encoding="utf-8")
    index_rows.append((0, "LIST", "RESULTS.md ledger in file order (every entry once)", "RESULTS_MD_LEDGER.md", len(L), len(ents)))

    # index (main file)
    tot_lines = 0
    idx = ["# Full results dump (Phase 1 and Phase 2)", "",
           "Generated 2026-11-08 by `scripts/full_results_dump.py`, read-only. Every number is copied from RESULTS.md (verbatim entries with the commit and date of the first line, from `git blame`), from the files under `results/` and from the paper tables; nothing is",
           "rounded, shortened, interpreted or recomputed. The only labels are keywords found in each entry's own title. Registered rules and verdicts are in the verbatim entries.",
           "Not dumped, by rule (listed by path and size at the end of each file): CSV files with more than 2,000 data rows, JSON files above 600,000 bytes, and binary or per-item files (parquet, npy, npz, adapters, checkpoints).", "",
           "Each experiment file has: the table of its RESULTS.md entries (labels, commit, date, lines, title); the models, languages, forms, tasks and seeds found in its result files; the entries verbatim; every result file with its path and first commit; the not-dumped list.", "",
           "## Index (Phase 1, then Phase 2, then cross-cutting lists)", "", "| phase | id | name | file | lines in file | RESULTS.md entries |", "|---|---|---|---|---|---|"]
    order = sorted(index_rows, key=lambda r: ({1: 0, 2: 1, 0: 2}[r[0]], 0))
    for ph, gid, name, fn, nl, ne in order:
        nl = len((OUT / fn).read_text(encoding="utf-8").split("
")) - 1  # actual lines in the file
        idx.append(f"| {'1' if ph == 1 else '2' if ph == 2 else 'all'} | {gid} | {name} | `results/phase2/dump/{fn}` | {nl} | {ne} |")
    MAIN.write_text("\n".join(idx) + "\n", encoding="utf-8")
    all_files = sorted(OUT.glob("*.md")) + [MAIN]
    tot_lines = sum(len(f.read_text(encoding="utf-8").split("\n")) for f in all_files)
    print(f"files: {len(all_files)}; experiments (groups): {n_exp}; RESULTS.md entries: {len(ents)}; total lines: {tot_lines}")
    for f in all_files:
        print(f.relative_to(REPO).as_posix(), len(f.read_text(encoding="utf-8").split("\n")))


if __name__ == "__main__":
    sys.exit(main())
