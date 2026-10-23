"""H1-LF: H1 at equal English-loan content (pre-registered in RESULTS.md, 2026-10-23 15:44 IST, a follow-up registered
after the H1 results; this script was written after that registration).

Usage: python scripts/h1lf.py opt2      (CPU: intercept of d_i on English-share difference; sensitivity a, b)
       python scripts/h1lf.py itrans    (CPU: English share of Hindi vs Kannada ITRANS on the H1 item sets)
       python scripts/h1lf.py draft     (API: natural drafts for all 1,004 SIB items, both languages; exit 3 on a quota
                                         stop, re-run to continue)
       python scripts/h1lf.py score <model> <kannada|hindi>  (GPU: one counted model x language on natural SIB
                                              1,004; one process per load so the chain checks the GPU before each)
       python scripts/h1lf.py score check    (CPU: row counts and the reproduction check over all four models)
       python scripts/h1lf.py analyse1  (CPU: H1 on the loan-free subset of the 1,004)
Outputs: results/h1lf/{opt2.csv, opt2_verdict.json, opt2_sensitivity.csv, opt2_tertiles.csv, itrans_share.json,
         scores/{kannada,hindi}/, sib1004_drafts.DONE, opt1.csv, opt1_verdict.json};
         data/processed/natural_sib1004_{kn,hi}_v1.jsonl
"""
import json
import sys

import numpy as np
import pandas as pd

from shattered.llm.ratelimit import DailyQuotaExceeded
from shattered.runlog import REPO, commit, results_dir, tmp_path, write_json
from shattered.translit.natural import MODEL, PROMPT_VERSION, defective, make_client, romanize

sys.path.insert(0, str(REPO / "scripts"))
import e0b_familiarity as e0b  # noqa: E402
import english_share as es  # noqa: E402
import h_hindi as hh  # noqa: E402
import l_ladder as lad  # noqa: E402
from m4b_mapping import layer_fit  # noqa: E402

OUT = results_dir("h1lf")
N_BOOT = 10000
FORM1 = "natural1004"
LANGS = {"kannada": ("kn", PROMPT_VERSION), "hindi": ("hi", hh.PROMPT_HI)}
DRAFTS = {lg: REPO / "data" / "processed" / f"natural_sib1004_{c}_v1.jsonl" for lg, (c, _) in LANGS.items()}
DONE = OUT / "sib1004_drafts.DONE"
SCORE1 = {lg: OUT / "scores" / lg for lg in LANGS}


# ---------------------------------------------------------------- shared

def boot_idx(n: int) -> np.ndarray:
    return np.random.default_rng(0).integers(0, n, (N_BOOT, n))


def boot_p(bs: np.ndarray) -> float:
    return float(min(max(2 * min((bs <= 0).mean(), (bs >= 0).mean()), 1 / N_BOOT), 1.0))


def scored(dirs: dict, forms: list[str]) -> pd.DataFrame:
    """Per-item calibrated predictions and gold margins. dirs: {task: score dir}; the raw fallback is decided on the
    Kannada-run English rows (same items), as in H1."""
    frames = []
    for t, d in dirs.items():
        e = lad.E0B_DIR if t == "sentiment" else lad.E0C_DIR
        eng = pd.concat([pd.read_parquet(e / f"{m}__english.parquet") for m in hh.MODELS])
        eng = eng[eng.task == t]
        src = pd.concat([pd.read_parquet(d / f"{m}__{f}.parquet") for m in hh.MODELS for f in forms
                         if (d / f"{m}__{f}.parquet").exists()])
        src = src[src.task == t]
        cf = {m: json.load(open(d / f"cf_{m}.json")) for m in hh.MODELS if (d / f"cf_{m}.json").exists()}
        D, fb = e0b.apply_calibration(pd.concat([eng, src], ignore_index=True), cf)
        use_raw = {(r.model, r.task) for r in fb.itertuples() if r.use_raw}
        D = D[D.form != "english"].copy()
        s = [np.asarray(lp) if (m, t) in use_raw else
             np.asarray(lp) - np.mean([cf[m][i][t] for i in e0b.CONTENT_FREE], axis=0)
             for lp, m in zip(D.logprobs, D.model)]
        D["margin"] = [x[y] - np.delete(x, y).max() for x, y in zip(s, D.label)]
        assert (np.array([int(np.argmax(x)) for x in s]) == D.pred_cal.to_numpy()).all()
        frames.append(D)
    D = pd.concat(frames, ignore_index=True)
    D["correct"] = (D.pred_cal == D.label).astype(float)
    return D


def share(text: str, wl: set) -> float:
    e, n = hh.en_count(text, wl)
    return e / max(n, 1)


# ---------------------------------------------------------------- option 2

def retrieval_outcomes(m: str, lang: str, form: str, ids_d: list) -> tuple[np.ndarray, np.ndarray]:
    """(hit, margin) on the test half at the train-half best layer, same split and centering as H1."""
    tr, te, folds = hh.retrieval_split(ids_d)
    E = (hh.vectors(m, "kannada", "english", ids_d) if m in lad.M4_MODELS
         else hh.vectors(m, "hindi", "english", ids_d))
    X = hh.vectors(m, lang, form, ids_d)
    fits = [layer_fit(X[:, l], E[:, l], tr, te, folds) for l in range(X.shape[1])]
    best = int(np.argmax([r["unmapped_train"] for r in fits]))
    x, y = X[:, best].astype(np.float64), E[:, best].astype(np.float64)
    P, Y = x[te] - x[tr].mean(0), y[te] - y[tr].mean(0)
    P /= np.linalg.norm(P, axis=1, keepdims=True) + 1e-8
    Y /= np.linalg.norm(Y, axis=1, keepdims=True) + 1e-8
    S = P @ Y.T
    diag = np.diag(S).copy()
    np.fill_diagonal(S, -np.inf)
    return fits[best]["unmapped"].astype(float), diag - S.max(1)


def regress(d: np.ndarray, x: np.ndarray) -> dict:
    def ab(D, X):
        mx, md = X.mean(-1, keepdims=True), D.mean(-1, keepdims=True)
        vx = ((X - mx) ** 2).mean(-1)
        b = np.where(vx > 0, ((X - mx) * (D - md)).mean(-1) / np.where(vx > 0, vx, 1), np.nan)
        return md[..., 0] - b * mx[..., 0], b
    a, b = ab(d, x)
    idx = boot_idx(len(d))
    ba, bb = ab(d[idx], x[idx])
    return {"n": len(d), "intercept": float(a), "intercept_ci": [float(v) for v in np.nanpercentile(ba, [2.5, 97.5])],
            "p": boot_p(ba[np.isfinite(ba)]), "slope": float(b),
            "slope_ci": [float(v) for v in np.nanpercentile(bb, [2.5, 97.5])],
            "mean_d": float(d.mean()), "mean_delta": float(x.mean()), "frac_delta_le_0": float((x <= 0).mean())}


def tertiles(d: np.ndarray, x: np.ndarray) -> list:
    r = pd.Series(x).rank(method="first").to_numpy()
    b = pd.qcut(r, 3, labels=False)
    out = []
    for k in range(3):
        v = d[b == k]
        bs = v[boot_idx(len(v))].mean(1)
        out.append({"tertile": k + 1, "n": len(v), "delta_min": float(x[b == k].min()), "delta_max": float(x[b == k].max()),
                    "mean_d": float(v.mean()), "ci": [float(q) for q in np.percentile(bs, [2.5, 97.5])]})
    return out


def opt2_items(nat: dict) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    ids, keep = hh.m4c_rows()
    D_ret = [i for i, k in zip(ids, keep) if k and f"flores-{i}" in nat]
    K = scored({"sentiment": lad.E0B_DIR, "sib": lad.E0C_DIR}, ["native", "itrans", "natural", "natural257"])
    H = scored(hh.SCORE_DIRS, hh.FORMS + ["natural"])
    return {"D_ret": D_ret}, K, H


def do_opt2() -> int:
    gate = json.load(open(hh.OUT / "gate.json"))
    del gate["provenance"]
    nat = hh.clean_natural()
    assert nat, "Hindi natural drafts incomplete"
    S, K, H = opt2_items(nat)
    D_ret = S["D_ret"]
    wl = es.wordlists()["zipf>=3"]
    texts = hh.natural_pairs(nat)
    delta = lambda key: share(texts[key][1], wl) - share(texts[key][0], wl)  # noqa: E731
    rows, sens, terts = [], [], []
    for m in hh.MODELS:
        per = {}
        if m in lad.M4_MODELS:
            _, te, _ = hh.retrieval_split(D_ret)
            o = {(lg, f): retrieval_outcomes(m, lg, f, D_ret) for lg in ("kannada", "hindi") for f in ("native", "natural")}
            x = np.array([delta(("m4c", D_ret[p])) for p in te])
            for k, name in ((0, "binary"), (1, "continuous")):
                d = (o[("kannada", "native")][k] - o[("kannada", "natural")][k]) - (o[("hindi", "native")][k] - o[("hindi", "natural")][k])
                per[("retrieval", name)] = (d, x)
            per[("retrieval", "counted")] = gate[m]["counted_h1_retrieval"]
        for t, kn_nat in (("sentiment", "natural"), ("sib", "natural257")):
            k = K[(K.model == m) & (K.task == t)]
            h = H[(H.model == m) & (H.task == t)]
            for name, col in (("binary", "correct"), ("continuous", "margin")):
                a = k.pivot_table(index="id", columns="form", values=col)
                b = h.pivot_table(index="id", columns="form", values=col)
                ok = a.index[a[kn_nat].notna()].intersection(b.index[b["natural"].notna()])
                d = (a.loc[ok, "native"] - a.loc[ok, kn_nat]) - (b.loc[ok, "native"] - b.loc[ok, "natural"])
                key = (lambda i: ("sentiment", i)) if t == "sentiment" else (lambda i: ("m4c", int(i)))
                per[(t, name)] = (d.to_numpy(float), np.array([delta(key(i)) for i in ok]))
            per[(t, "counted")] = gate[m]["counted_h1_accuracy"]
        for s in ("retrieval", "sentiment", "sib"):
            if (s, "binary") not in per:
                continue
            d, x = per[(s, "binary")]
            rows.append({"measure": s, "comparison": "native-natural", "model": m, "counted": per[(s, "counted")],
                         **regress(d, x)})
            sens.append({"measure": s, "model": m, "outcome": "continuous", **regress(*per[(s, "continuous")])})
            terts += [{"measure": s, "model": m, **r} for r in tertiles(d, x)]
    R = pd.DataFrame(rows)
    h1 = pd.read_csv(hh.OUT / "h1.csv").set_index(["measure", "model"])
    for r in R.itertuples():  # the binary d_i must reproduce the H1 statistic exactly
        assert r.n == h1.loc[(r.measure, r.model), "n"] and np.isclose(r.mean_d, h1.loc[(r.measure, r.model), "diff_of_gaps"]), r
    from statsmodels.stats.multitest import multipletests
    R["p_holm"] = np.nan
    for s, g in R[R.counted].groupby("measure"):
        R.loc[g.index, "p_holm"] = multipletests(g.p, method="holm")[1]
    R["positive"] = R.counted & (R.p_holm < 0.05) & (R.intercept > 0)
    R["ci_holm_disagree"] = R.counted & (R.positive != [c[0] > 0 for c in R.intercept_ci])
    R.to_csv(OUT / "opt2.csv", index=False)
    pd.DataFrame(sens).to_csv(OUT / "opt2_sensitivity.csv", index=False)
    pd.DataFrame(terts).to_csv(OUT / "opt2_tertiles.csv", index=False)
    v = hh.h1_rule(R)
    for s in v:
        v[s]["verdict"] = v[s]["verdict"].replace("effect (H1 supported)", "effect at equal English share")
    write_json(OUT / "opt2_verdict.json", v, {"registered": "RESULTS.md 2026-10-23 15:44 IST (H1-LF option 2, "
                                                            "follow-up registered post H1)"})
    print(json.dumps({s: (x["n_positive"], x["needed"], x["verdict"]) for s, x in v.items()}), flush=True)
    return 0


def do_itrans() -> int:
    nat = hh.clean_natural()
    S, K, H = opt2_items(nat)
    wl = es.wordlists()["zipf>=3"]
    from m14_full import flores_forms
    kn_fl, hi_fl = flores_forms()["itrans"], hh.flores_hi()
    kn_se = {it["id"]: it["forms"]["itrans"]["text"] for it in lad.e0b_items()["sentiment"]}
    hi_se = {it["id"]: it["forms"]["itrans"]["text"] for it in hh.sentiment_items()}
    hi_it = lambda i: hh.forms_of(hi_fl[i])["itrans"]  # noqa: E731
    _, te, _ = hh.retrieval_split(S["D_ret"])
    sets = {"retrieval": [("m4c", S["D_ret"][p]) for p in te]}
    for t, kn_nat in (("sentiment", "natural"), ("sib", "natural257")):
        k = K[(K.model == "sarvam-1") & (K.task == t)].pivot_table(index="id", columns="form", values="correct")
        h = H[(H.model == "sarvam-1") & (H.task == t)].pivot_table(index="id", columns="form", values="correct")
        ok = k.index[k[kn_nat].notna()].intersection(h.index[h["natural"].notna()])
        sets[t] = [(t if t == "sentiment" else "m4c", i) for i in ok]
    out = {}
    for s, keys in sets.items():
        kn = np.array([share(kn_se[i] if src == "sentiment" else kn_fl[int(i)], wl) for src, i in keys])
        hi = np.array([share(hi_se[i] if src == "sentiment" else hi_it(int(i)), wl) for src, i in keys])
        d = hi - kn
        bs = d[boot_idx(len(d))].mean(1)
        out[s] = {"n": len(d), "kannada_itrans_share": float(kn.mean()), "hindi_itrans_share": float(hi.mean()),
                  "hindi_minus_kannada": float(d.mean()), "ci": [float(v) for v in np.percentile(bs, [2.5, 97.5])],
                  "items_with_any_english_kannada": int((kn > 0).sum()), "items_with_any_english_hindi": int((hi > 0).sum())}
    write_json(OUT / "itrans_share.json", out, {"registered": "RESULTS.md 2026-10-23 15:44 IST (exploratory note)",
                                                "status": "exploratory, no verdict"})
    print(json.dumps(out, indent=1), flush=True)
    return 0


# ---------------------------------------------------------------- option 1

def sib_native() -> dict:
    """{language: {SIB id: native text}} for all 1,004 items."""
    kn = {int(it["id"]): it["forms"]["native"]["text"] for it in lad.e0c_items()["sib"]}
    hi = {int(it["id"]): it["forms"]["native"]["text"] for it in hh.sib_items()}
    assert sorted(kn) == sorted(hi) and len(kn) == 1004
    return {"kannada": kn, "hindi": hi}


def load_drafts(lang: str) -> dict:
    p = DRAFTS[lang]
    return {r["key"]: r for r in map(json.loads, p.open(encoding="utf-8"))} if p.exists() else {}


def do_draft() -> int:
    client, native, stopped, summary = make_client(), sib_native(), None, {}
    for lang, (_, pv) in LANGS.items():
        done = load_drafts(lang)
        for i, text in sorted(native[lang].items()):
            key = f"flores-{i}"
            if stopped or (key in done and (not done[key]["defective"] or done[key]["attempt"] >= 3)):
                continue
            for attempt in range(done[key]["attempt"] + 1 if key in done else 1, 4):
                try:
                    r = romanize(client, text, version=pv, attempt=attempt)
                except DailyQuotaExceeded as e:
                    stopped = str(e)[:200]
                    break
                row = {"key": key, "native": text, "natural": r["natural"], "attempt": attempt, "prompt": pv,
                       "model": MODEL, "finish_reason": r["finish_reason"]}
                row["defective"] = defective(row)
                done[key] = row
                if not row["defective"]:
                    break
        with tmp_path(DRAFTS[lang]).open("w", encoding="utf-8") as f:
            for k in sorted(done):
                f.write(json.dumps(done[k], ensure_ascii=False) + "\n")
        commit(tmp_path(DRAFTS[lang]), DRAFTS[lang])
        summary[lang] = {"n_done": len(done), "n_defective": sum(r["defective"] for r in done.values()),
                         "complete": len(done) == 1004 and all(not r["defective"] or r["attempt"] >= 3 for r in done.values())}
    complete = stopped is None and all(v["complete"] for v in summary.values())
    print({**summary, "stopped": stopped, "complete": complete}, flush=True)
    if complete:
        write_json(DONE, summary, {"prompts": {lg: pv for lg, (_, pv) in LANGS.items()}, "model": MODEL})
    return 0 if complete else 3


def clean1(lang: str) -> dict:
    return {int(k.split("-")[1]): r["natural"] for k, r in load_drafts(lang).items() if not r["defective"]}


def do_score(which: str, only: str | None = None) -> int:
    assert DONE.exists(), "SIB-1004 drafts are not complete"
    assert which == "check" or which in lad.COUNT_ACC, which
    base = {"kannada": {int(it["id"]): it for it in lad.e0c_items()["sib"]},
            "hindi": {int(it["id"]): it for it in hh.sib_items()}}
    for lang in LANGS:
        if only and lang != only:
            continue
        nat = clean1(lang)
        items = [{"task": "sib", "id": i, "label": it["label"],
                  "forms": {"native": it["forms"]["native"], FORM1: {"text": nat[i]}}}
                 for i, it in sorted(base[lang].items()) if i in nat]
        SCORE1[lang].mkdir(parents=True, exist_ok=True)
        for m in lad.COUNT_ACC:
            if which != "check":
                if m == which:
                    e0b.score_model(m, {"sib": items}, [FORM1], SCORE1[lang])
                continue
            x = pd.read_parquet(SCORE1[lang] / f"{m}__{FORM1}.parquet")
            if len(x) != len(items) or x.logprobs.map(lambda v: np.isnan(np.asarray(v)).any()).any():
                print(f"CHECK FAILED: {lang}/{m} has {len(x)} rows (expected {len(items)}) or NaN log-probs", flush=True)
                return 1
    if which != "check":
        return 0
    # reproduction check: overlap items with identical text agree with the H1 natural predictions
    nat_h1 = {"kannada": {it["id"]: it["forms"]["natural257"]["text"] for it in lad.sib257_items()["sib"]},
              "hindi": {int(k.split("-")[1]): v for k, v in hh.clean_natural().items() if k.startswith("flores-")}}
    old = {"kannada": scored({"sib": lad.E0C_DIR}, ["natural257"]), "hindi": scored({"sib": hh.SCORE_DIRS["sib"]}, ["natural"])}
    new = {lang: scored({"sib": SCORE1[lang]}, [FORM1]) for lang in LANGS}
    rep = {}
    for lang in LANGS:
        nat = clean1(lang)
        same = [i for i, v in nat_h1[lang].items() if nat.get(i) == v]
        for m in lad.COUNT_ACC:
            o = old[lang][old[lang].model == m].set_index("id").pred_cal
            n = new[lang][new[lang].model == m].set_index("id").pred_cal
            same_m = [i for i in same if i in o.index and i in n.index]
            agree = float((o.loc[same_m].to_numpy() == n.loc[same_m].to_numpy()).mean()) if same_m else float("nan")
            rep[f"{lang}/{m}"] = {"n_identical_text": len(same_m), "n_overlap": len(nat_h1[lang]), "agreement": agree}
    write_json(OUT / "opt1_reproduction.json", rep, {"rule": "pred_cal agreement >= 0.98 on identical-text overlap"})
    bad = {k: v for k, v in rep.items() if not v["agreement"] >= 0.98}
    if bad:
        print(f"CHECK FAILED: reproduction {bad}", flush=True)
        return 1
    return 0


def do_analyse1() -> int:
    from statsmodels.stats.multitest import multipletests
    wl = es.wordlists()["zipf>=3"]
    nk, nh = clean1("kannada"), clean1("hindi")
    both = sorted(set(nk) & set(nh))
    free = [i for i in both if hh.en_count(nk[i], wl)[0] == 0 and hh.en_count(nh[i], wl)[0] == 0]
    K = pd.concat([scored({"sib": lad.E0C_DIR}, ["native"]), scored({"sib": SCORE1["kannada"]}, [FORM1])])
    H = pd.concat([scored({"sib": hh.SCORE_DIRS["sib"]}, ["native"]), scored({"sib": SCORE1["hindi"]}, [FORM1])])
    rows = []
    for subset, ids in (("loan_free", free), ("all_clean", both)):
        for m in lad.COUNT_ACC:
            a = K[K.model == m].pivot_table(index="id", columns="form", values="correct").loc[ids]
            b = H[H.model == m].pivot_table(index="id", columns="form", values="correct").loc[ids]
            d = ((a["native"] - a[FORM1]) - (b["native"] - b[FORM1])).to_numpy(float)
            bs = d[boot_idx(len(d))].mean(1)
            rows.append({"subset": subset, "model": m, "n": len(d), "kannada_native": a["native"].mean(),
                         "kannada_natural": a[FORM1].mean(), "hindi_native": b["native"].mean(),
                         "hindi_natural": b[FORM1].mean(), "diff_of_gaps": float(d.mean()),
                         "ci": [float(v) for v in np.percentile(bs, [2.5, 97.5])], "p": boot_p(bs)})
    R = pd.DataFrame(rows)
    R["p_holm"] = np.nan
    for s, g in R.groupby("subset"):
        R.loc[g.index, "p_holm"] = multipletests(g.p, method="holm")[1]
    R["positive"] = (R.p_holm < 0.05) & (R.diff_of_gaps > 0)
    R.to_csv(OUT / "opt1.csv", index=False)
    g = R[R.subset == "loan_free"]
    pos = int(g.positive.sum())
    v = {"n_items_loan_free": len(free), "n_items_clean_both": len(both), "n_positive": pos, "needed": 3,
         "verdict": "loan-free effect" if pos >= 3 else "refuted",
         "all_clean_descriptive_n_positive": int(R[R.subset == "all_clean"].positive.sum())}
    write_json(OUT / "opt1_verdict.json", v, {"registered": "RESULTS.md 2026-10-23 15:44 IST (H1-LF option 1, "
                                                            "follow-up registered post H1)"})
    print(json.dumps(v), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit({"opt2": do_opt2, "itrans": do_itrans, "draft": do_draft,
              "score": lambda: do_score(*sys.argv[2:4]), "analyse1": do_analyse1}[sys.argv[1]]() or 0)
