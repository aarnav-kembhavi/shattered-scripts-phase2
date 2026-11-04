"""Kannada word-frequency list from Kannada Wikipedia (for E4a word selection and E9 corpora).

Words = maximal runs of Kannada-block characters plus ZWJ/ZWNJ, after NFC normalization (punctuation, digits and Latin
are separators). The top `--annotate` words get token counts under several tokenizers, as a mid-sentence word
(leading space) in native script and in ITRANS.

Usage: python scripts/build_kn_wordfreq.py [--annotate 20000]
Outputs: data/processed/kn_wiki_wordfreq.parquet, results/data_kn_wiki/summary.json
"""
import argparse
import collections
import re
import unicodedata

import pandas as pd

from shattered.data import corpora
from shattered.runlog import REPO, results_dir, write_json
from shattered.tok.registry import load_counter
from shattered.translit import to_itrans

WORD = re.compile(r"[ಀ-೿‌‍]+")
TOKENIZERS = [
    {"id": "o200k_base", "kind": "tiktoken"}, {"id": "Qwen/Qwen3-8B", "kind": "hf"},
    {"id": "Qwen/Qwen3.5-9B", "kind": "hf"}, {"id": "google/gemma-4-E2B-it", "kind": "hf"},
    {"id": "sarvamai/sarvam-1", "kind": "hf"},
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--annotate", type=int, default=20000)
    args = ap.parse_args()
    texts = corpora.wikipedia("kn")
    counts = collections.Counter()
    for t in texts:
        counts.update(m.group().strip("‌‍") for m in WORD.finditer(unicodedata.normalize("NFC", t)))
    counts.pop("", None)
    df = pd.DataFrame(counts.most_common(), columns=["word", "count"])
    df["rank"] = range(1, len(df) + 1)
    top = df.head(args.annotate).copy()
    top["itrans"] = top.word.map(to_itrans)
    for spec in TOKENIZERS:
        count = load_counter(spec)
        name = spec["id"].split("/")[-1]
        top[f"ntok_native_{name}"] = count([" " + w for w in top.word])
        top[f"ntok_itrans_{name}"] = count([" " + w for w in top.itrans])
    df = df.merge(top.drop(columns=["count", "rank"]), on="word", how="left")
    path = REPO / "data" / "processed" / "kn_wiki_wordfreq.parquet"
    df.to_parquet(path)

    summary = {"n_articles": len(texts), "n_word_tokens": int(df["count"].sum()), "n_word_types": len(df),
               "types_with_count_ge_30": int((df["count"] >= 30).sum()), "annotated_top": args.annotate}
    ge30 = df[df["count"] >= 30]
    for spec in TOKENIZERS:
        name = spec["id"].split("/")[-1]
        col = f"ntok_native_{name}"
        sub = ge30[ge30[col].notna()]
        summary[f"{name}_multi_token_native_among_annotated_ge30"] = int((sub[col] >= 2).sum())
        summary[f"{name}_mean_tokens_native_top1000"] = float(df.head(1000)[col].mean())
        summary[f"{name}_mean_tokens_itrans_top1000"] = float(df.head(1000)[f"ntok_itrans_{name}"].mean())
    write_json(results_dir("data_kn_wiki") / "summary.json", summary,
               {"source": "wikimedia/wikipedia 20231101.kn", "revision": corpora.WIKI_REV,
                "tokenizers": [t["id"] for t in TOKENIZERS], "word_regex": WORD.pattern})
    print(summary)
    print(df.head(15).to_string())


if __name__ == "__main__":
    main()
