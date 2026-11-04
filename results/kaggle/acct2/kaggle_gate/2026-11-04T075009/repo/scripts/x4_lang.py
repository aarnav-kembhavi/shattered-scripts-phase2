"""X4 scoring pipeline for Bengali and Telugu (registered in RESULTS.md, Phase 2 pre-registration, X4), generalised from scripts/h_hindi.py (the Hindi replication of the Kannada design).

Language by environment: X4_LANG=bn | te. Forms native / ITRANS (lossless, `itrans_for` of the script) / lossy (`to_lossy`) on the Kannada item ids (sentiment 200 from IndicSentiment, SIB-200 1,004, M4c 500 rows with
the 496 retained by the Kannada mask) and natural (Gemini drafts, `scripts/x4_natural.py`) on the 257 SIB ids and the 496 M4c rows. Built so far: check, forward, score, tpw. NOT built yet (flagged): the per-language E9
lowercase-lossless form, the MDL assembly probe on Wikipedia words, the registered R1-R4 / ladder / K3b-bn,te analysis (the Hindi `gate` / `analyse` steps below are inherited and still Hindi-specific).
Usage: X4_LANG=bn python scripts/x4_lang.py check | forward [natural] | score [natural] | tpw
Outputs: results/phase2/x4/<lang>/ ; cache/activations/x4_<lang>/
"""
import json
import sys
import time
import unicodedata
from functools import lru_cache

import numpy as np
import pandas as pd

from shattered.llm.ratelimit import DailyQuotaExceeded
from shattered.runlog import REPO, commit, results_dir, tmp_path, write_json
from shattered.translit import to_lossy
from shattered.translit.natural import MODEL, defective, make_client, romanize
from shattered.translit.scheme import SCRIPTS, itrans_for

sys.path.insert(0, str(REPO / "scripts"))
import e0b_familiarity as e0b  # noqa: E402
import english_share as es  # noqa: E402
import l_ladder as lad  # noqa: E402
from m4b_mapping import ACT, boot, layer_fit  # noqa: E402
from m4c_natural_flores import SEED  # noqa: E402

import os  # noqa: E402

XL = os.environ.get("X4_LANG", "bn")
LANG, ISO = {"bn": ("ben_Beng", "bn"), "te": ("tel_Telu", "te")}[XL]
PROMPT_HI = f"natural_romanization_{XL}_v1"
MODELS = lad.ACC_MODELS  # all five
OUT = results_dir(f"phase2/x4/{XL}")
SCORES = OUT / "scores"
SCORE_DIRS = {"sentiment": SCORES / "sentiment", "sib": SCORES / "sib"}  # separate: string vs int ids
H_ACT = REPO / "cache" / "activations" / f"x4_{XL}"
DRAFTS = REPO / "data" / "processed" / f"natural_flores_{XL}_x4_v1.jsonl"
STATUS_NAT = REPO / "results" / "phase2" / "x4" / "natural" / f"status_{XL}.json"


class _Done:
    def exists(self) -> bool:
        return STATUS_NAT.exists() and bool(json.loads(STATUS_NAT.read_text(encoding="utf-8")).get("complete"))


DRAFTS_DONE = _Done()
RAW_HI = REPO / "data" / "raw" / "indicsentiment" / "data" / "test" / f"{ISO}.json"
FORMS = ["native", "itrans", "lossy"]
N_BOOT = 10000


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s.strip())


@lru_cache(maxsize=1)
def itrans_hi():
    return itrans_for(SCRIPTS[LANG])


def forms_of(t: str) -> dict:
    return {"native": t, "itrans": itrans_hi().encode(t), "lossy": to_lossy(t, LANG)}


@lru_cache(maxsize=1)
def flores_hi() -> list:
    from m14_full import flores_any
    return flores_any(LANG, "dev", "flores_plus", nfc=True) + flores_any(LANG, "devtest", "flores_plus", nfc=True)


def drafts() -> dict:
    return {f"flores-{r['index']}": r for r in map(json.loads, DRAFTS.open(encoding="utf-8"))} if DRAFTS.exists() else {}


def clean_natural() -> dict:
    """{key: natural text} for drafts that are clean (only after the drafts are complete)."""
    if not DRAFTS_DONE.exists():
        return {}
    return {k: r["natural"] for k, r in drafts().items() if not r["defective"]}


def m4c_rows() -> tuple[list, np.ndarray]:
    R, keep, _ = lad.m4c_sample()
    return [r["index"] for r in R], keep


def sentiment_items() -> list:
    rows = [json.loads(x) for x in open(RAW_HI, encoding="utf-8") if x.strip()]
    nat = clean_natural()
    out = []
    for kn in lad.e0b_items()["sentiment"]:
        r = rows[int(kn["id"].rsplit("-", 1)[1])]
        assert r["ENGLISH REVIEW"].strip() == kn["forms"]["english"]["text"] and int(r["LABEL"] == "Positive") == kn["label"]
        it = {"task": "sentiment", "id": kn["id"], "label": kn["label"],
              "forms": {"english": kn["forms"]["english"], **{f: {"text": v} for f, v in forms_of(nfc(r["INDIC REVIEW"])).items()}}}
        if kn["id"] in nat:
            it["forms"]["natural"] = {"text": nat[kn["id"]]}
        it["natural_defective"] = kn["id"] not in nat  # here: no clean Hindi natural (skipped for that form)
        out.append(it)
    return out


def sib_items() -> list:
    from e0c_sib import CATS, sib
    S, K = sib(LANG), sib("kan_Knda")
    assert (S.index_id.values == K.index_id.values).all() and (S.category.values == K.category.values).all()
    F, nat = flores_hi(), clean_natural()
    overlap = {it["id"] for it in lad.sib257_items()["sib"]}
    from m14_full import flores_forms
    en = flores_forms()["english"]
    out = []
    for i, c in zip(S.index_id, S.category):
        i = int(i)
        it = {"id": i, "label": CATS.index(c), "forms": {"english": {"text": en[i]},
                                                          **{f: {"text": v} for f, v in forms_of(F[i]).items()}}}
        key = f"flores-{i}"
        if i in overlap and key in nat:
            it["forms"]["natural"] = {"text": nat[key]}
        it["natural_defective"] = not (i in overlap and key in nat)
        out.append(it)
    return out


# ---------------------------------------------------------------- check / draft

def do_check() -> int:
    from e0c_sib import sib
    F = flores_hi()
    checks = {"flores_hi_2009": len(F) == 2009}
    rows = [json.loads(x) for x in open(RAW_HI, encoding="utf-8") if x.strip()]
    kn = [json.loads(x) for x in open(RAW_HI.with_name("kn.json"), encoding="utf-8") if x.strip()]
    checks["sentiment_rows_aligned"] = len(rows) == len(kn) == 1000 and all(
        a["ENGLISH REVIEW"] == b["ENGLISH REVIEW"] and a.get("LABEL") == b.get("LABEL") for a, b in zip(rows, kn))
    S, K = sib(LANG), sib("kan_Knda")
    checks["sib_ids_labels_aligned"] = len(S) == 1004 and bool((S.index_id.values == K.index_id.values).all()
                                                              and (S.category.values == K.category.values).all())
    H = itrans_hi()
    checks["itrans_lossless_flores"] = all(H.decode(H.encode(s)) == s for s in F)
    checks["itrans_lossless_sentiment"] = all(H.decode(H.encode(nfc(r["INDIC REVIEW"]))) == nfc(r["INDIC REVIEW"])
                                              for r in rows)
    try:
        s = sentiment_items()
        checks["sentiment_items_200"] = len(s) == 200
    except AssertionError:
        checks["sentiment_items_200"] = False
    ids, keep = m4c_rows()
    checks["m4c_rows_500_retained_496"] = len(ids) == 500 and int(keep.sum()) == 496
    write_json(OUT / "data_check.json", checks, {"registered": "RESULTS.md X4"})
    print(checks, flush=True)
    return 0 if all(checks.values()) else 1


def draft_targets() -> list:
    ids, keep = m4c_rows()
    F = flores_hi()
    rows = [json.loads(x) for x in open(RAW_HI, encoding="utf-8") if x.strip()]
    out = [(f"flores-{i}", F[i]) for i, k in zip(ids, keep) if k]
    out += [(it["id"], nfc(rows[int(it["id"].rsplit("-", 1)[1])]["INDIC REVIEW"])) for it in lad.e0b_items()["sentiment"]]
    return out


def do_draft() -> int:
    client = make_client()
    done, stopped = drafts(), None
    targets = draft_targets()
    for key, native in targets:
        if key in done and not done[key]["defective"]:
            continue
        start = done[key]["attempt"] + 1 if key in done else 1
        for attempt in range(start, 4):
            try:
                r = romanize(client, native, version=PROMPT_HI, attempt=attempt)
            except DailyQuotaExceeded as e:
                stopped = str(e)[:200]
                break
            row = {"key": key, "native": native, "natural": r["natural"], "attempt": attempt, "prompt": PROMPT_HI,
                   "model": MODEL, "finish_reason": r["finish_reason"]}
            row["defective"] = defective(row)
            done[key] = row
            if not row["defective"]:
                break
        if stopped:
            break
    with tmp_path(DRAFTS).open("w", encoding="utf-8") as f:
        for k in sorted(done):
            f.write(json.dumps(done[k], ensure_ascii=False) + "\n")
    commit(tmp_path(DRAFTS), DRAFTS)
    complete = stopped is None and all(k in done for k, _ in targets) and all(
        not done[k]["defective"] or done[k]["attempt"] >= 3 for k, _ in targets)
    summary = {"n_done": len(done), "n_target": len(targets), "n_defective_after_retries":
               sum(done[k]["defective"] for k, _ in targets if k in done), "stopped": stopped, "complete": complete}
    print(summary, flush=True)
    if complete:
        write_json(DRAFTS_DONE, summary, {"prompt": PROMPT_HI, "model": MODEL})
    return 0 if complete else 3


# ---------------------------------------------------------------- GPU steps

def kn_layers(m: str) -> int | None:
    p = ACT / m / "native.npz"
    return int(np.load(p)["flores_states"].shape[1]) if p.exists() else None


def do_forward(natural: bool) -> int:
    import torch
    from shattered.interp.load import load
    from m14_full import flores_forms
    ids, keep = m4c_rows()
    F, en = flores_hi(), flores_forms()["english"]
    texts = {f: [forms_of(F[i])[f] for i in ids] for f in FORMS}
    rid = {f: list(ids) for f in FORMS}
    if natural:
        nat = clean_natural()
        assert nat, "natural drafts are not complete"
        rid["natural"] = [i for i in ids if f"flores-{i}" in nat]
        texts["natural"] = [nat[f"flores-{i}"] for i in rid["natural"]]
    for m in MODELS:
        need = {f: texts[f] for f in texts if not (H_ACT / m / f"{f}500.npz").exists()}
        if m not in lad.M4_MODELS and not (H_ACT / m / "english500.npz").exists():
            need["english"], rid["english"] = [en[i] for i in ids], list(ids)
        if not need:
            continue
        t0 = time.time()
        model, tok = load(m, "cuda")
        for f, T in need.items():
            out = lad.forward_form(model, tok, T, rid[f])
            X = out["sent_states"]
            L = kn_layers(m)
            if np.isnan(X.astype(np.float32)).any() or (L is not None and X.shape[1] != L) or len(X) != len(T):
                print(f"CHECK FAILED: {m}/{f} vectors shape {X.shape}, Kannada layers {L}", flush=True)
                return 1
            path = H_ACT / m / f"{f}500.npz"
            path.parent.mkdir(parents=True, exist_ok=True)
            np.savez(tmp_path(path), flores_states=X, index=np.array(rid[f]), n_tokens=out["n_tokens"])
            commit(tmp_path(path), path)
            print(f"{m}: hindi {f}500 forward done ({time.time() - t0:.0f}s since load)", flush=True)
        del model
        torch.cuda.empty_cache()
    return 0


def do_score(natural: bool) -> int:
    items = {"sentiment": sentiment_items(), "sib": sib_items()}
    forms = ["natural"] if natural else FORMS
    if natural:
        assert DRAFTS_DONE.exists(), "natural drafts are not complete"
    for m in MODELS:
        for t, d in SCORE_DIRS.items():
            d.mkdir(parents=True, exist_ok=True)
            e0b.score_model(m, {t: items[t]}, forms, d)
            for f in forms:
                x = pd.read_parquet(d / f"{m}__{f}.parquet")
                want = sum(not (f == "natural" and it["natural_defective"]) for it in items[t])
                if len(x) != want or x.logprobs.map(lambda v: np.isnan(np.asarray(v)).any()).any():
                    print(f"CHECK FAILED: {m}/{t}/{f} has {len(x)} rows (expected {want}) or NaN log-probs", flush=True)
                    return 1
    return 0


# ---------------------------------------------------------------- CPU steps

def do_tpw() -> None:
    from transformers import AutoTokenizer
    from shattered.interp.load import MODELS as REPOS
    ids, keep = m4c_rows()
    F, nat = flores_hi(), clean_natural()
    m4c = {f: [forms_of(F[i])[f] for i, k in zip(ids, keep) if k] for f in FORMS}
    if nat:
        m4c["natural"] = [nat[f"flores-{i}"] for i, k in zip(ids, keep) if k and f"flores-{i}" in nat]
    s, b = sentiment_items(), sib_items()
    sets = {"m4c496": m4c,
            "sentiment": {f: [it["forms"][f]["text"] for it in s if f in it["forms"]] for f in FORMS + ["natural"]},
            "sib": {f: [it["forms"][f]["text"] for it in b] for f in FORMS}}
    if nat:
        sets["sib257"] = {"natural": [it["forms"]["natural"]["text"] for it in b if "natural" in it["forms"]]}
    rows = []
    for m in MODELS:
        tok = AutoTokenizer.from_pretrained(REPOS[m])
        for d, fs in sets.items():
            for f, T in fs.items():
                if not T:
                    continue
                n = sum(len(x) for x in tok(T, add_special_tokens=False)["input_ids"])
                rows.append({"language": "hindi", "model": m, "dataset": d, "form": f, "n_texts": len(T),
                             "tokens_per_word": n / sum(len(x.split()) for x in T)})
    pd.DataFrame(rows).to_csv(OUT / "tokens_per_word.csv", index=False)
    print(pd.DataFrame(rows).pivot_table(index=["model", "dataset"], columns="form", values="tokens_per_word")
          .round(2).to_string(), flush=True)


def calibrated(lang: str, forms: list[str]) -> pd.DataFrame:
    """Per-item calibrated predictions; the raw fallback is decided on the Kannada-run English rows (same items)."""
    frames = []
    for d, tasks in ((lad.E0B_DIR, ("sentiment",)), (lad.E0C_DIR, ("sib",))):
        eng = pd.concat([pd.read_parquet(d / f"{m}__english.parquet") for m in MODELS])
        eng = eng[eng.task.isin(tasks)]
        if lang == "kannada":
            src = pd.concat([pd.read_parquet(d / f"{m}__{f}.parquet") for m in MODELS for f in forms
                             if (d / f"{m}__{f}.parquet").exists()])
            cf = {m: json.load(open(d / f"cf_{m}.json")) for m in MODELS}
        else:
            h = SCORE_DIRS[tasks[0]]
            src = pd.concat([pd.read_parquet(h / f"{m}__{f}.parquet") for m in MODELS for f in forms
                             if (h / f"{m}__{f}.parquet").exists()])
            cf = {m: json.load(open(h / f"cf_{m}.json")) for m in MODELS}
        src = src[src.task.isin(tasks)]
        D, _ = e0b.apply_calibration(pd.concat([eng, src], ignore_index=True), cf)
        frames.append(D[D.form != "english"])
    D = pd.concat(frames, ignore_index=True)
    D["correct"] = D.pred_cal == D.label
    return D


def retrieval_split(ids_d: list):
    """The M4c split (seed SEED over the 496 retained rows) restricted to the item list ids_d (in retained order)."""
    ids, keep = m4c_rows()
    kept = [i for i, k in zip(ids, keep) if k]
    n = len(kept)
    order = np.random.default_rng(SEED).permutation(n)
    tr, te = np.sort(order[: n // 2]), np.sort(order[n // 2:])
    folds = np.array_split(np.random.default_rng(SEED + 2).permutation(tr), 5)
    pos = {i: p for p, i in enumerate(ids_d)}
    to = lambda a: np.array([pos[kept[j]] for j in a if kept[j] in pos], dtype=int)  # noqa: E731
    return to(tr), to(te), [to(f) for f in folds]


def vectors(m: str, lang: str, form: str, ids_d: list) -> np.ndarray:
    if lang == "kannada":
        if form in ("native", "itrans", "english"):
            return np.load(ACT / m / f"{form}.npz")["flores_states"][ids_d]
        z = np.load(ACT / m / f"{form}500.npz")
    else:
        z = np.load(H_ACT / m / f"{form}500.npz")
    where = {int(i): k for k, i in enumerate(z["index"])}
    return z["flores_states"][[where[i] for i in ids_d]]


def retrieval_hits(m: str, lang: str, form: str, ids_d: list) -> np.ndarray:
    tr, te, folds = retrieval_split(ids_d)
    E = (vectors(m, "kannada", "english", ids_d) if m in lad.M4_MODELS
         else vectors(m, "hindi", "english", ids_d))
    X = vectors(m, lang, form, ids_d)
    fits = [layer_fit(X[:, l], E[:, l], tr, te, folds) for l in range(X.shape[1])]
    return fits[int(np.argmax([r["unmapped_train"] for r in fits]))]["unmapped"]


def do_gate() -> int:
    D = calibrated("hindi", ["native"])
    ids, keep = m4c_rows()
    kept = [i for i, k in zip(ids, keep) if k]
    out = {}
    for m in MODELS:
        g = {}
        for t, chance in (("sentiment", 0.5), ("sib", 1 / 7)):
            c = D[(D.model == m) & (D.task == t)].correct.to_numpy(float)
            lo, hi = e0b.bootstrap_ci(c)
            g[t] = {"n": len(c), "acc": c.mean(), "ci": [lo, hi], "chance": chance, "above_chance": lo > chance}
        hits = retrieval_hits(m, "hindi", "native", kept)
        g["retrieval"] = {"n_test": len(hits), "unmapped_test": float(hits.mean()), "ci": boot(hits)}
        g["counts_accuracy"] = bool(g["sentiment"]["above_chance"] and g["sib"]["above_chance"])
        g["counts_retrieval"] = bool(g["retrieval"]["unmapped_test"] > 0.5)
        g["counted_h1_accuracy"] = g["counts_accuracy"] and m in lad.COUNT_ACC
        g["counted_h1_retrieval"] = g["counts_retrieval"] and m in lad.COUNT_RETRIEVAL
        out[m] = g
    write_json(OUT / "gate.json", out, {"registered": "RESULTS.md 2026-10-23 (H-Hindi)", "rule": "fixed before data"})
    for m, g in out.items():
        print(m, {k: (round(v["acc"], 3), [round(x, 3) for x in v["ci"]]) for k, v in g.items()
                  if k in ("sentiment", "sib")}, "retrieval", round(g["retrieval"]["unmapped_test"], 3),
              "| counts acc", g["counts_accuracy"], "ret", g["counts_retrieval"], flush=True)
    return 0


def paired_stat(d: np.ndarray) -> dict:
    rng = np.random.default_rng(0)
    bs = d[rng.integers(0, len(d), (N_BOOT, len(d)))].mean(1)
    p = max(2 * min((bs <= 0).mean(), (bs >= 0).mean()), 1 / N_BOOT)
    return {"n": len(d), "diff_of_gaps": float(d.mean()), "ci": [float(x) for x in np.percentile(bs, [2.5, 97.5])],
            "p": float(min(p, 1.0))}


def do_analyse() -> int:
    gate = json.load(open(OUT / "gate.json"))
    del gate["provenance"]
    nat = clean_natural()
    missing = [m for m in MODELS if (gate[m]["counted_h1_accuracy"] or gate[m]["counted_h1_retrieval"])
               and not (all((d / f"{m}__natural.parquet").exists() for d in SCORE_DIRS.values())
                        and (H_ACT / m / "natural500.npz").exists())]
    if not nat or missing:
        print({"refused": "natural Hindi not complete for every counted model", "missing": missing}, flush=True)
        return 2
    ids, keep = m4c_rows()
    D_ret = [i for i, k in zip(ids, keep) if k and f"flores-{i}" in nat]
    K, H = calibrated("kannada", ["native", "itrans", "natural", "natural257"]), calibrated("hindi", FORMS + ["natural"])
    R = h1_table(gate, K, H, D_ret, None, check_ladder=len(D_ret) == int(keep.sum()))
    R[R.comparison == "native-natural"].to_csv(OUT / "h1.csv", index=False)
    R[R.comparison == "native-itrans"].to_csv(OUT / "exploratory_itrans.csv", index=False)
    verdict = h1_rule(R)
    write_json(OUT / "h1_verdict.json", verdict, {"registered": "RESULTS.md 2026-10-23 (H-Hindi + 12:05 addendum)",
                                                   "n_retrieval_items_D": len(D_ret)})
    # secondary (addendum item 3, no separate verdict): English-word share and loan-free H1
    wl = es.wordlists()["zipf>=3"]
    texts = natural_pairs(nat)
    ids_by = {"retrieval": D_ret, "sentiment": R.attrs["ids"]["sentiment"], "sib": R.attrs["ids"]["sib"]}
    key = lambda t, i: ("sentiment", i) if t == "sentiment" else ("m4c", int(i))  # noqa: E731
    share, loan_free = {}, {}
    for t, its in ids_by.items():
        e = np.array([[en_count(texts[key(t, i)][lg], wl) for lg in (0, 1)] for i in its], dtype=float)  # (n, lang, 2)
        sh = e[:, :, 0] / np.maximum(e[:, :, 1], 1)
        d = sh[:, 1] - sh[:, 0]
        bs = d[np.random.default_rng(0).integers(0, len(d), (N_BOOT, len(d)))].mean(1)
        free = (e[:, 0, 0] == 0) & (e[:, 1, 0] == 0)
        share[t] = {"n": len(d), "kannada_share": float(sh[:, 0].mean()), "hindi_share": float(sh[:, 1].mean()),
                    "hindi_minus_kannada": float(d.mean()), "ci": [float(x) for x in np.percentile(bs, [2.5, 97.5])],
                    "n_english_free_both": int(free.sum())}
        loan_free[t] = {i for i, f in zip(its, free) if f}
    L = h1_table(gate, K, H, [i for i in D_ret if i in loan_free["retrieval"]], loan_free, check_ladder=False)
    L[L.comparison == "native-natural"].to_csv(OUT / "h1_loanfree.csv", index=False)
    lf = h1_rule(L)
    for t in lf:
        lf[t]["rule_outcome_descriptive"] = lf[t].pop("verdict")
        lf[t]["flag"] = ("possibly driven by English loans" if verdict[t]["verdict"].startswith("effect")
                         and not lf[t]["rule_outcome_descriptive"].startswith("effect") else None)
    write_json(OUT / "h1_secondary.json", {"english_word_share": share, "loan_free_h1": lf},
               {"registered": "RESULTS.md 2026-10-23 12:05 addendum, item 3", "status": "secondary, no separate verdict",
                "wordlist": "wordfreq en best, Zipf >= 3, words longer than 3 characters, lowercased"})
    print("H1 analysis and secondary written", flush=True)
    return 0


def en_count(text: str, wl: set) -> tuple[int, int]:
    """(English words, words): lowercased `english_share.words()`, longer than 3 characters, Zipf >= 3 list."""
    w = [x.lower() for x in es.words(text)]
    return sum(len(x) > 3 and x in wl for x in w), len(w)


def natural_pairs(nat: dict) -> dict:
    """{("sentiment", id) | ("m4c", index): (Kannada natural, Hindi natural)} for items clean in both languages."""
    out = {}
    for it in lad.e0b_items()["sentiment"]:
        if not it["natural_defective"] and it["id"] in nat:
            out[("sentiment", it["id"])] = (it["forms"]["natural"]["text"], nat[it["id"]])
    R, keep, _ = lad.m4c_sample()
    for r, k in zip(R, keep):
        if k and f"flores-{r['index']}" in nat:
            out[("m4c", int(r["index"]))] = (r["natural"], nat[f"flores-{r['index']}"])
    return out


def h1_table(gate: dict, K: pd.DataFrame, H: pd.DataFrame, D_ret: list, restrict: dict | None,
             check_ladder: bool) -> pd.DataFrame:
    """H1 and exploratory rows per model; `restrict` limits the sentiment/SIB ids (loan-free secondary)."""
    from statsmodels.stats.multitest import multipletests
    lad_ret = pd.read_csv(REPO / "results/l_ladder/retrieval.csv").set_index(["model", "form"])
    rows, used = [], {}
    for m in MODELS:
        # retrieval (models with Kannada retrieval only)
        if m in lad.M4_MODELS:
            h = {(lang, f): retrieval_hits(m, lang, f, D_ret) for lang in ("kannada", "hindi")
                 for f in ("native", "natural", "itrans")}
            if check_ladder:  # no Hindi defect: Kannada must reproduce the ladder
                for f in ("native", "natural", "itrans"):
                    assert np.isclose(h[("kannada", f)].mean(), lad_ret.loc[(m, f), "unmapped_test"]), (m, f)
            for comp in ("natural", "itrans"):
                d = ((h[("kannada", "native")].astype(float) - h[("kannada", comp)])
                     - (h[("hindi", "native")].astype(float) - h[("hindi", comp)]))
                rows.append({"measure": "retrieval", "comparison": f"native-{comp}", "model": m,
                             "counted": gate[m]["counted_h1_retrieval"],
                             "kannada_native": h[("kannada", "native")].mean(), "kannada_other": h[("kannada", comp)].mean(),
                             "hindi_native": h[("hindi", "native")].mean(), "hindi_other": h[("hindi", comp)].mean(),
                             **paired_stat(d)})
        for t, kn_nat in (("sentiment", "natural"), ("sib", "natural257")):
            k = K[(K.model == m) & (K.task == t)].pivot_table(index="id", columns="form", values="correct")
            hh = H[(H.model == m) & (H.task == t)].pivot_table(index="id", columns="form", values="correct")
            ok = k.index[k[kn_nat].notna()].intersection(hh.index[hh["natural"].notna()])
            if restrict is not None:
                ok = ok[ok.isin(list(restrict[t]))]
            used[t] = list(ok)
            for comp, kc, hc in (("natural", kn_nat, "natural"), ("itrans", "itrans", "itrans")):
                a, b = k.loc[ok], hh.loc[ok]
                d = (a["native"].astype(float) - a[kc]) - (b["native"].astype(float) - b[hc])
                rows.append({"measure": t, "comparison": f"native-{comp}", "model": m,
                             "counted": gate[m]["counted_h1_accuracy"], "kannada_native": a["native"].mean(),
                             "kannada_other": a[kc].mean(), "hindi_native": b["native"].mean(),
                             "hindi_other": b[hc].mean(), **paired_stat(d.to_numpy(float))})
    R = pd.DataFrame(rows)
    R["p_holm"] = np.nan
    for (s, c), g in R[R.counted].groupby(["measure", "comparison"]):
        R.loc[g.index, "p_holm"] = multipletests(g.p, method="holm")[1]
    R["positive"] = R.counted & (R.p_holm < 0.05) & (R.diff_of_gaps > 0)
    R["ci_holm_disagree"] = R.counted & (R.positive != [c[0] > 0 for c in R.ci])
    R.attrs["ids"] = used
    return R


def h1_rule(R: pd.DataFrame) -> dict:
    verdict = {}
    for s in ("retrieval", "sentiment", "sib"):
        g = R[(R.measure == s) & (R.comparison == "native-natural") & R.counted]
        n = len(g)
        need = (2 if s == "retrieval" else 3) if n == (3 if s == "retrieval" else 4) else max(n - 1, 2)
        pos = int(g.positive.sum())
        verdict[s] = {"n_counted": n, "needed": need, "n_positive": pos, "counted_models": g.model.tolist(),
                      "n_items": int(g.n.iloc[0]) if n else 0,
                      "verdict": "not testable" if n < 2 else ("effect (H1 supported)" if pos >= need else "refuted"),
                      "ci_holm_disagreements": g[g.ci_holm_disagree].model.tolist()}
    return verdict


if __name__ == "__main__":
    step, arg = sys.argv[1], sys.argv[2:]
    nat = "natural" in arg
    code = {"check": do_check, "draft": do_draft, "gate": do_gate, "analyse": do_analyse,
            "forward": lambda: do_forward(nat), "score": lambda: do_score(nat),
            "tpw": lambda: do_tpw() or 0}[step]()
    sys.exit(code or 0)
