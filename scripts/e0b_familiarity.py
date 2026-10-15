"""E0b familiarity test: five forms x models, contextual calibration, McNemar tests, P1-P3 verdicts.

Pre-registered in RESULTS.md (2026-10-14). Same 200 items per task as E0 (seed 0).

Usage: python scripts/e0b_familiarity.py --models qwen2.5-1.5b qwen3.5-2b sarvam-1 gemma4-e2b qwen3-1.7b
       python scripts/e0b_familiarity.py --models ... --forms english native itrans lossy --tag gate1a   (provisional)
Scores are cached per (model, form) in results/e0b_familiarity/scores/, so adding a form later scores only that form.
Outputs (results/e0b_familiarity/<tag>/): accuracy.csv, mcnemar.csv, mcnemar_exploratory.csv, fertility.csv,
                                          verdicts.json, summary.json

Calibration (deviation registered 2026-10-15): primary = content-free log-probs averaged over "N/A", "" and "[MASK]";
if a model x task's calibrated English accuracy is > 5 points below raw, that whole row uses raw scores (flagged).
Raw and "N/A"-only results are also written. Items whose natural romanization is still defective after retries are
dropped from the natural form only.

McNemar/Holm: the registered family is COMPARISONS (natural-native, natural-itrans, lossy-itrans), restricted to the
forms present. itrans-native is an exploratory comparison, Holm-corrected separately.
"""
import argparse
import json
import time

import numpy as np
import pandas as pd
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.multitest import multipletests

from shattered.data import tasks
from shattered.eval.loglik import VERBALIZERS, build_prompt, choice_logprobs
from shattered.interp.load import load
from shattered.runlog import REPO, commit, results_dir, tmp_path, write_json
from shattered.translit import to_lossy

FORMS = ["english", "native", "itrans", "lossy", "natural"]
CHANCE = {"xnli": 1 / 3, "sentiment": 0.5}
QWEN = {"qwen2.5-1.5b", "qwen3.5-2b"}
COMPARISONS = [("natural", "native"), ("natural", "itrans"), ("lossy", "itrans")]
EXPLORATORY = [("itrans", "native")]
OUT_NAME = "e0b_familiarity"
CONTENT_FREE = ["N/A", "", "[MASK]"]
FALLBACK_POINTS = 0.05


def load_items(forms: list[str]) -> dict:
    from shattered.translit.natural import defective
    rows = [json.loads(x) for x in open(REPO / "data" / "processed" / "natural_e0_v1.jsonl", encoding="utf-8")]
    nat = {r["native"]: r["natural"] for r in rows}
    bad = {r["native"] for r in rows if defective(r)}
    out = {}
    for t in ("xnli", "sentiment"):
        items = tasks.stratified_sample(tasks.load_task(t), 200, seed=0)
        for it in items:
            native = it["forms"]["native"]
            it["forms"]["lossy"] = {k: to_lossy(v) for k, v in native.items()}
            if "natural" in forms:
                missing = [v for v in native.values() if v not in nat]
                if missing:
                    raise SystemExit(f"natural romanization missing for {len(missing)} texts; run e0b_natural.py first")
                it["forms"]["natural"] = {k: nat[v] for k, v in native.items()}
                it["natural_defective"] = any(v in bad for v in native.values())
        out[t] = items
    return out


def bootstrap_ci(x: np.ndarray, n_boot: int = 10000, seed: int = 0) -> tuple[float, float]:
    idx = np.random.default_rng(seed).integers(0, len(x), size=(n_boot, len(x)))
    m = x[idx].mean(1)
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def content_free(name: str, items: dict, score_dir, model=None, tok=None) -> dict:
    """{input: {task: [label log-probs]}} for every content-free input; cached in cf_<model>.json."""
    path = score_dir / f"cf_{name}.json"
    if path.exists():
        return json.load(open(path))
    own = model is None
    if own:
        model, tok = load(name, "cuda")
    cf = {x: {t: choice_logprobs(model, tok, build_prompt(t, {k: x for k in its[0]["forms"]["native"]}),
                                 VERBALIZERS[t])[0] for t, its in items.items()} for x in CONTENT_FREE}
    tmp_path(path).write_text(json.dumps(cf, indent=1), encoding="utf-8")
    commit(tmp_path(path), path)
    if own:
        import torch
        del model
        torch.cuda.empty_cache()
    return cf


def score_model(name: str, items: dict, forms: list[str], score_dir) -> None:
    """Scores every item in each form not yet on disk; one parquet + one json (fertility, calibration) per form."""
    todo = [f for f in forms if not (score_dir / f"{name}__{f}.parquet").exists()]
    if not todo:
        content_free(name, items, score_dir)
        return
    import torch
    t0 = time.time()
    model, tok = load(name, "cuda")
    cf = {t: choice_logprobs(model, tok, build_prompt(t, {k: "N/A" for k in its[0]["forms"]["native"]}),
                             VERBALIZERS[t])[0] for t, its in items.items()}
    content_free(name, items, score_dir, model, tok)
    print(f"{name}: loaded in {time.time() - t0:.0f}s", flush=True)
    for f in todo:
        t1, rows, fert = time.time(), [], []
        for t, its in items.items():
            for it in its:
                if f == "natural" and it.get("natural_defective"):
                    continue
                lp, n_tok = choice_logprobs(model, tok, build_prompt(t, it["forms"][f]), VERBALIZERS[t])
                cal = np.asarray(lp) - np.asarray(cf[t])
                rows.append({"model": name, "task": t, "form": f, "id": it["id"], "label": it["label"],
                             "logprobs": lp, "logprobs_cal": cal.tolist(), "pred_raw": int(np.argmax(lp)),
                             "pred_cal": int(np.argmax(cal)), "prompt_tokens": n_tok})
            texts = [v for it in its if not (f == "natural" and it.get("natural_defective"))
                     for v in it["forms"][f].values()]
            ntok = sum(len(x) for x in tok(texts, add_special_tokens=False)["input_ids"])
            fert.append({"model": name, "task": t, "form": f, "n_texts": len(texts),
                         "tokens_per_word": ntok / sum(len(x.split()) for x in texts)})
        # json first, parquet last: the parquet's existence marks the (model, form) as finished
        meta_path, pq_path = score_dir / f"{name}__{f}.json", score_dir / f"{name}__{f}.parquet"
        tmp_path(meta_path).write_text(json.dumps(
            {"content_free_logprobs": cf, "fertility": fert, "seconds": time.time() - t1}, indent=1), encoding="utf-8")
        commit(tmp_path(meta_path), meta_path)
        pd.DataFrame(rows).to_parquet(tmp_path(pq_path))
        commit(tmp_path(pq_path), pq_path)
        print(f"{name}/{f}: {len(rows)} prompts in {time.time() - t1:.0f}s", flush=True)
    del model
    torch.cuda.empty_cache()


def apply_calibration(df: pd.DataFrame, cf: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Adds pred_raw, pred_na, pred_avg3 and the primary pred_cal (avg3 with the raw fallback rule).
    cf: {model: {input: {task: logprobs}}}. Returns (df, fallback table)."""
    df = df.copy()
    lp = df.logprobs.map(np.asarray)
    df["pred_raw"] = lp.map(np.argmax)
    for col, inputs in (("pred_na", ["N/A"]), ("pred_avg3", CONTENT_FREE)):
        df[col] = [int(np.argmax(x - np.mean([cf[m][i][t] for i in inputs], axis=0)))
                   for x, m, t in zip(lp, df.model, df.task)]
    fb = []
    for (m, t), g in df[df.form == "english"].groupby(["model", "task"]):
        raw, cal = (g.pred_raw == g.label).mean(), (g.pred_avg3 == g.label).mean()
        fb.append({"model": m, "task": t, "english_raw": raw, "english_avg3": cal,
                   "use_raw": bool(cal < raw - FALLBACK_POINTS)})
    fb = pd.DataFrame(fb)
    use_raw = {(r.model, r.task) for r in fb.itertuples() if r.use_raw}
    df["pred_cal"] = [r if (m, t) in use_raw else c for r, c, m, t in zip(df.pred_raw, df.pred_avg3, df.model, df.task)]
    return df, fb


def accuracy_table(df: pd.DataFrame) -> pd.DataFrame:
    out = []
    for (m, t, f), g in df.groupby(["model", "task", "form"]):
        y = g.label.to_numpy()
        row = {"model": m, "task": t, "form": f, "n": len(g), "chance": CHANCE[t]}
        for kind in ("cal", "raw", "na", "avg3"):
            c = (g[f"pred_{kind}"].to_numpy() == y).astype(float)
            lo, hi = bootstrap_ci(c)
            row.update({f"acc_{kind}": c.mean(), f"acc_{kind}_ci_low": lo, f"acc_{kind}_ci_high": hi,
                        f"constant_label_rate_{kind}": np.bincount(g[f"pred_{kind}"]).max() / len(g)})
        out.append(row)
    return pd.DataFrame(out)


def mcnemar_table(df: pd.DataFrame, comparisons) -> pd.DataFrame:
    forms = set(df.form)
    comparisons = [(a, b) for a, b in comparisons if a in forms and b in forms]
    rows = []
    for (m, t), g in df.groupby(["model", "task"]):
        piv = g.pivot_table(index="id", columns="form", values="pred_cal")
        lab = g.drop_duplicates("id").set_index("id").label.loc[piv.index]
        corr = piv.eq(lab, axis=0)
        for a, b in comparisons:
            keep = piv[a].notna() & piv[b].notna()  # natural form drops defective items
            ca, cb = corr[a][keep], corr[b][keep]
            table = [[int((ca & cb).sum()), int((ca & ~cb).sum())], [int((~ca & cb).sum()), int((~ca & ~cb).sum())]]
            res = mcnemar(table, exact=True)
            rows.append({"model": m, "task": t, "a": a, "b": b, "acc_a": ca.mean(), "acc_b": cb.mean(),
                         "n": int(keep.sum()), "diff": ca.mean() - cb.mean(), "a_only": table[0][1], "b_only": table[1][0],
                         "p": res.pvalue})
    mc = pd.DataFrame(rows)
    if mc.empty:
        return mc
    mc["p_holm"] = multipletests(mc.p, method="holm")[1]
    mc["significant"] = mc.p_holm < 0.05
    return mc


def verdicts(acc: pd.DataFrame, mc: pd.DataFrame) -> dict:
    """Apply the pre-registered decision rules (RESULTS.md, 2026-10-14) to whichever predictions the forms allow."""
    en = acc[acc.form == "english"].set_index(["model", "task"])
    informative = {k for k, r in en.iterrows() if r.acc_cal >= r.chance + 0.05}
    mc = mc[[(r.model, r.task) in informative for r in mc.itertuples()]]
    out = {"informative_cells": sorted(f"{m}/{t}" for m, t in informative)}

    lossy = mc[(mc.a == "lossy") & (mc.b == "itrans")]
    if len(lossy):
        out["P3_lossy_lt_itrans"] = bool((lossy["diff"] < 0).all() and lossy.significant.mean() >= 0.5)
        out["P3_parts"] = {"all_cells_lossy_below_itrans": bool((lossy["diff"] < 0).all()),
                           "fraction_significant": float(lossy.significant.mean()), "n_cells": len(lossy)}
    if not (mc.a == "natural").any():
        out["P1_familiarity_dominates"] = out["P2_fragmentation_also_matters"] = "pending (natural form not scored)"
        return out

    def sig(a, b, sign, model=None):
        d = mc[(mc.a == a) & (mc.b == b)]
        if model:
            d = d[d.model == model]
        return d[(d.significant) & (np.sign(d["diff"]) == sign)]

    nat_itr = mc[(mc.a == "natural") & (mc.b == "itrans")]
    p1 = bool((nat_itr["diff"] >= 0).all() and sig("natural", "itrans", -1).empty
              and sig("natural", "native", +1).empty)
    p2_qwen = all(not sig("natural", "native", +1, q).empty and sig("natural", "native", -1, q).empty
                  for q in QWEN)
    p2_sarvam = not sig("natural", "native", -1, "sarvam-1").empty
    return {**out, "P1_familiarity_dominates": p1, "P2_fragmentation_also_matters": bool(p2_qwen and p2_sarvam),
            "P2_parts": {"qwen_natural_gt_native": p2_qwen, "sarvam_natural_lt_native": p2_sarvam}}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--forms", nargs="+", default=FORMS, choices=FORMS)
    ap.add_argument("--tag", default="gate1")
    args = ap.parse_args()
    root = results_dir(OUT_NAME)
    score_dir, out = root / "scores", root / args.tag
    score_dir.mkdir(exist_ok=True)
    out.mkdir(exist_ok=True)
    items = load_items(args.forms)
    for name in args.models:
        score_model(name, items, args.forms, score_dir)
    df = pd.concat([pd.read_parquet(score_dir / f"{m}__{f}.parquet") for m in args.models for f in args.forms],
                   ignore_index=True)
    extra = {(m, f): json.load(open(score_dir / f"{m}__{f}.json")) for m in args.models for f in args.forms}
    df, fallback = apply_calibration(df, {m: json.load(open(score_dir / f"cf_{m}.json")) for m in args.models})
    fallback.to_csv(out / "calibration_fallback.csv", index=False)
    fert = pd.DataFrame([r for e in extra.values() for r in e["fertility"]])
    acc, mc, ex = accuracy_table(df), mcnemar_table(df, COMPARISONS), mcnemar_table(df, EXPLORATORY)
    acc = acc.merge(fert[["model", "task", "form", "tokens_per_word"]], on=["model", "task", "form"])
    acc.to_csv(out / "accuracy.csv", index=False)
    mc.to_csv(out / "mcnemar.csv", index=False)
    ex.to_csv(out / "mcnemar_exploratory.csv", index=False)
    fert.to_csv(out / "fertility.csv", index=False)
    v = verdicts(acc, mc)
    n_excl = sum(it.get("natural_defective", False) for its in items.values() for it in its)
    cfg = {"models": args.models, "forms": args.forms,
           "calibration": "primary: mean of content-free N/A, '', [MASK]; raw fallback if English drops > 5 pts",
           "calibration_fallback_rows": fallback[fallback.use_raw][["model", "task"]].to_dict("records"),
           "natural_items_excluded_defective": n_excl,
           "templates": "e0_{xnli,sentiment}_v1", "n_per_task": 200, "seed": 0, "bos": "always prepended",
           "seconds_per_model_form": {f"{m}/{f}": e["seconds"] for (m, f), e in extra.items()}}
    write_json(out / "verdicts.json", v, cfg)
    write_json(out / "summary.json", {"calibration_fallback": fallback.to_dict("records"),
                                      "accuracy": acc.to_dict("records"), "mcnemar": mc.to_dict("records"),
                                      "mcnemar_exploratory": ex.to_dict("records"),
                                      "fertility": fert.to_dict("records"), "verdicts": v}, cfg)
    print(json.dumps(v, indent=1))


if __name__ == "__main__":
    main()
