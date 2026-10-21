"""Kanglish + natural-romanization human annotation (registered in RESULTS.md, 2026-10-16: K1-K3).

Items (500): the 200 E0 sentiment items (seed 0, as in E0/E0b) + 300 FLORES+ sentences drawn at random (seed 0) from
those in SIB-200 and in the M4b test half. 100 random items (seed 1) are marked for a second annotator.
Drafts (Gemini, gemini-3.5-flash-lite, temperature 0, cached): natural romanization with the existing prompt
natural_romanization_v1 (the E0 sentiment drafts are reused from data/processed/natural_e0_v1.jsonl), Kanglish with
kanglish_v1. Defective drafts (Indic script or new non-ASCII characters) get attempts 2-3, as for E0; a draft still
defective is shown to the annotators anyway (they correct it) and flagged.

Usage: python scripts/k_annotation.py select     # writes data/annotation/items_v1.jsonl (no API)
       python scripts/k_annotation.py plan       # counts uncached Gemini requests (no API)
       python scripts/k_annotation.py draft      # API; stops on the daily quota (exit 3), re-run to continue
       python scripts/k_annotation.py regen      # API; natural drafts still defective get attempts 4-5 (2026-10-22)
       python scripts/k_annotation.py blind      # writes data/annotation/blind_v1.json (40 blind items, seed 2)
       python scripts/k_annotation.py page       # writes annotation/annotate_v2.html (drafts embedded)
       python scripts/k_annotation.py agreement  # kappas on the double-annotated items
"""
import json
import sys

import numpy as np
import pandas as pd

from shattered.llm.cache import ResponseCache, request_key
from shattered.llm.ratelimit import DailyQuotaExceeded
from shattered.runlog import REPO, commit, results_dir, tmp_path, write_json
from shattered.translit.natural import MODEL, PROMPT_VERSION, TEMPLATE_DIR, defective, make_client, prompt, romanize

KANGLISH_VERSION = "kanglish_v1"
N_FLORES, N_DOUBLE = 300, 100
DIR = REPO / "data" / "annotation"
ITEMS, DRAFTS = DIR / "items_v1.jsonl", DIR / "drafts_v1.jsonl"
REGEN = DIR / "drafts_regen_v1.jsonl"  # natural drafts re-asked after attempt 3 (deviation, 2026-10-22)
MANUAL = DIR / "drafts_manual_v1.jsonl"  # drafts fixed by hand by Aarnav ({"id", "kind", "text"}); override all others
BLIND = DIR / "blind_v1.json"  # 40 of the 100 double items written from scratch by the second annotator (2026-10-22)
N_BLIND, BLIND_SEED = 40, 2
TEMPLATE = REPO / "annotation" / "template_v2.html"
PAGE = REPO / "annotation" / "annotate_v2.html"
ANN_DIR = REPO / "annotation" / "results"
PARAMS = {"max_tokens": 1024, "temperature": 0.0, "system": None}


def kanglish_prompt(text: str) -> str:
    return (TEMPLATE_DIR / f"{KANGLISH_VERSION}.txt").read_text(encoding="utf-8").format(text=text)


def do_select() -> None:
    from e0c_sib import sib
    from m14_full import flores_forms
    from shattered.data import tasks
    items = []
    for it in tasks.stratified_sample(tasks.load_task("sentiment"), 200, seed=0):
        items.append({"id": it["id"], "source": "sentiment", "label": it["label"],
                      "native": it["forms"]["native"]["text"], "english": it["forms"]["english"]["text"]})
    n = 2009
    te = np.sort(np.random.default_rng(0).permutation(n)[n // 2:])
    S = sib("kan_Knda")
    pool = np.sort(np.intersect1d(S.index_id.to_numpy(), te))
    pick = np.sort(np.random.default_rng(0).choice(pool, N_FLORES, replace=False))
    F, lab = flores_forms(), dict(zip(S.index_id, S.category))
    for i in pick:
        items.append({"id": f"flores-{i}", "source": "flores_sib", "flores_index": int(i), "sib_category": lab[i],
                      "native": F["native"][i], "english": F["english"][i]})
    dbl = set(np.random.default_rng(1).choice(len(items), N_DOUBLE, replace=False).tolist())
    for k, it in enumerate(items):
        it["double"] = k in dbl
    DIR.mkdir(parents=True, exist_ok=True)
    with tmp_path(ITEMS).open("w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    commit(tmp_path(ITEMS), ITEMS)
    print({"n_items": len(items), "n_flores_pool": len(pool), "n_double": len(dbl),
           "double_by_source": pd.Series([it["source"] for it in items if it["double"]]).value_counts().to_dict()})


def items() -> list:
    return [json.loads(x) for x in ITEMS.open(encoding="utf-8")]


def e0_natural() -> dict:
    return {r["native"]: r for r in map(json.loads, (REPO / "data/processed/natural_e0_v1.jsonl").open(encoding="utf-8"))}


def requests_needed() -> list:
    """(item id, kind, prompt) of the first attempt of every draft; E0 sentiment natural drafts already exist."""
    nat = e0_natural()
    out = []
    for it in items():
        if not (it["source"] == "sentiment" and it["native"] in nat):
            out.append((it["id"], "natural", prompt(it["native"], PROMPT_VERSION)))
        out.append((it["id"], "kanglish", kanglish_prompt(it["native"])))
    return out


def do_plan() -> None:
    cache = ResponseCache()
    req = requests_needed()
    todo = [r for r in req if cache.get(request_key("gemini", MODEL, r[2], PARAMS)) is None]
    by = pd.Series([k for _, k, _ in todo]).value_counts().to_dict()
    print({"first_attempt_requests": len(req), "uncached": len(todo), "uncached_by_kind": by})


def do_draft() -> int:
    client = make_client()
    nat = e0_natural()
    done = {(r["id"], r["kind"]): r for r in map(json.loads, DRAFTS.open(encoding="utf-8"))} if DRAFTS.exists() else {}
    stopped = None
    for it in items():
        for kind in ("natural", "kanglish"):
            key = (it["id"], kind)
            if kind == "natural" and it["source"] == "sentiment" and it["native"] in nat:
                r = nat[it["native"]]
                done[key] = {"id": it["id"], "kind": kind, "text": r["natural"], "attempt": r.get("attempt", 1),
                             "defective": defective(r), "source": "natural_e0_v1.jsonl"}
                continue
            if key in done and not done[key]["defective"]:
                continue
            start = done[key]["attempt"] + 1 if key in done else 1
            for attempt in range(start, 4):
                try:
                    if kind == "natural":
                        r = romanize(client, it["native"], attempt=attempt)
                        text = r["natural"]
                    else:
                        extra = {"attempt": attempt} if attempt > 1 else {}
                        text = client.generate(kanglish_prompt(it["native"]), max_tokens=1024, temperature=0.0,
                                               **extra).text.strip()
                except DailyQuotaExceeded as e:
                    stopped = str(e)[:200]
                    break
                bad = defective({"native": it["native"], "natural": text})
                done[key] = {"id": it["id"], "kind": kind, "text": text, "attempt": attempt, "defective": bad,
                             "prompt": PROMPT_VERSION if kind == "natural" else KANGLISH_VERSION, "model": MODEL}
                if not bad:
                    break
            if stopped:
                break
        if stopped:
            break
    with tmp_path(DRAFTS).open("w", encoding="utf-8") as f:
        for k in sorted(done):
            f.write(json.dumps(done[k], ensure_ascii=False) + "\n")
    commit(tmp_path(DRAFTS), DRAFTS)
    n_target = 2 * len(items())
    complete = len(done) == n_target and stopped is None
    print({"n_done": len(done), "n_target": n_target, "n_defective_after_retries":
           sum(r["defective"] for r in done.values()), "stopped": stopped, "complete": complete}, flush=True)
    return 0 if complete else 3


def do_regen(max_attempt: int = 5) -> int:
    """Deviation of 2026-10-22 (Aarnav): natural drafts still defective after attempts 1-3 get attempts 4..max_attempt
    (same model, prompt, temperature; only the cache key changes). Written to REGEN, never to DRAFTS or to the E0 file
    natural_e0_v1.jsonl (Gate 1 data); the page uses a regenerated draft only if it is clean."""
    client = make_client()
    its = {it["id"]: it for it in items()}
    done = {r["id"]: r for r in map(json.loads, REGEN.open(encoding="utf-8"))} if REGEN.exists() else {}
    bad = [r for r in map(json.loads, DRAFTS.open(encoding="utf-8")) if r["kind"] == "natural" and r["defective"]]
    stopped = None
    for r in bad:
        native = its[r["id"]]["native"]
        prev = done.get(r["id"])
        if prev and not prev["defective"]:
            continue
        for attempt in range(max(4, prev["attempt"] + 1 if prev else 4), max_attempt + 1):
            try:
                text = romanize(client, native, attempt=attempt)["natural"]
            except DailyQuotaExceeded as e:
                stopped = str(e)[:200]
                break
            d = defective({"native": native, "natural": text})
            done[r["id"]] = {"id": r["id"], "kind": "natural", "text": text, "attempt": attempt, "defective": d,
                             "prompt": PROMPT_VERSION, "model": MODEL, "replaces_attempt": r["attempt"]}
            if not d:
                break
        if stopped:
            break
    with tmp_path(REGEN).open("w", encoding="utf-8") as f:
        for k in sorted(done):
            f.write(json.dumps(done[k], ensure_ascii=False) + "\n")
    commit(tmp_path(REGEN), REGEN)
    still = sorted(k for k, v in done.items() if v["defective"])
    print({"n_regenerated": len(done), "clean": sorted(k for k, v in done.items() if not v["defective"]),
           "still_defective": still, "stopped": stopped}, flush=True)
    return 3 if stopped else 0


def do_blind() -> None:
    """Blind condition (registered 2026-10-22): N_BLIND of the double-annotated items, chosen with BLIND_SEED from the
    double items in items_v1.jsonl order. The second annotator sees only the native sentence for these."""
    dbl = [it["id"] for it in items() if it["double"]]
    pick = sorted(np.random.default_rng(BLIND_SEED).choice(len(dbl), N_BLIND, replace=False).tolist())
    ids = [dbl[i] for i in pick]
    tmp_path(BLIND).write_text(json.dumps({"seed": BLIND_SEED, "n": N_BLIND, "n_double": len(dbl),
                                           "rule": "numpy default_rng(seed).choice(n_double, n, replace=False) over "
                                                   "the double items in items_v1.jsonl order",
                                           "ids": ids}, indent=1), encoding="utf-8")
    commit(tmp_path(BLIND), BLIND)
    print({"blind": len(ids), "sentiment": sum(i.startswith("indicsentiment") for i in ids),
           "flores": sum(i.startswith("flores") for i in ids)})


def do_page() -> None:
    drafts = {}
    if DRAFTS.exists():
        drafts = {(r["id"], r["kind"]): r for r in map(json.loads, DRAFTS.open(encoding="utf-8"))}
    if REGEN.exists():  # clean regenerated natural drafts replace defective ones (deviation of 2026-10-22)
        for r in map(json.loads, REGEN.open(encoding="utf-8")):
            if not r["defective"]:
                drafts[(r["id"], "natural")] = r
    if MANUAL.exists():  # Aarnav's hand fixes override every Gemini draft
        for r in map(json.loads, MANUAL.open(encoding="utf-8")):
            drafts[(r["id"], r["kind"])] = {**r, "defective": False, "source": "manual"}
    blind = set(json.load(open(BLIND))["ids"]) if BLIND.exists() else set()
    rows = []
    for it in items():
        d = {k: drafts.get((it["id"], k)) for k in ("natural", "kanglish")}
        rows.append({"id": it["id"], "source": it["source"], "double": it["double"], "blind": it["id"] in blind,
                     "native": it["native"],
                     "english": it["english"],
                     **{f"{k}_draft": (v["text"] if v else "") for k, v in d.items()},
                     **{f"{k}_flag": bool(v and v["defective"]) for k, v in d.items()}})
    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("__ITEMS_JSON__", json.dumps(rows, ensure_ascii=False).replace("</", "<\\/"))
    PAGE.write_text(html, encoding="utf-8")
    print({"page": str(PAGE), "n_items": len(rows), "n_blind": sum(r["blind"] for r in rows),
           "flagged": [r["id"] for r in rows if r["natural_flag"] or r["kanglish_flag"]], "n_missing_drafts": sum(not r["natural_draft"] or
                                                                             not r["kanglish_draft"] for r in rows)})


def chrf_stats(hyp: pd.Series, ref: pd.Series, n_boot: int = 10000) -> dict:
    """Mean sentence chrF (sacrebleu chrF: char order 6, word order 0, beta 2) with a bootstrap CI over items."""
    from sacrebleu.metrics import CHRF
    m = CHRF(char_order=6, word_order=0, beta=2)
    s = np.array([m.sentence_score(str(h) if pd.notna(h) else "", [str(r) if pd.notna(r) else ""]).score
                  for h, r in zip(hyp, ref)])
    rng = np.random.default_rng(0)
    bs = s[rng.integers(0, len(s), (n_boot, len(s)))].mean(1)
    return {"mean": float(s.mean()), "ci": [float(v) for v in np.percentile(bs, [2.5, 97.5])], "n": int(len(s))}


def do_agreement() -> None:
    from sklearn.metrics import cohen_kappa_score
    files = sorted(ANN_DIR.glob("*.csv"))
    A = {f.stem: pd.read_csv(f, encoding="utf-8-sig").drop_duplicates("item_id", keep="last").set_index("item_id") for f in files}
    blind = set(json.load(open(BLIND))["ids"]) if BLIND.exists() else set()
    # 2026-10-22: the second annotator writes the blind items from scratch (no drafts, no ratings), so rating and
    # correction agreement is computed on the other double items (60); the blind items are analysed for K3.
    dbl = [it["id"] for it in items() if it["double"] and it["id"] not in blind]
    full = [a for a, d in A.items() if set(dbl) <= set(d.index)]
    if len(full) < 2:
        print({"status": f"waiting: fewer than two annotators have finished the {len(dbl)} non-blind double items",
               "progress": {a: int(len(set(dbl) & set(d.index))) for a, d in A.items()}})
        return
    a, b = full[:2]
    x, y = A[a].loc[dbl], A[b].loc[dbl]
    out = {"annotators": [a, b], "n_items": len(dbl)}
    for k in ("natural", "kanglish"):
        out[f"{k}_meaning_cohen_kappa"] = float(cohen_kappa_score(x[f"{k}_meaning"], y[f"{k}_meaning"]))
        out[f"{k}_naturalness_weighted_kappa_quadratic"] = float(cohen_kappa_score(
            x[f"{k}_naturalness"], y[f"{k}_naturalness"], weights="quadratic"))
        out[f"{k}_meaning_raw_agreement"] = float((x[f"{k}_meaning"] == y[f"{k}_meaning"]).mean())
        # addendum 2026-10-17: agreement on corrections, and how much each annotator edited the Gemini draft
        out[f"{k}_corrections_chrf"] = chrf_stats(x[f"{k}_corrected"], y[f"{k}_corrected"])
        for who, d in ((a, x), (b, y)):
            out[f"{k}_draft_vs_correction_chrf_{who}"] = chrf_stats(d[f"{k}_draft"], d[f"{k}_corrected"])
    write_json(results_dir("k_annotation") / "agreement.json", out, {"items": str(ITEMS), "files": [str(f) for f in files]})
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    sys.path.insert(0, str(REPO / "scripts"))
    step = sys.argv[1]
    if step == "regen":
        sys.exit(do_regen())
    if step == "draft":
        sys.exit(do_draft())
    {"select": do_select, "plan": do_plan, "blind": do_blind, "page": do_page, "agreement": do_agreement}[step]()
