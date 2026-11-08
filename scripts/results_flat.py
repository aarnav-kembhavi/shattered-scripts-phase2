"""Read-only generator of results/phase2/RESULTS_FLAT.md (2026-11-08): one line per result, "ID | model | form | task | metric | value | CI | n | source file".
Parsed from the same files and with the same inclusion rules as the full dump (CSV up to 2,000 data rows, JSON up to 600,000 bytes; per-item, binary and prose files are skipped). Values are the file's own
strings or JSON numbers, not rounded or reformatted. Qualifiers that have no column in the format (seed, vocab, level, layer, language, contrast, ...) are written in the metric field as `metric [k=v; ...]`.
Usage: python scripts/results_flat.py
"""
import csv
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location("fd", REPO / "scripts" / "full_results_dump.py")
fd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fd)

OUT = REPO / "results" / "phase2" / "RESULTS_FLAT.md"
MAX_CSV_ROWS, MAX_JSON_BYTES = 2000, 600_000
MODELS = {"qwen2.5-1.5b", "qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-8b", "llama-3.1-8b", "sarvam-m", "llama-2-7b", "ambari-7b-base", "ambari-7b-instruct-v0.1", "ambari-7b-instruct-v0.2",
          "llama-3.2-1b", "oro-1.7b", "allam-2-7b", "openai__gpt-oss-120b", "qwen__qwen3.8-27b", "gpt-oss-120b", "qwen3.8-27b", "gemini-3.5-flash-lite"}
FORMS = {"native", "itrans", "lossy", "lower", "lowercase", "natural", "english", "natural_verified", "natural_dbl", "kanglish", "nc_a", "nc_b", "nc_c", "x3_m", "x3_r", "natural257", "natural500",
         "natural_dbl500", "natural_verified500", "lossy500", "lower500", "universal", "t2", "t3"}
TASKS = {"sib", "sentiment", "xnli", "retrieval", "sib-200 accuracy", "flores+ retrieval", "sib-200", "generation", "mdl"}
CI_KEYS = {"ci", "ci95", "ci975", "ci90", "ci_95", "conf_int"}
VALUE_KEYS = ("point", "diff", "acc", "acc_cal", "acc_unmapped", "ratio", "mean", "gap", "did", "kappa", "cer_mean", "est", "value", "rate", "r", "rho")
SKIP_KEYS = {"provenance", "rule", "prediction", "text", "note", "notes", "label", "registration", "source", "argv", "python", "platform", "git_commit", "timestamp_utc", "status", "reason", "description",
             "interpretation", "caveat", "joint_reading", "quote", "instruction", "config", "version"}
VERDICT_KEYS = {"verdict", "significant", "counted", "significant_positive", "significant_negative", "ci_excludes_0", "ci_holm_disagree", "pass", "above_0", "below_0", "informative", "R1", "R4", "K3b",
                "gate_passed", "reproduces_account1_exactly", "tokenizer_unchanged", "flagged", "H3_pattern_met", "reaches_original_native_level"}
QUALIFIER_NUM = {"seed", "vocab", "level", "layer", "id", "index", "step", "rank", "run", "fold", "k", "pct", "exposure"}
FORM_COLS, TASK_COLS, MODEL_COLS = {"form", "forms"}, {"task", "measure", "dataset"}, {"model", "tokenizer", "m"}
N_COLS = ("n", "n_items", "n_test", "n_sentences", "n_ids")
NUM = re.compile(r"^-?\d+(\.\d+)?([eE][-+]?\d+)?$")


def clean(x) -> str:
    return str(x).replace("|", "/").replace("\n", " ").strip()


def line(gid, model, form, task, metric, value, ci, n, src):
    return " | ".join([gid, clean(model), clean(form), clean(task), clean(metric), clean(value), clean(ci), clean(n), src])


def ci_text(a, b) -> str:
    return f"[{a}, {b}]"


# ---------------------------------------------------------------------------------------------------------------- CSV
def csv_lines(gid, p: Path, rel):
    rows = list(csv.reader(open(p, encoding="utf-8", errors="replace", newline="")))
    if len(rows) < 2 or len(rows) - 1 > MAX_CSV_ROWS:
        return []
    hdr = rows[0]
    idx = {h: i for i, h in enumerate(hdr)}
    out = []
    # CI column pairs
    pairs, used = {}, set()
    for h in hdr:
        m = re.match(r"^(.*?)_?ci(?:95|975|90)?_(low|lo|lower)$", h)
        if m:
            base = m.group(1)
            for hi in (h.replace("low", "high").replace("_lo", "_hi").replace("lower", "upper"),):
                if hi in idx and hi != h:
                    pairs[base] = (h, hi)
                    used |= {h, hi}
    ci_single = next((h for h in hdr if h in CI_KEYS), None)
    main_val = next((h for h in VALUE_KEYS if h in idx), None)
    for r in rows[1:]:
        g = lambda h: r[idx[h]].strip() if h in idx and idx[h] < len(r) else ""
        model = next((g(h) for h in hdr if h in MODEL_COLS and g(h)), "")
        form = next((g(h) for h in hdr if h in FORM_COLS and g(h)), "")
        task = next((g(h) for h in hdr if h in TASK_COLS and g(h)), "")
        n = next((g(h) for h in N_COLS if g(h)), "")
        quals = []
        for h in hdr:
            v = g(h)
            if h in MODEL_COLS | FORM_COLS | TASK_COLS or h in N_COLS or h in used or h == ci_single or v == "":
                continue
            if h in VERDICT_KEYS or (NUM.match(v) and h not in QUALIFIER_NUM):
                continue
            if NUM.match(v) and h in QUALIFIER_NUM or (not NUM.match(v) and len(v) <= 48):
                quals.append(f"{h}={v}")
        qs = f" [{'; '.join(quals)}]" if quals else ""
        for h in hdr:
            v = g(h)
            if v == "" or h in MODEL_COLS | FORM_COLS | TASK_COLS or h in N_COLS or h in used or h == ci_single:
                continue
            if h in VERDICT_KEYS:
                out.append(line(gid, model, form, task, h + qs, v, "", n, rel))
                continue
            if NUM.match(v) and h not in QUALIFIER_NUM:
                ci = ""
                if h in pairs:
                    ci = ci_text(g(pairs[h][0]), g(pairs[h][1]))
                elif h == main_val and ci_single:
                    ci = g(ci_single)
                elif h == main_val and ("ci_low" in idx and "ci_high" in idx):
                    ci = ci_text(g("ci_low"), g("ci_high"))
                out.append(line(gid, model, form, task, h + qs, v, ci, n, rel))
        for h in used | ({ci_single} if ci_single else set()):
            pass
        # CI columns that did not attach to a value column are written as their own results
        attached = {x for b in pairs for x in pairs[b]} if False else set()
    return out


# ---------------------------------------------------------------------------------------------------------------- JSON
def json_lines(gid, obj, rel):
    out = []

    def emit(model, form, task, path, value, ci, n):
        out.append(line(gid, model, form, task, ".".join(path), json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value, ci, n, rel))

    def walk(o, path, model, form, task, n):
        if isinstance(o, dict):
            model = o["model"] if isinstance(o.get("model"), str) else model
            form = o["form"] if isinstance(o.get("form"), str) else form
            task = o["task"] if isinstance(o.get("task"), str) else task
            nn = next((o[k] for k in N_COLS if isinstance(o.get(k), (int, float)) and not isinstance(o.get(k), bool)), None)
            n = nn if nn is not None else n
            cik = next((k for k in o if k in CI_KEYS and isinstance(o[k], list) and len(o[k]) == 2), None)
            vk = next((k for k in VALUE_KEYS if k in o and isinstance(o[k], (int, float)) and not isinstance(o[k], bool)), None)
            for k, v in o.items():
                if k in SKIP_KEYS or (k in ("model", "form", "task") and isinstance(v, str)) or k in N_COLS and isinstance(v, (int, float)):
                    continue
                lk = str(k).lower()
                m2, f2, t2, p2 = model, form, task, path
                if lk in MODELS:
                    m2 = str(k)
                elif lk in FORMS:
                    f2 = str(k)
                elif lk in TASKS:
                    t2 = str(k)
                else:
                    p2 = path + [str(k)]
                if cik and k == cik:
                    if vk is None:
                        emit(m2, f2, t2, p2, v, "", n)
                    continue
                if cik and vk and k == vk and isinstance(v, (int, float)):
                    emit(m2, f2, t2, p2, v, ci_text(o[cik][0], o[cik][1]), n)
                    continue
                walk(v, p2, m2, f2, t2, n)
        elif isinstance(o, list):
            if o and all(isinstance(x, (int, float)) and not isinstance(x, bool) or x is None for x in o):
                emit(model, form, task, path, o, "", n)
            elif o and all(isinstance(x, (int, float, str)) for x in o) and all(len(str(x)) <= 40 for x in o):
                emit(model, form, task, path, o, "", n)
            else:
                for i, v in enumerate(o):
                    walk(v, path + [f"[{i}]"], model, form, task, n)
        elif isinstance(o, bool):
            if path and (path[-1] in VERDICT_KEYS or "verdict" in ".".join(path)):
                emit(model, form, task, path, o, "", n)
        elif isinstance(o, (int, float)):
            emit(model, form, task, path, o, "", n)
        elif isinstance(o, str):
            if path and len(o) <= 60 and (path[-1] in VERDICT_KEYS or "verdict" in path[-1].lower()):
                emit(model, form, task, path, o, "", n)

    walk(obj, [], "", "", "", "")
    return out


def file_lines(gid, p: Path):
    rel = p.relative_to(REPO).as_posix()
    low = p.name.lower()
    if "provenance" in low or p.name == ".gitkeep":
        return []
    try:
        if p.suffix.lower() == ".csv":
            return csv_lines(gid, p, rel)
        if p.suffix.lower() == ".json" and p.stat().st_size <= MAX_JSON_BYTES:
            return json_lines(gid, json.loads(p.read_text(encoding="utf-8", errors="replace")), rel)
    except Exception as e:  # noqa: BLE001
        print("skip", rel, repr(e)[:80], file=sys.stderr)
    return []


def kaggle_id(rel: str) -> str:
    if "kaggle_x9b" in rel or "laptop_x9b" in rel:
        return "X9b"
    if "x_score" in rel:
        return "X12-X13-scoring"
    if "kaggle_precision" in rel:
        return "A1-P"
    if "kaggle_retrieval_gate" in rel:
        return "A1-R"
    if "kaggle_gate" in rel:
        return "GATE"
    if "kaggle_mdl" in rel:
        return "X12-X13-MDL"
    if "kaggle_x10" in rel:
        return "X10"
    return "KAGGLE-other"


def main() -> None:
    lines = ["ID | model | form | task | metric | value | CI | n | source file"]
    total = 0
    n_groups = 0
    for phase, groups in ((1, fd.P1), (2, fd.P2)):
        for gid, name, pat, dirs in groups:
            body = []
            for d in dirs:
                for p in fd.files_in(d):
                    if p.suffix.lower() in (".csv", ".json"):
                        body += file_lines(gid, p)
            if gid == "BT":
                pass
            if body:
                lines.append(f"## {gid}")
                lines += body
                n_groups += 1
                total += len(body)
    # phase 2 files outside the experiment folders
    body = []
    for p in sorted((REPO / "results" / "phase2").glob("*.json")):
        body += file_lines("P2-FILES", p)
    if body:
        lines.append("## P2-FILES")
        lines += body
        total += len(body)
    # Kaggle and laptop run outputs
    kb = {}
    for p in sorted((REPO / "results" / "kaggle").rglob("*")):
        if not p.is_file() or "repo" in p.relative_to(REPO / "results" / "kaggle").parts or p.suffix.lower() not in (".json", ".csv"):
            continue
        rel = p.relative_to(REPO).as_posix()
        gid = kaggle_id(rel)
        kb.setdefault(gid, []).extend(file_lines(gid, p))
    for gid in sorted(kb):
        if kb[gid]:
            lines.append(f"## {gid}")
            lines += kb[gid]
            total += len(kb[gid])
            n_groups += 1
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"result lines: {total}; groups with results: {n_groups}; file lines: {len(lines)}")


if __name__ == "__main__":
    main()
