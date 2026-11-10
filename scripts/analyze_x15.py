"""X15 analysis, exactly as registered (RESULTS.md, X15, Phase 2 pre-registration). Runs as soon as the importer has written results/phase2/x15/x15_g*_seat*.csv.
No outcome-dependent choice.

Data: 100 SIB-200 items stratified by category, 4 forms (native, ITRANS, lossy, natural), Latin square over four groups of two annotators (800 judgments, 2 per item-form). The gold
label of an item is the SIB-200 label (read from the private key annotation/private/x15_keys.json; this file is the only place where gold labels and forms are joined).
Statistics: accuracy per form with 95% bootstrap CIs resampling ITEMS AND ANNOTATORS (10,000 resamples, seed 0): in each resample, items are drawn with replacement from the 100 and
annotators with replacement from the annotators present; a judgment (item i, annotator a) has weight count(i) x count(a); accuracy of a form = weighted share correct among the judgments
of that form. Chance = 1/7. Prediction X15-P: human accuracy on native and natural differs by less than 5 points. *Supported:* |diff| < 0.05 and the 90% CI within +-0.12;
*refuted:* |diff| >= 0.05 with the 95% CI excluding 0; *inconclusive:* otherwise (diff = accuracy(native) - accuracy(natural), same resamples, 90% and 95% percentile intervals).
Model accuracies on the same 100 items (Phase 1 SIB-200 scores, calibrated as Phase 1: mean of the content-free inputs with the raw fallback rule), 95% bootstrap CI over items,
reported next to the human ones; Qwen2.5 is shown but never counted.
Usage: python scripts/analyze_x15.py [--in DIR] [--out DIR]   (defaults: results/phase2/x15)
"""
import argparse
import csv
import glob
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e0b_familiarity as e0b  # noqa: E402
import e0c_sib as e0c  # noqa: E402

from shattered.runlog import REPO, results_dir, write_json  # noqa: E402

N_BOOT, SEED = 10_000, 0
FORMS = ["native", "itrans", "lossy", "natural"]
CHANCE = 1 / 7
KEYS = REPO / "annotation" / "private" / "x15_keys.json"


def pct(x, q):
    return [float(v) for v in np.percentile(x, q)]


def human(d: Path) -> dict:
    keys = json.loads(KEYS.read_text(encoding="utf-8"))
    gold = {str(i["sib_id"]): i["gold"] for i in keys["items"]}
    rows = []
    for f in sorted(glob.glob(str(d / "x15_g*_seat*.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            rows.append({"item": r["item_id"], "form": r["form"], "ann": f"g{r['group']}{r['seat']}", "correct": float(r["choice"] == gold[r["item_id"]])})
    df = pd.DataFrame(rows)
    items, anns = sorted(df.item.unique()), sorted(df.ann.unique())
    ii, aa = {x: k for k, x in enumerate(items)}, {x: k for k, x in enumerate(anns)}
    C = np.full((len(items), len(anns)), np.nan)
    Fm = np.full((len(items), len(anns)), -1)
    for r in df.itertuples():
        C[ii[r.item], aa[r.ann]] = r.correct
        Fm[ii[r.item], aa[r.ann]] = FORMS.index(r.form)
    rng = np.random.default_rng(SEED)
    wi = np.stack([np.bincount(rng.integers(0, len(items), len(items)), minlength=len(items)) for _ in range(N_BOOT)]).astype(float)
    wa = np.stack([np.bincount(rng.integers(0, len(anns), len(anns)), minlength=len(anns)) for _ in range(N_BOOT)]).astype(float)
    acc_b, res = {}, {"n_judgments": int(len(df)), "n_items": len(items), "n_annotators": len(anns), "annotators": anns, "forms": {}}
    mask = {f: (Fm == k) & np.isfinite(C) for k, f in enumerate(FORMS)}
    for f in FORMS:
        M = mask[f]
        num = np.einsum("bi,ia,ba->b", wi, np.where(M, C, 0.0), wa)
        den = np.einsum("bi,ia,ba->b", wi, M.astype(float), wa)
        acc_b[f] = num / den
        k = M.sum()
        res["forms"][f] = {"n_judgments": int(k), "accuracy": float(np.nansum(np.where(M, C, 0)) / k) if k else None, "ci95": pct(acc_b[f], [2.5, 97.5]) if k else None,
                           "chance": CHANCE}
    nat, nz = res["forms"]["native"]["accuracy"], res["forms"]["natural"]["accuracy"]
    diff = nat - nz
    db = acc_b["native"] - acc_b["natural"]
    ci90, ci95 = pct(db, [5, 95]), pct(db, [2.5, 97.5])
    if abs(diff) < 0.05 and ci90[0] >= -0.12 and ci90[1] <= 0.12:
        verdict = "supported"
    elif abs(diff) >= 0.05 and (ci95[0] > 0 or ci95[1] < 0):
        verdict = "refuted"
    else:
        verdict = "inconclusive"
    res["X15_P"] = {"native_minus_natural": float(diff), "ci90": ci90, "ci95": ci95, "verdict": verdict,
                    "rule": "supported: |diff| < 0.05 and 90% CI within +-0.12; refuted: |diff| >= 0.05 with the 95% CI excluding 0; inconclusive otherwise"}
    res["complete_design"] = bool(len(anns) == 8 and all(mask[f].sum() == 200 for f in FORMS))
    if not res["complete_design"]:
        res["warning"] = f"{len(anns)} annotators and judgments per form {[int(mask[f].sum()) for f in FORMS]}: the registered design has 8 annotators and 200 judgments per form; verdict not final"
    return res, items


def models_on(items: list[str]) -> dict:
    """Calibrated accuracy of the Phase 1 models on exactly these SIB-200 items."""
    root = REPO / "results" / "e0c_sib" / "scores"
    forms = ["english", "native", "itrans", "lossy", "natural257"]
    df = pd.concat([pd.read_parquet(root / f"{m}__{f}.parquet") for m in e0c.MODELS for f in forms], ignore_index=True)
    df, fb = e0b.apply_calibration(df, {m: json.load(open(root / f"cf_{m}.json")) for m in e0c.MODELS})
    use = {int(i) for i in items}
    out = {}
    for m in e0c.MODELS:
        out[m] = {"counted": m != "qwen2.5-1.5b", "raw_fallback": bool(fb[(fb.model == m)].use_raw.any())}
        for f in ("native", "itrans", "lossy", "natural257"):
            g = df[(df.model == m) & (df.form == f) & (df.id.isin(use))]
            c = (g.pred_cal.to_numpy() == g.label.to_numpy()).astype(float)
            lo, hi = e0b.bootstrap_ci(c) if len(c) else (None, None)
            out[m][f"{f}"] = {"n": int(len(c)), "accuracy": float(c.mean()) if len(c) else None, "ci95": [lo, hi]}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--skip-deviation-check", action="store_true", help="tests on synthetic data only")
    a = ap.parse_args()
    d = Path(a.inp) if a.inp else results_dir("phase2/x15")
    out = Path(a.out) if a.out else d
    out.mkdir(parents=True, exist_ok=True)
    n_files = len(glob.glob(str(d / "x15_g*_seat*.csv")))
    if n_files < 8 and not a.skip_deviation_check:
        log = (REPO / "RESULTS.md").read_text(encoding="utf-8")
        if f"X15 DEVIATION: {n_files} of 8 files" not in log:
            print(f"{n_files} of 8 X15 files: log the line \"X15 DEVIATION: {n_files} of 8 files\" in RESULTS.md as a deviation before analysing anything (the lead author's rule); not run.")
            return 3
    res, items = human(d)
    res["models_same_items"] = models_on(items)
    res.update({"n_boot": N_BOOT, "seed": SEED})
    write_json(out / "analysis.json", res, {"registration": "RESULTS.md X15 (Phase 2 pre-registration)"})
    print(json.dumps({"forms": {f: (round(v["accuracy"], 3), [round(x, 3) for x in v["ci95"]]) for f, v in res["forms"].items()}, "X15_P": res["X15_P"],
                      "complete": res["complete_design"]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
