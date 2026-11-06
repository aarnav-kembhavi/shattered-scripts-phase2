"""E5 analysis: table T6, learning curves, equal-compute comparison. Reads only results/e05_pretrain and E5 data meta.

Usage: python scripts/e05_analysis.py
Outputs: results/e05_pretrain/T6.csv, curves.parquet, analysis.json; figures via shattered.plots.e05
"""
import json
import re

import numpy as np
import pandas as pd
from scipy import stats

from shattered.pretrain.data import read_stories
from shattered.runlog import REPO, lower_priority, results_dir, write_json

RES = REPO / "results" / "e05_pretrain"


def main() -> None:
    lower_priority()
    meta = json.load(open(REPO / "data" / "processed" / "e05" / "meta_400000000.json"))
    n_words_valid = sum(len(s.split()) + 0 for s in read_stories("valid"))  # whitespace words, EOS excluded
    rows, curves = [], []
    for d in sorted(RES.glob("run_v*_s*")):
        v, s = map(int, re.match(r"run_v(\d+)_s(\d+)", d.name).groups())
        fin = json.load(open(d / "final.json"))
        m = meta[str(v)]
        mp = fin["minimal_pairs"]
        rows.append({"vocab": v, "seed": s, "bytes_per_token": m["bytes_per_token_valid"],
                     "tokens_per_word": m["valid_tokens"] / n_words_valid, "ctx_tokens": fin["ctx_tokens"],
                     "params_embedding": fin["params"]["embedding"], "params_non_embedding": fin["params"]["non_embedding"],
                     "train_flops": fin["train_flops"], "val_bpb": fin["val_bpb_full"],
                     **{f"mp_{k}": x["acc_total_logprob"] for k, x in mp.items()},
                     **{f"mp_perbyte_{k}": x["acc_per_byte"] for k, x in mp.items()}})
        bytes_per_step = fin["train_bytes_seen"] / fin["steps"]
        flops_per_step = fin["train_flops"] / fin["steps"]
        for line in open(d / "log.jsonl"):
            r = json.loads(line)
            if "val_bpb_subset" in r:
                curves.append({"vocab": v, "seed": s, "step": r["step"], "bytes_seen": r["step"] * bytes_per_step,
                               "flops": r["step"] * flops_per_step, "val_bpb_subset": r["val_bpb_subset"],
                               **{f"mp_{k}": a for k, a in r.get("mp_acc", {}).items()}})
    runs = pd.DataFrame(rows).sort_values(["vocab", "seed"])
    cur = pd.DataFrame(curves)
    cur.to_parquet(RES / "curves.parquet")
    agg = runs.groupby("vocab").agg(["mean", "std"])
    t6 = pd.DataFrame({
        "vocab": agg.index, "bytes_per_token": agg[("bytes_per_token", "mean")].values,
        "tokens_per_word": agg[("tokens_per_word", "mean")].values, "ctx_tokens": agg[("ctx_tokens", "mean")].values,
        "params_embedding": agg[("params_embedding", "mean")].values,
        "params_non_embedding": agg[("params_non_embedding", "mean")].values,
        "train_flops": agg[("train_flops", "mean")].values,
        "val_bpb_mean": agg[("val_bpb", "mean")].values, "val_bpb_sd": agg[("val_bpb", "std")].values,
        "mp_all_mean": agg[("mp_all", "mean")].values, "mp_all_sd": agg[("mp_all", "std")].values,
        "n_seeds": runs.groupby("vocab").size().values})
    for ph in ["subject_verb_agreement_singular", "subject_verb_agreement_plural", "determiner_noun_agreement",
               "irregular_past"]:
        t6[f"mp_{ph}_mean"] = agg[(f"mp_{ph}", "mean")].values
    t6.to_csv(RES / "T6.csv", index=False)

    # monotonicity across conditions (seed means), and effect size vs seed noise
    rho_bpb = stats.spearmanr(t6.tokens_per_word, t6.val_bpb_mean)
    rho_mp = stats.spearmanr(t6.tokens_per_word, t6.mp_all_mean)
    span = t6.val_bpb_mean.max() - t6.val_bpb_mean.min()
    # equal compute: each condition's subset-BPB at the smallest total training FLOPs of any condition
    fmin = runs.train_flops.min()
    eq = []
    for (v, s), g in cur.groupby(["vocab", "seed"]):
        g = g.sort_values("flops")
        eq.append({"vocab": v, "seed": s,
                   "val_bpb_subset_at_equal_flops": float(np.interp(fmin, g.flops, g.val_bpb_subset)),
                   "mp_all_at_equal_flops": float(np.interp(fmin, g.flops, g.mp_all)) if "mp_all" in g else None})
    eqdf = pd.DataFrame(eq).groupby("vocab").agg(["mean", "std"])
    payload = {"T6": t6.to_dict("records"), "runs": runs.to_dict("records"),
               "spearman_tokens_per_word_vs_bpb": {"rho": rho_bpb.statistic, "p": rho_bpb.pvalue},
               "spearman_tokens_per_word_vs_mp": {"rho": rho_mp.statistic, "p": rho_mp.pvalue},
               "bpb_span_across_conditions": span, "max_seed_sd_bpb": float(t6.val_bpb_sd.max()),
               "equal_flops": {"flops": fmin, "by_vocab": {int(k): {"bpb_mean": r[("val_bpb_subset_at_equal_flops", "mean")],
                                                                     "bpb_sd": r[("val_bpb_subset_at_equal_flops", "std")],
                                                                     "mp_mean": r[("mp_all_at_equal_flops", "mean")]}
                                                             for k, r in eqdf.iterrows()}},
               "n_words_valid": n_words_valid}
    write_json(results_dir("e05_pretrain") / "analysis.json", payload, {"source": "results/e05_pretrain/run_*"})
    print(t6.round(4).to_string(index=False))
    print("spearman tpw~bpb", rho_bpb, "| tpw~mp", rho_mp, "| span", round(span, 4), "max seed sd",
          round(t6.val_bpb_sd.max(), 4))
    print("equal flops", f"{fmin:.3g}", {int(k): round(r[("val_bpb_subset_at_equal_flops", "mean")], 4)
                                          for k, r in eqdf.iterrows()})


if __name__ == "__main__":
    main()
