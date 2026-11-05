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
SEEDS = (0, 1)  # Sarvam-1 (primary); the Qwen3.5-2B arm has one seed (set in main)


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
    ap.add_argument("--seeds", default=None, help="comma-separated code seeds (extra seeds added 2026-11-05: --seeds 0,1,2,3 gives the all-four-seeds analysis; default = the registered original seeds)")
    cli = ap.parse_args()
    m = cli.model
    global SEEDS
    SEEDS = (0, 1) if m == "sarvam-1" else (0,)
    if cli.seeds:
        SEEDS = tuple(int(x) for x in cli.seeds.split(","))
    base = REPO / "results" / "kaggle"
    bdir = sorted(glob.glob(str(base / "**" / "out" / f"{m}__base" / "retrieval.json"), recursive=True))[0]
    bdir = Path(bdir).parent
    res = {"model": m, "measures": {}}
    runs = {(c, s): find(m, c, s) for c in CONDS for s in SEEDS}
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
        pick = {c: rng.integers(0, len(SEEDS), N_BOOT) for c in CONDS}  # one of the two seeds per cell per resample
        gm = {c: np.stack([gaps[(c, s)] for s in SEEDS]) for c in CONDS}  # [seeds, n]
        mean_c = {c: np.array([gm[c][pick[c][b]][idx[b]].mean() for b in range(N_BOOT)]) for c in CONDS}
        DN, DE = mean_c["native"] - mean_c["itrans"], mean_c["english"] - mean_c["itrans"]
        point = {c: float(np.mean([gaps[(c, s)].mean() for s in SEEDS])) for c in CONDS}
        row = {"n": int(n), "g0_before_training": float(g0.mean()), "g_after_seed_mean": point,
               "g_after_by_seed": {c: [float(gaps[(c, s)].mean()) for s in SEEDS] for c in CONDS}}
        for lab, D, a, b in (("D_N", DN, "native", "itrans"), ("D_E", DE, "english", "itrans")):
            lo, hi = float(np.percentile(D, 1.25)), float(np.percentile(D, 98.75))
            seeds = [float(gaps[(a, s)].mean() - gaps[(b, s)].mean()) for s in SEEDS]
            row[lab] = {"point": point[a] - point[b], "ci975": [lo, hi], "above_0": bool(lo > 0), "entirely_below_0": bool(hi < 0), "seed_spread_D_seed0_seed1": seeds}
        above = row["D_N"]["above_0"] + row["D_E"]["above_0"]
        below = row["D_N"]["entirely_below_0"] + row["D_E"]["entirely_below_0"]
        pts_nonpos = row["D_N"]["point"] <= 0 and row["D_E"]["point"] <= 0
        row["verdict"] = "supported" if above == 2 else "partly supported" if above == 1 and below == 0 else "refuted" if (above == 0 and below >= 1) or pts_nonpos else "inconclusive"
        accs = {f"{c}+s{s}": {"native": float(full[(c, s)]["native"].mean()), "itrans": float(full[(c, s)]["itrans"].mean())} for c in CONDS for s in SEEDS}
        row["accuracy_by_run"] = accs
        row["accuracy_base"] = {"native": float(bsib["native"].mean() if name.startswith("SIB") else bret["native"].mean()), "itrans": float(bsib["itrans"].mean() if name.startswith("SIB") else bret["itrans"].mean())}
        res["measures"][name] = row
    eng_base = float(bsib["english"].mean())
    res["english_sib_damage_check"] = {"base": eng_base, "by_run": {f"{c}+s{s}": {"acc": float(sib[(c, s)][0]["english"].mean()), "drop_points": float((eng_base - sib[(c, s)][0]["english"].mean()) * 100),
                                                                                   "flagged": bool(eng_base - sib[(c, s)][0]["english"].mean() > 0.05)} for c in CONDS for s in SEEDS}}
    res["tokenizer_unchanged"] = {f"{c}+s{s}": json.load(open(runs[(c, s)] / "done.json"))["tokenizer_unchanged"] for c in CONDS for s in SEEDS}
    res["B"] = json.load(open(runs[("itrans", 0)] / "done.json"))["B"]
    # ---- extras requested on 2026-11-05: per-run values, training budget per form, tokens per word, English regression with its interval, ITRANS-trained versus the ORIGINAL native level
    dones = {f"{c}+s{s}": json.load(open(runs[(c, s)] / "done.json")) for c in CONDS for s in SEEDS}
    res["per_run"] = {k: {"condition": d["condition"], "seed": d["seed"], "B_tokens": d["B"], "optimizer_steps": d["optimizer_steps"], "articles": d["articles"], "words": d["words"], "stream_tokens": d["tokens"],
                          "stream_tokens_per_word": d["tokens"] / d["words"], "tokenizer_sha256_before": d["tokenizer_sha256_before"], "tokenizer_sha256_after": d["tokenizer_sha256_after"],
                          "tokenizer_unchanged": d["tokenizer_unchanged"], "train_seconds": d["train_seconds"],
                          "sib": {f: float(sib[(d["condition"], d["seed"])][0][f].mean()) for f in ("english", "native", "itrans")},
                          "retrieval": {f: float(ret[(d["condition"], d["seed"])][f].mean()) for f in ("native", "itrans")}} for k, d in dones.items()}
    try:
        from transformers import AutoTokenizer

        from shattered.interp.load import MODELS
        from shattered.translit import to_itrans
        fl = json.load(open(REPO / "build" / "kaggle" / "flores_private" / "flores_private.json", encoding="utf-8"))["kn"]
        tk = AutoTokenizer.from_pretrained(MODELS[m])
        nw = sum(len(x.split()) for x in fl)
        res["tokens_per_word_flores"] = {"native": sum(len(x) for x in tk(fl, add_special_tokens=False)["input_ids"]) / nw,
                                         "itrans": sum(len(x) for x in tk([" ".join(to_itrans(w) for w in x.split()) for x in fl], add_special_tokens=False)["input_ids"]) / nw,
                                         "note": "tokenizer files are identical before and after training (sha256 in per_run), so tokens per word are the same before and after by construction"}
    except Exception as e:  # noqa: BLE001
        res["tokens_per_word_flores"] = {"error": repr(e)[:150]}
    eng_rng = np.random.default_rng(1)
    eidx = eng_rng.integers(0, len(bsib["english"]), (N_BOOT, len(bsib["english"])))
    res["english_regression_vs_base"] = {}
    for c in CONDS:
        d_ = np.mean([sib[(c, s)][0]["english"] - bsib["english"] for s in SEEDS], axis=0)  # per item, mean over seeds
        b_ = d_[eidx].mean(1)
        res["english_regression_vs_base"][c] = {"mean_change_points": float(d_.mean() * 100), "ci95_points": [float(np.percentile(b_, 2.5) * 100), float(np.percentile(b_, 97.5) * 100)],
                                                "flag_more_than_5_points": bool(d_.mean() < -0.05), "by_seed_points": [float((sib[(c, s)][0]["english"] - bsib["english"]).mean() * 100) for s in SEEDS]}
    res["itrans_trained_vs_original_native"] = {}
    for name, (get_run, get_base, nn) in {"SIB-200 accuracy": (lambda c, s: sib[(c, s)][0], bsib, len(bsib["english"])), "FLORES+ retrieval": (lambda c, s: ret[(c, s)], bret, len(bret["native"]))}.items():
        dd = np.mean([get_run("itrans", s)["itrans"] - get_base["native"] for s in SEEDS], axis=0)
        ii = np.random.default_rng(2).integers(0, nn, (N_BOOT, nn))
        bb = dd[ii].mean(1)
        res["itrans_trained_vs_original_native"][name] = {"itrans_accuracy_after_itrans_training": float(np.mean([get_run("itrans", s)["itrans"].mean() for s in SEEDS])), "original_native_accuracy_untrained": float(get_base["native"].mean()),
                                                         "difference": float(dd.mean()), "ci95": [float(np.percentile(bb, 2.5)), float(np.percentile(bb, 97.5))],
                                                         "reaches_original_native_level": bool(np.percentile(bb, 97.5) >= 0)}
    write_json(results_dir("phase2/x9b") / (f"analysis_{m}.json" if not cli.seeds else f"analysis_{m}_seeds{cli.seeds.replace(',', '')}.json"), res, {"registration": "RESULTS.md Amendment 2, X9b (primary Sarvam-1)" + ("" if not cli.seeds else "; seeds " + cli.seeds + " (the extra seeds were added after seeing the originals, RESULTS.md 2026-11-05)")})
    print(json.dumps({k: {"verdict": v["verdict"], "g0": round(v["g0_before_training"], 3), "g_after": {c: round(x, 3) for c, x in v["g_after_seed_mean"].items()},
                          "D_N": [round(v["D_N"]["point"], 3), [round(x, 3) for x in v["D_N"]["ci975"]], [round(x, 3) for x in v["D_N"]["seed_spread_D_seed0_seed1"]]],
                          "D_E": [round(v["D_E"]["point"], 3), [round(x, 3) for x in v["D_E"]["ci975"]], [round(x, 3) for x in v["D_E"]["seed_spread_D_seed0_seed1"]]]} for k, v in res["measures"].items()}, indent=1))
    print("english damage:", {k: round(v["drop_points"], 1) for k, v in res["english_sib_damage_check"]["by_run"].items()})


if __name__ == "__main__":
    main()
