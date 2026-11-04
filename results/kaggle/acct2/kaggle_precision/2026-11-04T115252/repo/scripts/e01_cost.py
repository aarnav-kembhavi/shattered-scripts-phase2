"""E1 (local part): token cost atlas over FLORES for local tokenizers (tiktoken + HF tokenizer files).

Usage: python scripts/e01_cost.py --config configs/e01_cost.yaml
Outputs (results/e01_cost/):
  token_counts.parquet  one row per (tokenizer, lang, form, split, sentence)
  summary.parquet/.csv  per (tokenizer, lang, form): tokens/sentence, fertility, bytes/token, tax ratio vs English
                        with paired bootstrap 95% CI over sentences
  tokenizers.json       which tokenizers loaded, vocab sizes, failures
  run.json              provenance (config, git commit)
"""
import argparse
import json
import time

import numpy as np
import pandas as pd
import yaml

from shattered.data import corpora
from shattered.runlog import lower_priority, results_dir, write_json
from shattered.tok.registry import load_counter, load_hf_tokenizer
from shattered.translit import to_lossy
from shattered.translit.scheme import SCRIPTS, itrans_for


def build_texts(cfg: dict) -> pd.DataFrame:
    rows = []
    for lang in cfg["languages"]:
        scheme = itrans_for(SCRIPTS[lang]) if lang in SCRIPTS else None
        for split in cfg["splits"]:
            for i, t in enumerate(corpora.flores_any(lang, split, cfg["corpus"], nfc=cfg["nfc"])):
                rows.append((lang, "native", split, i, t))
                if scheme is not None:
                    if "itrans" in cfg["forms"]:
                        rows.append((lang, "itrans", split, i, scheme.encode(t)))
                    if "lossy" in cfg["forms"]:
                        rows.append((lang, "lossy", split, i, to_lossy(t, lang)))
    df = pd.DataFrame(rows, columns=["lang", "form", "split", "sent", "text"])
    df["words"] = df.text.str.split().str.len()
    df["bytes"] = df.text.str.encode("utf-8").str.len()
    df["chars"] = df.text.str.len()
    return df


def summarize(counts: pd.DataFrame, n_boot: int, seed: int) -> pd.DataFrame:
    out = []
    eng = counts[(counts.lang == "eng_Latn") & (counts.form == "native")]
    n_sent = eng.groupby("tokenizer").size().iloc[0]
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n_sent, size=(n_boot, n_sent))  # same resamples for every cell (paired)
    for (tk, lang, form), g in counts.groupby(["tokenizer", "lang", "form"], sort=False):
        e = eng[eng.tokenizer == tk].sort_values(["split", "sent"]).tokens.to_numpy()
        x = g.sort_values(["split", "sent"]).tokens.to_numpy()
        boot = x[idx].sum(1) / e[idx].sum(1)
        out.append({
            "tokenizer": tk, "lang": lang, "form": form, "n_sentences": len(x),
            "tokens_total": int(x.sum()), "tokens_per_sentence": x.mean(),
            "fertility": x.sum() / g.words.sum(), "bytes_per_token": g.bytes.sum() / x.sum(),
            "tax_ratio": x.sum() / e.sum(),
            "tax_ci_low": np.percentile(boot, 2.5), "tax_ci_high": np.percentile(boot, 97.5),
        })
    return pd.DataFrame(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/e01_cost.yaml")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config, encoding="utf-8"))
    lower_priority()
    out_dir = results_dir(cfg.get("results_name", "e01_cost"))
    t0 = time.time()
    texts = build_texts(cfg)
    print(f"{len(texts)} texts built in {time.time() - t0:.0f}s")

    frames, tk_info = [], {}
    for spec in cfg["tokenizers"]:
        tk = spec["id"]
        try:
            count = load_counter(spec)
            vocab = None
            if spec["kind"] == "hf":
                vocab = len(load_hf_tokenizer(tk))
            else:
                import tiktoken
                vocab = tiktoken.get_encoding(tk).n_vocab
            t1 = time.time()
            toks = count(texts.text.tolist())
            frames.append(texts.drop(columns="text").assign(tokenizer=tk, tokens=toks))
            tk_info[tk] = {**spec, "status": "ok", "vocab_size": vocab, "seconds": round(time.time() - t1, 1)}
            print(f"ok   {tk:45} vocab={vocab}")
        except Exception as e:  # noqa: BLE001 - record and continue
            tk_info[tk] = {**spec, "status": "failed", "error": f"{type(e).__name__}: {str(e)[:300]}"}
            print(f"FAIL {tk:45} {type(e).__name__}: {str(e)[:120]}")

    counts = pd.concat(frames, ignore_index=True)
    counts.to_parquet(out_dir / "token_counts.parquet")
    summ = summarize(counts, cfg["bootstrap"]["resamples"], cfg["bootstrap"]["seed"])
    meta = pd.DataFrame([{"tokenizer": k, **{f: v.get(f) for f in ("family", "gen", "released", "kind", "vocab_size")}}
                         for k, v in tk_info.items() if v["status"] == "ok"])
    summ = summ.merge(meta, on="tokenizer", how="left")
    summ.to_parquet(out_dir / "summary.parquet")
    summ.to_csv(out_dir / "summary.csv", index=False)
    (out_dir / "tokenizers.json").write_text(json.dumps(tk_info, indent=2, default=str), encoding="utf-8")
    write_json(out_dir / "run.json", {"n_texts": len(texts), "n_tokenizers_ok": len(frames),
                                      "seconds": round(time.time() - t0, 1)}, cfg)
    piv = summ[summ.form == "native"].pivot_table(index="gen", columns="lang", values="tax_ratio")
    print(piv.round(2).to_string())


if __name__ == "__main__":
    main()
