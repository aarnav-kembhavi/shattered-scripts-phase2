"""E0 add-on: native vs ITRANS tokens per word for every E0 candidate's tokenizer (FLORES Kannada, in context).

Each whitespace word's token span comes from the offset-mapping alignment (src/shattered/tok/align.py), so counts are
per word in running text, not for isolated words. ITRANS preserves whitespace, so words correspond one to one.

Usage: python scripts/e00_tokens_per_word.py [--corpus flores_plus]
Outputs: results/e00_gate/tokens_per_word.csv (one row per candidate tokenizer), tokens_per_word.json
"""
import argparse

import numpy as np
import pandas as pd

from shattered.data import corpora
from shattered.models import CANDIDATES
from shattered.runlog import results_dir, write_json
from shattered.tok.align import word_spans
from shattered.tok.registry import load_hf_tokenizer
from shattered.translit import to_itrans


def per_word_counts(tok, texts: list[str]) -> np.ndarray:
    enc = tok(texts, return_offsets_mapping=True, add_special_tokens=False)
    counts = []
    for text, offs in zip(texts, enc["offset_mapping"]):
        spans = word_spans(text, offs)
        counts.extend(s.n_tokens for s in spans)
    return np.asarray(counts)


def summarize(c: np.ndarray, n_tokens_total: int, n_words: int) -> dict:
    return {"mean_tokens_per_word": float(c.mean()), "fertility": n_tokens_total / n_words,
            "share_ge2": float((c >= 2).mean()), "share_ge4": float((c >= 4).mean()),
            "median": float(np.median(c))}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="flores_plus", choices=["flores_plus", "flores200"])
    args = ap.parse_args()
    native = [t for s in ("dev", "devtest") for t in corpora.flores_any("kan_Knda", s, args.corpus, nfc=True)]
    itrans = [to_itrans(t) for t in native]
    n_words = sum(len(t.split()) for t in native)
    assert n_words == sum(len(t.split()) for t in itrans)
    rows = []
    for repo, family, note in CANDIDATES:
        try:
            tok = load_hf_tokenizer(repo)
        except Exception as e:  # noqa: BLE001 - gated or remote-code tokenizers are recorded, not fatal
            rows.append({"repo": repo, "family": family, "status": f"unavailable: {type(e).__name__}"})
            print(f"skip {repo}: {type(e).__name__}")
            continue
        row = {"repo": repo, "family": family, "status": "ok"}
        for form, texts in (("native", native), ("itrans", itrans)):
            c = per_word_counts(tok, texts)
            total = sum(len(x) for x in tok(texts, add_special_tokens=False)["input_ids"])
            row.update({f"{form}_{k}": v for k, v in summarize(c, total, n_words).items()})
            row[f"{form}_n_words_aligned"] = len(c)
        row["itrans_over_native_tokens_per_word"] = row["itrans_mean_tokens_per_word"] / row["native_mean_tokens_per_word"]
        rows.append(row)
        print(f"{repo:40} native {row['native_mean_tokens_per_word']:.2f} itrans {row['itrans_mean_tokens_per_word']:.2f}")
    df = pd.DataFrame(rows)
    out = results_dir("e00_gate")
    df.to_csv(out / "tokens_per_word.csv", index=False)
    write_json(out / "tokens_per_word.json", {"rows": rows, "n_sentences": len(native), "n_words": n_words},
               {"corpus": args.corpus, "lang": "kan_Knda", "splits": ["dev", "devtest"], "nfc": True})


if __name__ == "__main__":
    main()
