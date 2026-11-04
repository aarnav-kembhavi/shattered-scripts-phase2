"""X9b analysis (registered, Amendment 2; primary model Sarvam-1, 2 seeds per condition): gap g(c) = native minus ITRANS after QLoRA training on condition c in {ITRANS, native, English}, g(0) before
training; D_N = g(native) - g(ITRANS), D_E = g(English) - g(ITRANS); prediction D_N > 0 and D_E > 0. Measures: SIB-200 accuracy (1,004 items, calibrated as Phase 1) and FLORES+ retrieval (test half n = 1,005,
unmapped at the train-chosen layer). Interval: paired bootstrap over items (SIB) or test sentences (retrieval), 10,000 resamples (seed 0), within each cell one of the two seeds drawn at random in every
resample (the interval includes seed variance), 97.5% intervals (1.25th and 98.75th percentiles; Bonferroni over D_N and D_E); seed spread (D from seed 0 runs and from seed 1 runs) next to each interval.
Supported: both intervals above 0. Partly supported: exactly one above 0 and none entirely below 0. Refuted: none above 0 and at least one entirely below 0, or both point estimates at or below 0. Inconclusive:
otherwise. English SIB-200 damage check (descriptive): a drop of more than 5 points from the base is flagged. Reads results/kaggle/**/out/<model>+<cond>+s<seed>/ (batches on both accounts).
Usage: python scripts/x9b_analyse.py [--model sarvam-1]     Output: results/phase2/x9b/analysis_<model>.json"""
import argparse
import glob
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e0b_familiarity as e0b  # noqa: E402

from shattered.runlog import REPO, results_dir, write_json  # noqa: E402

N_BOOT = 10_000
CONDS = ["itrans", "native", "english"]


def find(model: str, cond: str, seed: int) -> Path:
    hits = sorted(glob.glob(str(REPO / "results" / "kaggle" / "**" / "out" / f"{model}+{cond}+s{seed}" / "done.json"), recursive=True))
    hits = [h for h in hits if "rehearsal" not in h]
    assert hits, f"no finished run {model}+{cond}+s{seed}"
    return Path(hits[-1]).parent


def sib_correct(d: Path, tag: str) -> tuple[dict, dict]:
    e0b.CHANCE.setdefault("sib", 1 / 7)
    df = pd.concat([pd.read_parquet(d / f"sib_{f}.parquet") for f in ("english", "native", "itrans")], ignore_index=True)
    df["model"] = tag
    df, fb = e0b.apply_calibration(df, {tag: json.load(open(d / "cf.json"))})
    out = {}
    for f in ("english", "native", "itrans"):
        g = df[df.form == f].sort_values("id")
        out[f] = (g.pred_cal.to_numpy() == g.label.to_numpy()).astype(float)
    return out, {"raw_fallback_used": bool(fb.use_raw.any())}


def retr(d: Path) -> dict:
    return {f: np.load(d / f"retrieval_test_correct_{f}.npy").astype(float) for f in ("native", "itrans")}


def gap(x: dict) -> np.ndarray:
    return x["native"] - x["itrans"]  # per item


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="sarvam-1")
    m = ap.parse_args().model
    base = REPO / "results" / "kaggle"
    bdir = sorted(glob.glob(str(base / "**" / "out" / f"{m}__base" / "retrieval.json"), recursive=True))[0]
    bdir = Path(bdir).parent
    res = {"model": m, "measures": {}}
    runs = {(c, s): find(m, c, s) for c in CONDS for s in (0, 1)}
    sib = {k: sib_correct(d, f"{m}+{k[0]}+s{k[1]}") for k, d in runs.items()}
    bsib, _ = sib_correct(bdir, f"{m}__base")
    ret = {k: retr(d) for k, d in runs.items()}
    bret = retr(bdir)
    data = {"SIB-200 accuracy": ({k: gap(v[0]) for k, v in sib.items()}, gap(bsib), {k: v[0] for k, v in sib.items()}),
            "FLORES+ retrieval": ({k: gap(v) for k, v in ret.items()}, gap(bret), ret)}
    rng = np.random.default_rng(0)
    for name, (gaps, g0, full) in data.items():
        n = len(g0)
        idx = rng.integers(0, n, (N_BOOT, n))
        pick = {c: rng.integers(0, 2, N_BOOT) for c in CONDS}  # one of the two seeds per cell per resample
        gm = {c: np.stack([gaps[(c, 0)], gaps[(c, 1)]]) for c in CONDS}  # [2, n]
        mean_c = {c: np.array([gm[c][pick[c][b]][idx[b]].mean() for b in range(N_BOOT)]) for c in CONDS}
        DN, DE = mean_c["native"] - mean_c["itrans"], mean_c["english"] - mean_c["itrans"]
        point = {c: float(np.mean([gaps[(c, 0)].mean(), gaps[(c, 1)].mean()])) for c in CONDS}
        row = {"n": int(n), "g0_before_training": float(g0.mean()), "g_after_seed_mean": point,
               "g_after_by_seed": {c: [float(gaps[(c, 0)].mean()), float(gaps[(c, 1)].mean())] for c in CONDS}}
        for lab, D, a, b in (("D_N", DN, "native", "itrans"), ("D_E", DE, "english", "itrans")):
            lo, hi = float(np.percentile(D, 1.25)), float(np.percentile(D, 98.75))
            seeds = [float(gaps[(a, s)].mean() - gaps[(b, s)].mean()) for s in (0, 1)]
            row[lab] = {"point": point[a] - point[b], "ci975": [lo, hi], "above_0": bool(lo > 0), "entirely_below_0": bool(hi < 0), "seed_spread_D_seed0_seed1": seeds}
        above = row["D_N"]["above_0"] + row["D_E"]["above_0"]
        below = row["D_N"]["entirely_below_0"] + row["D_E"]["entirely_below_0"]
        pts_nonpos = row["D_N"]["point"] <= 0 and row["D_E"]["point"] <= 0
        row["verdict"] = "supported" if above == 2 else "partly supported" if above == 1 and below == 0 else "refuted" if (above == 0 and below >= 1) or pts_nonpos else "inconclusive"
        accs = {f"{c}+s{s}": {"native": float(full[(c, s)]["native"].mean()), "itrans": float(full[(c, s)]["itrans"].mean())} for c in CONDS for s in (0, 1)}
        row["accuracy_by_run"] = accs
        row["accuracy_base"] = {"native": float(bsib["native"].mean() if name.startswith("SIB") else bret["native"].mean()), "itrans": float(bsib["itrans"].mean() if name.startswith("SIB") else bret["itrans"].mean())}
        res["measures"][name] = row
    eng_base = float(bsib["english"].mean())
    res["english_sib_damage_check"] = {"base": eng_base, "by_run": {f"{c}+s{s}": {"acc": float(sib[(c, s)][0]["english"].mean()), "drop_points": float((eng_base - sib[(c, s)][0]["english"].mean()) * 100),
                                                                                   "flagged": bool(eng_base - sib[(c, s)][0]["english"].mean() > 0.05)} for c in CONDS for s in (0, 1)}}
    res["tokenizer_unchanged"] = {f"{c}+s{s}": json.load(open(runs[(c, s)] / "done.json"))["tokenizer_unchanged"] for c in CONDS for s in (0, 1)}
    res["B"] = json.load(open(runs[("itrans", 0)] / "done.json"))["B"]
    write_json(results_dir("phase2/x9b") / f"analysis_{m}.json", res, {"registration": "RESULTS.md Amendment 2, X9b (primary Sarvam-1)"})
    print(json.dumps({k: {"verdict": v["verdict"], "g0": round(v["g0_before_training"], 3), "g_after": {c: round(x, 3) for c, x in v["g_after_seed_mean"].items()},
                          "D_N": [round(v["D_N"]["point"], 3), [round(x, 3) for x in v["D_N"]["ci975"]], [round(x, 3) for x in v["D_N"]["seed_spread_D_seed0_seed1"]]],
                          "D_E": [round(v["D_E"]["point"], 3), [round(x, 3) for x in v["D_E"]["ci975"]], [round(x, 3) for x in v["D_E"]["seed_spread_D_seed0_seed1"]]]} for k, v in res["measures"].items()}, indent=1))
    print("english damage:", {k: round(v["drop_points"], 1) for k, v in res["english_sib_damage_check"]["by_run"].items()})


if __name__ == "__main__":
    main()
