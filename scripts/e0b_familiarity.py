"""E0b familiarity test: five forms x models, contextual calibration, McNemar tests, P1-P3 verdicts.

Pre-registered in RESULTS.md (2026-10-14). Same 200 items per task as E0 (seed 0).

Usage: python scripts/e0b_familiarity.py --models qwen2.5-1.5b qwen3.5-2b sarvam-1 gemma4-e2b qwen3-1.7b
       python scripts/e0b_familiarity.py --models ... --forms english native itrans lossy --tag gate1a   (provisional)
Scores are cached per (model, form) in results/e0b_familiarity/scores/, so adding a form later scores only that form.
Outputs (results/e0b_familiarity/<tag>/): accuracy.csv, mcnemar.csv, mcnemar_exploratory.csv, fertility.csv,
                                          verdicts.json, summary.json

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
from shattered.runlog import REPO, results_dir, write_json
from shattered.translit import to_lossy

FORMS = ["english", "native", "itrans", "lossy", "natural"]
CHANCE = {"xnli": 1 / 3, "sentiment": 0.5}
QWEN = {"qwen2.5-1.5b", "qwen3.5-2b"}
COMPARISONS = [("natural", "native"), ("natural", "itrans"), ("lossy", "itrans")]
EXPLORATORY = [("itrans", "native")]
OUT_NAME = "e0b_familiarity"


def load_items(forms: list[str]) -> dict:
    nat = {r["native"]: r["natural"] for r in map(json.loads, open(REPO / "data" / "processed" / "natural_e0_v1.jsonl",
                                                                      encoding="utf-8"))}
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
        out[t] = items
    return out


def bootstrap_ci(x: np.ndarray, n_boot: int = 10000, seed: int = 0) -> tuple[float, float]:
    idx = np.random.default_rng(seed).integers(0, len(x), size=(n_boot, len(x)))
    m = x[idx].mean(1)
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def score_model(name: str, items: dict, forms: list[str], score_dir) -> None:
    """Scores every item in each form not yet on disk; one parquet + one json (fertility, calibration) per form."""
    todo = [f for f in forms if not (score_dir / f"{name}__{f}.parquet").exists()]
    if not todo:
        return
    import torch
    t0 = time.time()
    model, tok = load(name, "cuda")
    cf = {t: choice_logprobs(model, tok, build_prompt(t, {k: "N/A" for k in its[0]["forms"]["native"]}),
                             VERBALIZERS[t])[0] for t, its in items.items()}
    print(f"{name}: loaded in {time.time() - t0:.0f}s", flush=True)
    for f in todo:
        t1, rows, fert = time.time(), [], []
        for t, its in items.items():
            for it in its:
                lp, n_tok = choice_logprobs(model, tok, build_prompt(t, it["forms"][f]), VERBALIZERS[t])
                cal = np.asarray(lp) - np.asarray(cf[t])
                rows.append({"model": name, "task": t, "form": f, "id": it["id"], "label": it["label"],
                             "logprobs": lp, "logprobs_cal": cal.tolist(), "pred_raw": int(np.argmax(lp)),
                             "pred_cal": int(np.argmax(cal)), "prompt_tokens": n_tok})
            texts = [v for it in its for v in it["forms"][f].values()]
            ntok = sum(len(x) for x in tok(texts, add_special_tokens=False)["input_ids"])
            fert.append({"model": name, "task": t, "form": f, "n_texts": len(texts),
                         "tokens_per_word": ntok / sum(len(x.split()) for x in texts)})
        pd.DataFrame(rows).to_parquet(score_dir / f"{name}__{f}.parquet")
        (score_dir / f"{name}__{f}.json").write_text(json.dumps(
            {"content_free_logprobs": cf, "fertility": fert, "seconds": time.time() - t1}, indent=1), encoding="utf-8")
        print(f"{name}/{f}: {len(rows)} prompts in {time.time() - t1:.0f}s", flush=True)
    del model
    torch.cuda.empty_cache()


def accuracy_table(df: pd.DataFrame) -> pd.DataFrame:
    out = []
    for (m, t, f), g in df.groupby(["model", "task", "form"]):
        y = g.label.to_numpy()
        row = {"model": m, "task": t, "form": f, "n": len(g), "chance": CHANCE[t]}
        for kind in ("cal", "raw"):
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
            ca, cb = corr[a], corr[b]
            table = [[int((ca & cb).sum()), int((ca & ~cb).sum())], [int((~ca & cb).sum()), int((~ca & ~cb).sum())]]
            res = mcnemar(table, exact=True)
            rows.append({"model": m, "task": t, "a": a, "b": b, "acc_a": ca.mean(), "acc_b": cb.mean(),
                         "diff": ca.mean() - cb.mean(), "a_only": table[0][1], "b_only": table[1][0],
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
    fert = pd.DataFrame([r for e in extra.values() for r in e["fertility"]])
    acc, mc, ex = accuracy_table(df), mcnemar_table(df, COMPARISONS), mcnemar_table(df, EXPLORATORY)
    acc = acc.merge(fert[["model", "task", "form", "tokens_per_word"]], on=["model", "task", "form"])
    acc.to_csv(out / "accuracy.csv", index=False)
    mc.to_csv(out / "mcnemar.csv", index=False)
    ex.to_csv(out / "mcnemar_exploratory.csv", index=False)
    fert.to_csv(out / "fertility.csv", index=False)
    v = verdicts(acc, mc)
    cfg = {"models": args.models, "forms": args.forms, "calibration": "contextual, content-free 'N/A' in every field",
           "templates": "e0_{xnli,sentiment}_v1", "n_per_task": 200, "seed": 0, "bos": "always prepended",
           "seconds_per_model_form": {f"{m}/{f}": e["seconds"] for (m, f), e in extra.items()}}
    write_json(out / "verdicts.json", v, cfg)
    write_json(out / "summary.json", {"accuracy": acc.to_dict("records"), "mcnemar": mc.to_dict("records"),
                                      "mcnemar_exploratory": ex.to_dict("records"),
                                      "fertility": fert.to_dict("records"), "verdicts": v}, cfg)
    print(json.dumps(v, indent=1))


if __name__ == "__main__":
    main()
