"""E0 gate: can these open models understand Kannada? Log-likelihood scoring of English label words.

For each model x task (xnli, sentiment) x form (english, native, itrans): 200 stratified items (seed 0), English
instruction prompt (templates e0_<task>_v1), label = argmax log P(verbalizer | prompt). Primary metric: raw argmax
accuracy. Secondary: calibrated accuracy (subtract each label's mean log-prob over the items of that form).

Usage: python scripts/e00_gate.py --models qwen3-1.7b sarvam-1 [--n 200] [--device cuda] [--limit 0]
Outputs: results/e00_gate/scores_<model>.parquet, summary.csv, summary.json, sample_ids_<task>.json
"""
import argparse
import time

import numpy as np
import pandas as pd

from shattered.data import tasks
from shattered.eval.loglik import VERBALIZERS, build_prompt, choice_logprobs
from shattered.interp.load import load
from shattered.runlog import results_dir, write_json

FORMS = ["english", "native", "itrans"]
CHANCE = {"xnli": 1 / 3, "sentiment": 0.5}


def bootstrap_ci(correct: np.ndarray, n_boot: int = 10000, seed: int = 0) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(correct), size=(n_boot, len(correct)))
    acc = correct[idx].mean(1)
    return float(np.percentile(acc, 2.5)), float(np.percentile(acc, 97.5))


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (m, t, f), g in df.groupby(["model", "task", "form"]):
        lp = np.stack(g.logprobs.to_numpy())
        y = g.label.to_numpy()
        raw = lp.argmax(1) == y
        cal = (lp - lp.mean(0, keepdims=True)).argmax(1) == y
        lo, hi = bootstrap_ci(raw.astype(float))
        clo, chi = bootstrap_ci(cal.astype(float))
        rows.append({"model": m, "task": t, "form": f, "n": len(g), "chance": CHANCE[t],
                     "acc": raw.mean(), "acc_ci_low": lo, "acc_ci_high": hi,
                     "acc_calibrated": cal.mean(), "acc_cal_ci_low": clo, "acc_cal_ci_high": chi,
                     "pred_majority_share": float(np.bincount(lp.argmax(1)).max() / len(g)),
                     "mean_prompt_tokens": g.prompt_tokens.mean()})
    return pd.DataFrame(rows)


def gate(summary: pd.DataFrame) -> pd.DataFrame:
    """Brief's rule: native >= chance + 10 pts AND English >= chance + 15 pts on at least one task (raw accuracy)."""
    out = []
    for m, g in summary.groupby("model"):
        passes = []
        for t, gt in g.groupby("task"):
            a = gt.set_index("form").acc
            if "native" in a and "english" in a:
                ok = a["native"] >= CHANCE[t] + 0.10 and a["english"] >= CHANCE[t] + 0.15
                passes.append((t, bool(ok)))
        out.append({"model": m, "passes": any(ok for _, ok in passes), "by_task": dict(passes)})
    return pd.DataFrame(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--device", default=None)
    ap.add_argument("--limit", type=int, default=0, help="pilot: only the first N items per task")
    args = ap.parse_args()
    out = results_dir("e00_gate")
    samples = {}
    for t in ("xnli", "sentiment"):
        samples[t] = tasks.stratified_sample(tasks.load_task(t), args.n, seed=0)
        tasks.save_ids(out / f"sample_ids_{t}.json", samples[t])
        if args.limit:
            samples[t] = samples[t][: args.limit]
    for name in args.models:
        path = out / (f"scores_{name}.parquet" if not args.limit else f"pilot_scores_{name}.parquet")
        if path.exists() and not args.limit:
            print(f"{name}: exists, skipping")
            continue
        t0 = time.time()
        model, tok = load(name, args.device)
        t_load = time.time() - t0
        rows = []
        for t, items in samples.items():
            for it in items:
                for f in FORMS:
                    lp, n_tok = choice_logprobs(model, tok, build_prompt(t, it["forms"][f]), VERBALIZERS[t])
                    rows.append({"model": name, "task": t, "form": f, "id": it["id"], "label": it["label"],
                                 "logprobs": lp, "pred": int(np.argmax(lp)), "prompt_tokens": n_tok})
        df = pd.DataFrame(rows)
        df.to_parquet(path)
        secs = time.time() - t0
        print(f"{name}: {len(df)} scored in {secs:.0f}s (load {t_load:.0f}s; "
              f"{(secs - t_load) / len(df):.3f} s/prompt)", flush=True)
        del model
        import torch
        torch.cuda.empty_cache()
    if args.limit:
        return
    frames = [pd.read_parquet(p) for p in sorted(out.glob("scores_*.parquet"))]
    summary = summarize(pd.concat(frames, ignore_index=True))
    summary.to_csv(out / "summary.csv", index=False)
    g = gate(summary)
    write_json(out / "summary.json", {"summary": summary.to_dict("records"), "gate": g.to_dict("records")},
               {"n_per_task": args.n, "seed": 0, "templates": "e0_{xnli,sentiment}_v1",
                "verbalizers": VERBALIZERS, "forms": FORMS})
    print(summary[["model", "task", "form", "n", "acc", "acc_ci_low", "acc_ci_high", "acc_calibrated"]]
          .round(3).to_string(index=False))
    print(g.to_string(index=False))


if __name__ == "__main__":
    main()
