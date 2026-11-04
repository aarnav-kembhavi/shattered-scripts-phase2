"""E9 evaluation (GATE: token savings only, no accuracy runs).

For each best scheme from e09_search.py: exact round trip on FLORES Kannada and a Kannada Wikipedia sample, and
held-out sentence-level token counts on every distinct local tokenizer, versus native script and ITRANS.

Usage: python scripts/e09_eval.py [--corpus flores_plus]
Outputs: results/e09_romanize/savings.csv, savings.json, schemes.md (mapping tables)
"""
import argparse
import json

import pandas as pd

from shattered.data import corpora
from shattered.romanize_opt.candidates import itrans_assignment, tables
from shattered.runlog import REPO, lower_priority, results_dir, write_json
from shattered.tok.registry import load_counter
from shattered.translit import ITRANS
from shattered.translit.scheme import Scheme

# distinct tokenizers from E1 (one representative per identical group)
EVAL_TOKENIZERS = ["o200k_base", "cl100k_base", "r50k_base", "google/gemma-4-E2B-it", "Qwen/Qwen3.5-9B",
                   "Qwen/Qwen3-8B", "sarvamai/sarvam-1", "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                   "mistralai/Mistral-Nemo-Instruct-2407", "deepseek-ai/DeepSeek-V3", "BharatGenAI/Param-1-2.9B-Instruct",
                   "bigscience/bloom-560m", "utter-project/EuroLLM-9B-Instruct-2512"]
LABELS = {"o200k_base": "o200k (GPT-4o)", "cl100k_base": "cl100k (GPT-4)", "r50k_base": "r50k (GPT-3)",
          "google/gemma-4-E2B-it": "Gemma 4", "Qwen/Qwen3.5-9B": "Qwen 3.5-3.8", "Qwen/Qwen3-8B": "Qwen 1.5-3",
          "sarvamai/sarvam-1": "Sarvam-1", "TinyLlama/TinyLlama-1.1B-Chat-v1.0": "Llama 2",
          "mistralai/Mistral-Nemo-Instruct-2407": "Tekken (Nemo/Sarvam-M)", "deepseek-ai/DeepSeek-V3": "DeepSeek-V3",
          "BharatGenAI/Param-1-2.9B-Instruct": "Param-1", "bigscience/bloom-560m": "BLOOM",
          "utter-project/EuroLLM-9B-Instruct-2512": "EuroLLM"}


def scheme_from(assignment: list) -> Scheme:
    c, v, g = tables({(t, n): s for t, n, s in assignment})
    return Scheme("e09", c, v, g)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="flores_plus")
    ap.add_argument("--wiki-every", type=int, default=30, help="round-trip every Nth Wikipedia article")
    args = ap.parse_args()
    lower_priority()
    best = json.load(open(REPO / "results" / "e09_romanize" / "best_schemes.json", encoding="utf-8"))["best"]
    native = [t for s in ("dev", "devtest") for t in corpora.flores_any("kan_Knda", s, args.corpus, nfc=True)]
    wiki = corpora.wikipedia("kn")[:: args.wiki_every]
    forms = {"native": native, "itrans": [ITRANS.encode(t) for t in native]}
    roundtrip = {}
    for key, r in best.items():
        sch = scheme_from(r["assignment"])
        enc = [sch.encode(t) for t in native]
        ok_fl = sum(sch.decode(e) == t for e, t in zip(enc, native))
        ok_wk = sum(sch.roundtrips(t) for t in wiki)
        roundtrip[key] = {"flores_exact": ok_fl, "flores_n": len(native), "wiki_exact": ok_wk, "wiki_n": len(wiki)}
        print(key, roundtrip[key], flush=True)
        if ok_fl == len(native) and ok_wk == len(wiki):
            forms[f"e09:{key}"] = enc
    rows = []
    for tk in EVAL_TOKENIZERS:
        count = load_counter({"id": tk, "kind": "tiktoken" if tk.endswith("_base") else "hf"})
        totals = {f: sum(count(texts)) for f, texts in forms.items()}
        for f, n in totals.items():
            rows.append({"tokenizer": LABELS[tk], "form": f, "tokens": n, "vs_native": n / totals["native"],
                         "vs_itrans": n / totals["itrans"]})
        print(LABELS[tk], {f: round(n / totals["itrans"], 3) for f, n in totals.items()}, flush=True)
    df = pd.DataFrame(rows)
    out = results_dir("e09_romanize")
    df.to_csv(out / "savings.csv", index=False)
    write_json(out / "savings.json", {"rows": rows, "roundtrip": roundtrip, "n_sentences": len(native)},
               {"corpus": args.corpus, "wiki_every": args.wiki_every, "tokenizers": EVAL_TOKENIZERS})
    # mapping tables
    lines = ["# E9 schemes (best per target x variant)\n", "Units whose spelling differs from ITRANS.\n"]
    itr = itrans_assignment()
    for key, r in best.items():
        diffs = [(n, itr[(t, n)], s) for t, n, s in r["assignment"] if itr.get((t, n)) != s]
        lines.append(f"\n## {key}\n\n| unit | ITRANS | scheme |\n|---|---|---|")
        lines += [f"| {n} | `{a}` | `{b}` |" for n, a, b in diffs]
    (out / "schemes.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
