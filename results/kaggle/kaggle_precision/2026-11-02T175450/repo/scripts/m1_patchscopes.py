"""M1a: Patchscopes detokenization layer per word (FragMend setup), native vs ITRANS vs English.

Words: Kannada words in the selected E0 items (maximal Kannada-letter runs, NFC); each is also run in its ITRANS
spelling (paired by construction). English words: maximal ASCII-letter runs in the items' English form (reference;
not paired). Each unique word is run once per form.

Usage: python scripts/m1_patchscopes.py --model qwen3-1.7b [--n-items 50] [--max-new auto|20]
Outputs: results/m1_detok/<model>/patchscopes_<tag>.parquet (one row per word x form), outputs_<tag>.jsonl,
         summary_<tag>.json (pre-registered Delta with paired bootstrap CI)
"""
import argparse
import json
import re
import time

import numpy as np
import pandas as pd

from shattered.data import tasks
from shattered.interp import patchscopes as ps
from shattered.interp.load import load, n_layers
from shattered.runlog import REPO, results_dir, write_json
from shattered.translit import to_itrans

KN_WORD = re.compile(r"[ಀ-೿‌‍]+")
EN_WORD = re.compile(r"[A-Za-z]+")


def pilot_items(n: int) -> list[dict]:
    """First n/2 items of each E0 sample (same seed, so these are E0 items)."""
    out = []
    for t in ("xnli", "sentiment"):
        out += tasks.stratified_sample(tasks.load_task(t), 200, seed=0)[: n // 2]
    return out


def item_texts(it: dict, form: str) -> str:
    return " ".join(it["forms"][form].values())


def word_inventory(items: list[dict]) -> tuple[list[str], list[str]]:
    kn, en = [], []
    for it in items:
        kn += [w.strip("‌‍") for w in KN_WORD.findall(item_texts(it, "native"))]
        en += EN_WORD.findall(item_texts(it, "english"))
    return sorted(set(w for w in kn if w)), sorted(set(en))


def paired_delta(df: pd.DataFrame, L: int, n_boot: int = 10000, seed: int = 0) -> dict:
    piv = df[df.form.isin(["native", "itrans"])].pivot_table(index="kn_word", columns="form", values="detok_layer")
    both = piv.dropna()
    d = ((both["native"] - both["itrans"]) / L).to_numpy()
    if len(d) == 0:
        return {"n_words_both": 0}
    rng = np.random.default_rng(seed)
    boot = d[rng.integers(0, len(d), size=(n_boot, len(d)))].mean(1)
    lo, hi = np.percentile(boot, [2.5, 97.5])
    verdict = "ITRANS-earlier" if lo > 0 else ("native-earlier" if hi < 0 else "no difference")
    return {"n_words_both": len(d), "delta_mean": float(d.mean()), "ci_low": float(lo), "ci_high": float(hi),
            "verdict": verdict}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--n-items", type=int, default=50)
    ap.add_argument("--max-new", default="20", help="'20' (FragMend) or 'auto' (= word tokens + 10, at least 20)")
    ap.add_argument("--batch-size", type=int, default=None)
    args = ap.parse_args()
    tag = f"n{args.n_items}_max{args.max_new}"
    out = results_dir(f"m1_detok/{args.model}")
    items = pilot_items(args.n_items)
    kn_words, en_words = word_inventory(items)
    model, tok = load(args.model, "cuda")
    L = n_layers(model)
    template = ps.build_template(tok)
    jobs = [("native", w, w) for w in kn_words] + [("itrans", w, to_itrans(w)) for w in kn_words] + \
           [("english", None, w) for w in en_words]
    rows, t0 = [], time.time()
    with open(out / f"outputs_{tag}.jsonl", "w", encoding="utf-8") as fo:
        for form, kn, w in jobs:
            ntok = len(tok(w, add_special_tokens=False)["input_ids"])
            max_new = 20 if args.max_new == "20" else max(20, ntok + 10)
            states = ps.word_states(model, tok, w)
            outs = ps.decode_states(model, tok, states, template, max_new_tokens=max_new, batch_size=args.batch_size)
            layer = ps.detok_layer(w, outs)
            rows.append({"form": form, "kn_word": kn, "word": w, "n_tokens": ntok, "n_chars": len(w),
                         "detok_layer": layer, "detok_layer_frac": None if layer is None else layer / L,
                         "max_new_tokens": max_new})
            fo.write(json.dumps({"form": form, "word": w, "outputs": outs}, ensure_ascii=False) + "\n")
    secs = time.time() - t0
    df = pd.DataFrame(rows)
    df.to_parquet(out / f"patchscopes_{tag}.parquet")
    by_form = df.groupby("form").agg(n_words=("word", "size"), success_rate=("detok_layer", lambda s: s.notna().mean()),
                                     mean_layer=("detok_layer", "mean"), median_tokens=("n_tokens", "median"))
    summ = {"model": args.model, "n_layers": L, "n_items": len(items), "seconds": secs,
            "seconds_per_word": secs / len(jobs), "by_form": by_form.reset_index().to_dict("records"),
            "paired_native_minus_itrans": paired_delta(df, L)}
    write_json(out / f"summary_{tag}.json", summ, vars(args))
    print(json.dumps({k: v for k, v in summ.items() if k != "by_form"}, indent=1, default=str))
    print(by_form.round(3).to_string())


if __name__ == "__main__":
    main()
